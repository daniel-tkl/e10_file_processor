import streamlit as st
import hashlib
import logging

from webui.config import APP_TITLE, load_app_icon
from webui.services import process_excel_upload
from webui.ui import render_controls, render_download, render_page_header, render_preview, render_success


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


st.set_page_config(page_title=APP_TITLE, page_icon=load_app_icon(), layout="wide")
render_page_header()

if "processed_result" not in st.session_state:
    st.session_state.processed_result = None
if "processing_error" not in st.session_state:
    st.session_state.processing_error = None
if "processing_cache" not in st.session_state:
    st.session_state.processing_cache = {}

uploaded_file, sort_active_first, process_clicked = render_controls()

if process_clicked and uploaded_file is not None:
    uploaded_bytes = uploaded_file.getvalue()
    cache_key = hashlib.sha256(uploaded_bytes + f"|sort={sort_active_first}".encode("utf-8")).hexdigest()
    with st.spinner("Processing workbook..."):
        try:
            if cache_key in st.session_state.processing_cache:
                st.session_state.processed_result = st.session_state.processing_cache[cache_key]
            else:
                st.session_state.processed_result = process_excel_upload(
                    file_name=uploaded_file.name,
                    file_bytes=uploaded_bytes,
                    sort_active_first=sort_active_first,
                )
                st.session_state.processing_cache[cache_key] = st.session_state.processed_result
            st.session_state.processing_error = None
        except Exception as exc:
            logger.exception(
                "Processing failed in Streamlit flow",
                extra={
                    "uploaded_file_name": uploaded_file.name,
                    "sort_active_first": sort_active_first,
                },
            )
            st.session_state.processed_result = None
            st.session_state.processing_error = str(exc)

if st.session_state.processing_error:
    st.error(st.session_state.processing_error)

result = st.session_state.processed_result
if result is not None:
    render_success(result)
    render_preview(result)
    clear_clicked = render_download(result)
    if clear_clicked:
        st.session_state.processed_result = None
        st.session_state.processing_error = None
        st.rerun()
