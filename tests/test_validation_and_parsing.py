import io

import pandas as pd
import pytest

from e10_app import extract_trend_rows
from webui.services import process_excel_upload


def _workbook_bytes(sheets: dict[str, pd.DataFrame]) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    return buffer.getvalue()


def test_process_excel_upload_rejects_missing_trend_sheet() -> None:
    condition_df = pd.DataFrame(
        [
            ["Customer", "TEL S/N"],
            ["ACME", "EQP001"],
        ]
    )

    file_bytes = _workbook_bytes({"Condition": condition_df})

    with pytest.raises(ValueError, match=r"Missing required sheet\(s\): Trend"):
        process_excel_upload(file_name="missing_trend.xlsx", file_bytes=file_bytes, sort_active_first=True)


def test_extract_trend_rows_returns_empty_without_week_row() -> None:
    trend_df = pd.DataFrame(
        [
            ["E10 Status & Processed Wafer Count [EQP001]", ""],
            ["Exposure Count", 123],
            ["Idle Time", 20],
        ]
    )

    rows = extract_trend_rows(trend_df)

    assert rows == []


def test_extract_trend_rows_excludes_average_block() -> None:
    trend_df = pd.DataFrame(
        [
            ["", "ww2601"],
            ["E10 Status & Processed Wafer Count [Average]", ""],
            ["Exposure Count", 100],
            ["", ""],
            ["E10 Status & Processed Wafer Count [EQP777]", ""],
            ["", "ww2601"],
            ["Exposure Count", 55],
        ]
    )

    rows = extract_trend_rows(trend_df)

    assert len(rows) == 1
    assert rows[0]["Equipment"] == "EQP777"
    assert rows[0]["Metric"] == "Exposure Count"
    assert rows[0]["ww2601"] == 55
