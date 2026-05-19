import streamlit as st

from .config import APP_CAPTION, APP_TITLE, PREVIEW_HEIGHT, XLSX_MIME
from .theme import THEME_MARKUP
from .types import ProcessedWorkbook


def _apply_modern_theme() -> None:
    st.markdown(THEME_MARKUP, unsafe_allow_html=True)


def _build_preview_df(result: ProcessedWorkbook):
        preview_df = result.summary_df.drop(columns=["_source_metric_row", "_source_week_row"], errors="ignore")

        if "TEL S/N" not in preview_df.columns:
                return preview_df.head(20)

        tel_values = preview_df["TEL S/N"].dropna().astype(str).str.strip()
        tel_values = tel_values[tel_values != ""]
        selected_tels = tel_values.drop_duplicates().head(2).tolist()
        if not selected_tels:
                return preview_df.head(20)

        return preview_df[preview_df["TEL S/N"].astype(str).isin(selected_tels)]


def _build_dark_preview_styler(preview_df):
    return (
        preview_df.style
        .set_table_styles(
            [
                {
                    "selector": "th.col_heading",
                    "props": "background-color: #122740 !important; color: #eef7ff !important; border: 1px solid #2a4666 !important;",
                },
                {
                    "selector": "th.row_heading, th.index_name, th.blank",
                    "props": "background-color: #102239 !important; color: #dfefff !important; border: 1px solid #2a4666 !important;",
                },
                {
                    "selector": "td",
                    "props": "background-color: #0c1a2d !important; color: #eaf4ff !important; border: 1px solid #203752 !important;",
                },
            ]
        )
        .set_properties(**{"background-color": "#0c1a2d", "color": "#eaf4ff"})
    )


def render_page_header() -> None:
    _apply_modern_theme()
    title_parts = APP_TITLE.split(" ", 1)
    if len(title_parts) == 2:
        title_html = f'{title_parts[0]} <span class="hero-title-accent">{title_parts[1]}</span>'
    else:
        title_html = f'<span class="hero-title-accent">{APP_TITLE}</span>'

    st.markdown(
        f"""
        <div class="hero-shell">
            <h1 class="hero-title">{title_html}</h1>
            <p class="hero-caption">{APP_CAPTION}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_controls():
    st.markdown('<div class="controls-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="upload-panel">
            <p class="upload-title">Upload Input Workbook</p>
            <p class="upload-copy">Drop your Excel file here or click the button to browse. Accepted format: .xlsx</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader("Upload workbook", type=["xlsx"], label_visibility="collapsed")

    st.markdown('<div class="controls-spacer-md"></div>', unsafe_allow_html=True)
    sort_active_first = st.checkbox("Sort active equipment first", value=True)

    if uploaded_file is not None:
        st.markdown(
            f"""
            <div class="selected-file-chip">
                <strong>Selected file</strong>
                <span class="selected-file-name">{uploaded_file.name}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="controls-spacer-md"></div>', unsafe_allow_html=True)
    process_clicked = st.button("Process File", type="primary", disabled=uploaded_file is None)
    return uploaded_file, sort_active_first, process_clicked


def render_success(result: ProcessedWorkbook) -> None:
    st.success(f"Done. Rows summarized: {len(result.summary_df)}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Time elapsed", f"{result.elapsed_seconds:.2f} s")
    col2.metric("Unique customers", result.unique_customers)
    col3.metric("Unique equipment", result.unique_equipment)

    diag_col1, diag_col2, diag_col3 = st.columns(3)
    diag_col1.metric("Week columns", result.parsed_week_columns)
    diag_col2.metric("Rows with missing TEL S/N", result.missing_tel_sn_rows)
    diag_col3.metric("Metric rows", result.total_metric_rows)


def render_preview(result: ProcessedWorkbook) -> None:
    preview_df = _build_preview_df(result)
    preview_styler = _build_dark_preview_styler(preview_df)
    st.markdown('<div class="section-spacer-lg"></div>', unsafe_allow_html=True)
    st.subheader("Preview")
    st.caption("Showing rows for up to 2 unique equipment in this preview.")
    st.dataframe(preview_styler, width="stretch", height=PREVIEW_HEIGHT)


def render_download(result: ProcessedWorkbook) -> None:
    st.markdown('<div class="section-spacer-lg"></div>', unsafe_allow_html=True)
    st.subheader("Download")
    st.caption("Choose output file name, then click download. Save location is handled by your browser.")

    download_name = st.text_input(
        "Output file name",
        value=result.output_name,
        key=f"download_name_{result.output_name}",
        help="Example: E10Monitor_20260518094306_processed.xlsx",
    ).strip()

    if not download_name:
        download_name = result.output_name
    if not download_name.lower().endswith(".xlsx"):
        download_name = f"{download_name}.xlsx"

    left_col, right_col = st.columns([3, 1])
    with left_col:
        st.download_button(
            label="Download Processed File",
            data=result.output_bytes,
            file_name=download_name,
            mime=XLSX_MIME,
            type="primary",
        )
    with right_col:
        clear_clicked = st.button("Clear Result", type="secondary", key="clear_result_button", use_container_width=True)

    return clear_clicked
