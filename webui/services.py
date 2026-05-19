import tempfile
import time
import warnings
import logging
from pathlib import Path

import pandas as pd

from e10_app import build_summary_from_frames, write_summary_with_format

from .types import ProcessedWorkbook


logger = logging.getLogger(__name__)


def _count_unique_non_empty(summary_df, column_name: str) -> int:
    if column_name not in summary_df.columns:
        return 0

    values = summary_df[column_name].dropna().astype(str).str.strip()
    values = values[values != ""]
    return int(values.nunique())


def _load_and_validate_workbook(input_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        workbook = pd.ExcelFile(input_path)
    except Exception as exc:
        raise ValueError("The uploaded file is not a valid Excel workbook (.xlsx).") from exc
    try:
        required_sheets = {"Condition", "Trend"}
        missing_sheets = sorted(required_sheets - set(workbook.sheet_names))
        if missing_sheets:
            missing_text = ", ".join(missing_sheets)
            raise ValueError(
                f"The uploaded file is not a supported E10 export. Missing required sheet(s): {missing_text}."
            )

        condition_df = pd.read_excel(input_path, sheet_name="Condition", header=None)
        trend_df = pd.read_excel(input_path, sheet_name="Trend", header=None)

        if condition_df.empty or trend_df.empty:
            raise ValueError("The uploaded workbook is missing required data rows in Condition or Trend sheet.")
        if condition_df.shape[1] < 2 or trend_df.shape[1] < 2:
            raise ValueError("The uploaded workbook has an unexpected sheet structure (not enough columns).")

        condition_values = {str(value).strip() for value in condition_df.fillna("").to_numpy().flatten() if str(value).strip()}
        has_condition_headers = {"Customer", "TEL S/N"}.issubset(condition_values)

        trend_first_col = trend_df.iloc[:, 0].fillna("").astype(str).str.strip() if not trend_df.empty else pd.Series(dtype=str)
        has_trend_title = trend_first_col.str.contains(r"E10 Status & Processed Wafer Count \[", regex=True).any()

        if not has_condition_headers or not has_trend_title:
            raise ValueError(
                "The uploaded file does not match the expected E10 export format. "
                "Please upload the usual E10 monitor Excel file containing Condition and Trend data."
            )
        return condition_df, trend_df
    finally:
        workbook.close()


def _to_user_friendly_error(exc: Exception) -> str:
    message = str(exc)
    if isinstance(exc, PermissionError) or "WinError 32" in message:
        return (
            "The app could not finish processing because the temporary output file was locked during creation. "
            "Please try again. If the issue continues, close any Excel windows that may be open and retry."
        )

    return message


def process_excel_upload(file_name: str, file_bytes: bytes, sort_active_first: bool) -> ProcessedWorkbook:
    if not file_bytes:
        raise ValueError("The uploaded file is empty. Please upload a valid .xlsx file.")

    start_time = time.perf_counter()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        input_path = tmp_path / file_name
        input_path.write_bytes(file_bytes)

        condition_df, trend_df = _load_and_validate_workbook(input_path)

        output_name = f"{Path(file_name).stem}_processed.xlsx"
        output_path = tmp_path / output_name

        # Some Excel files contain features that emit non-fatal parser warnings.
        # Keep the UI clean by filtering known benign warnings during processing.
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message=r"Workbook contains no default style.*",
                    category=UserWarning,
                )
                warnings.filterwarnings(
                    "ignore",
                    message=r"Data Validation extension is not supported and will be removed.*",
                    category=UserWarning,
                )

                summary_df = build_summary_from_frames(condition_df, trend_df, sort_active_first=sort_active_first)
                write_summary_with_format(input_path, output_path, summary_df)
        except Exception as exc:
            logger.exception(
                "Failed to process workbook",
                extra={
                    "file_name": file_name,
                    "file_size_bytes": len(file_bytes),
                    "sort_active_first": sort_active_first,
                },
            )
            raise ValueError(_to_user_friendly_error(exc)) from exc

        elapsed_seconds = time.perf_counter() - start_time
        week_columns = [c for c in summary_df.columns if c.startswith("ww")]
        missing_tel_sn_rows = 0
        if "TEL S/N" in summary_df.columns:
            tel_series = summary_df["TEL S/N"].fillna("").astype(str).str.strip()
            missing_tel_sn_rows = int((tel_series == "").sum())

        return ProcessedWorkbook(
            output_name=output_name,
            output_bytes=output_path.read_bytes(),
            summary_df=summary_df,
            elapsed_seconds=elapsed_seconds,
            unique_customers=_count_unique_non_empty(summary_df, "Customer"),
            unique_equipment=_count_unique_non_empty(summary_df, "TEL S/N"),
            parsed_week_columns=len(week_columns),
            missing_tel_sn_rows=missing_tel_sn_rows,
            total_metric_rows=len(summary_df),
        )
