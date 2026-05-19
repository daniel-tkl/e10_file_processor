# E10 Monitor Processor

This tool converts an E10 monitor export file (Excel) into a summarized processed file.

## Features

1. Reads source workbook sheets:
	- Condition
	- Trend
2. Extracts equipment metadata from Condition:
	- Customer
	- Area
	- Building
	- TEL S/N
	- Customer ID
	- Exposure Type
3. Extracts metric blocks from Trend by equipment title.
4. Removes the Average block automatically.
5. Removes the Equipment output column (TEL S/N is used instead).
6. Supports all available equipment blocks, including blocks without local week-header repetition.
7. Produces one Summary sheet with metric rows and ww columns.
8. Preserves Excel formatting (style, fill, border, alignment, number format) in output cells.
9. Default sorting puts equipment with non-zero ww data at the top.
10. Optional flag to keep original source order.
11. Default output naming:
	- input file name + _processed.xlsx
	- Example: E10Monitor_20260518094306.xlsx -> E10Monitor_20260518094306_processed.xlsx

## Requirements

1. Python 3.10+
2. Packages:
	- pandas
	- openpyxl
	- streamlit

Install packages:

```powershell
pip install pandas openpyxl streamlit
```

## Web UI (Streamlit)

Run a simple web UI:

```powershell
streamlit run .\streamlit_app.py
```

Then open the local URL shown in terminal (usually http://localhost:8501).

Run regression tests:

```powershell
pytest
```

Web UI features:

1. Upload .xlsx input file
2. Toggle active-equipment-first sorting
3. Process file using the same logic as CLI
4. Preview summary table
5. Download processed .xlsx

Modular Streamlit structure:

1. streamlit_app.py
	- Entry point only (thin orchestrator)
2. webui/config.py
	- UI constants and page settings
3. webui/services.py
	- Processing service that calls core Excel logic
4. webui/ui.py
	- Reusable UI rendering functions
5. webui/types.py
	- Shared dataclass for processed result payload

Why this modular design:

1. Separation of concerns
	- streamlit_app.py only coordinates flow.
	- UI rendering is isolated from file-processing logic.
	- Core Excel business logic stays in e10_app.py and is reused by both CLI and Web UI.
2. Easier maintenance
	- UI text/layout changes are made in webui/ui.py without touching processing code.
	- Processing behavior changes are made in e10_app.py or webui/services.py without breaking UI components.
3. Better testability
	- Service functions can be tested without Streamlit runtime.
	- UI functions can be validated independently from workbook parsing/writing.
4. Safer future extension
	- New pages or controls can be added by creating new UI functions/modules.
	- New processing flows can be added as new service functions.
	- Shared payload types in webui/types.py reduce coupling and simplify refactoring.
5. Reduced regression risk
	- Changes are localized to a module responsibility.
	- Smaller files make code review and debugging faster.

Recommended change guide:

1. Change labels/layout/controls:
	- Edit webui/ui.py (and webui/config.py for constants).
2. Change processing pipeline for uploaded files:
	- Edit webui/services.py.
3. Change summary generation/output format rules:
	- Edit e10_app.py.
4. Change cross-module response structure:
	- Edit webui/types.py.

## Usage

Run with default behavior:

```powershell
python .\e10_app.py E10Monitor_20260518094306.xlsx
```

Run with custom output file:

```powershell
python .\e10_app.py E10Monitor_20260518094306.xlsx -o E10Monitor_20260518094306_processed_custom.xlsx
```

Run and keep original equipment order (disable active-first sorting):

```powershell
python .\e10_app.py E10Monitor_20260518094306.xlsx --no-sort-active-first
```

Run with explicit active-first sorting (same as default):

```powershell
python .\e10_app.py E10Monitor_20260518094306.xlsx --sort-active-first
```

## Command Arguments

1. input_file (required)
	- Path to source .xlsx file.

2. -o, --output (optional)
	- Output file path.
	- If not provided, the script writes: <input_stem>_processed.xlsx

3. --sort-active-first (optional, default enabled)
	- Put equipment with non-zero ww data first.

4. --no-sort-active-first (optional)
	- Disable active-first sorting.
	- Preserve original source order.

## Output Columns

1. Customer
2. Area
3. Building
4. TEL S/N
5. Customer ID
6. Exposure Type
7. Metric
8. ww columns (for example ww2601, ww2602, ...)

## Notes

1. If the script looks stuck, verify you are running from the project folder or using full file paths.
2. Processing time depends on workbook size and style copying, but should complete normally for the provided sample.