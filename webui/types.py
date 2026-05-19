from dataclasses import dataclass

import pandas as pd


@dataclass
class ProcessedWorkbook:
    output_name: str
    output_bytes: bytes
    summary_df: pd.DataFrame
    elapsed_seconds: float
    unique_customers: int
    unique_equipment: int
    parsed_week_columns: int
    missing_tel_sn_rows: int
    total_metric_rows: int
