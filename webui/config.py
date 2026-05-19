"""Static configuration values and utility helpers for the web UI."""

from pathlib import Path


APP_TITLE = "E10 Monitor Processor"
APP_CAPTION = "Upload an E10 monitor Excel file and download the processed summary."
APP_ICON = ":bar_chart:"
PREVIEW_HEIGHT = 420
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def load_app_icon() -> str:
	"""Return favicon path when available, otherwise fallback to the default icon."""
	icon_path = Path(__file__).resolve().parent.parent / "assets" / "favicon.ico"
	if icon_path.exists():
		return str(icon_path)
	return APP_ICON
