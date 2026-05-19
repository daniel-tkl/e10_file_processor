THEME_MARKUP = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0" rel="stylesheet">
<style>
    .stApp {
        background:
            radial-gradient(circle at 10% 8%, rgba(50, 140, 230, 0.28) 0%, rgba(50, 140, 230, 0) 34%),
            radial-gradient(circle at 86% 14%, rgba(72, 186, 255, 0.2) 0%, rgba(72, 186, 255, 0) 30%),
            radial-gradient(circle at 50% 85%, rgba(29, 95, 178, 0.16) 0%, rgba(29, 95, 178, 0) 38%),
            conic-gradient(from 205deg at 52% 50%, rgba(30, 83, 156, 0.2), rgba(11, 23, 44, 0.0) 30%, rgba(36, 112, 196, 0.14) 63%, rgba(12, 26, 49, 0.0) 100%),
            linear-gradient(132deg, #050913 0%, #081225 32%, #0a1a33 52%, #071224 74%, #040913 100%) !important;
        color: #e8eef5 !important;
    }

    div[data-testid="stAppViewContainer"] {
        background-image:
            linear-gradient(rgba(125, 191, 255, 0.035) 1px, transparent 1px),
            linear-gradient(90deg, rgba(125, 191, 255, 0.035) 1px, transparent 1px);
        background-size: 28px 28px;
        background-position: 0 0;
    }

    .stApp, .stApp * {
        font-family: "Space Grotesk", "Segoe UI", sans-serif !important;
    }

    .stApp code, .stApp pre {
        font-family: "JetBrains Mono", Consolas, monospace !important;
    }

    span[data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded" !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 20px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: "liga" !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: "liga" !important;
    }

    div[data-testid="stAppViewContainer"] .block-container {
        padding-top: 2rem !important;
        max-width: 1180px !important;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"] {
        display: none !important;
    }

    .hero-shell {
        position: relative;
        margin: 0 0 2rem 0;
        padding: 1.2rem 1.4rem 1rem 1.4rem;
        border-radius: 18px;
        border: 1px solid rgba(126, 190, 255, 0.18);
        background: linear-gradient(135deg, rgba(18, 32, 52, 0.96), rgba(8, 17, 31, 0.93));
        box-shadow: 0 12px 34px rgba(0, 0, 0, 0.26);
        overflow: hidden;
    }

    .hero-shell::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            radial-gradient(circle at 15% 20%, rgba(69, 170, 255, 0.18), transparent 35%),
            linear-gradient(90deg, transparent, rgba(120, 199, 255, 0.08), transparent);
        pointer-events: none;
    }

    .hero-title {
        position: relative;
        margin: 0 !important;
        text-align: center;
        font-size: clamp(2rem, 3.8vw, 3.2rem);
        font-weight: 700 !important;
        line-height: 1.08;
        letter-spacing: 0.03em !important;
        color: #f4f9ff;
        text-shadow: 0 0 24px rgba(83, 186, 255, 0.18);
    }

    .hero-title-accent {
        background: linear-gradient(90deg, #7ed3ff 0%, #9ecbff 45%, #d7ebff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
    }

    .hero-caption {
        position: relative;
        margin: 0.55rem auto 0 auto !important;
        max-width: 760px;
        text-align: center;
        color: #b8c6d8 !important;
        font-size: 1rem;
        line-height: 1.55;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(122, 183, 238, 0.26) !important;
        border-radius: 14px !important;
        padding: 10px 12px !important;
        background: rgba(13, 25, 41, 0.9) !important;
    }

    div[data-testid="stMetricLabel"] p,
    div[data-testid="stMetricValue"] {
        color: #eaf4ff !important;
    }

    div[data-testid="stMetricLabel"] p {
        opacity: 0.92 !important;
    }

    div[data-testid="stCaptionContainer"] p,
    .stApp label,
    .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stMarkdownContainer"] p {
        color: #d8e7f7 !important;
    }

    div[data-testid="stCheckbox"] label,
    div[data-testid="stCheckbox"] label span {
        color: #e8f2ff !important;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stTextInput"] label p {
        color: #e8f2ff !important;
    }

    div[data-testid="stTextInput"] input {
        color: #f4faff !important;
        background: rgba(9, 20, 35, 0.92) !important;
        border: 1px solid rgba(132, 197, 255, 0.45) !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #9eb7d2 !important;
    }

    .upload-panel {
        margin-top: 0.4rem;
        margin-bottom: 0.65rem;
        padding: 1rem 1rem 0.85rem 1rem;
        border-radius: 16px;
        border: 1px solid rgba(126, 190, 255, 0.22);
        background: linear-gradient(160deg, rgba(17, 31, 50, 0.97), rgba(10, 20, 33, 0.95));
        box-shadow: inset 0 1px 0 rgba(201, 231, 255, 0.04), 0 10px 26px rgba(0, 0, 0, 0.22);
    }

    .upload-title {
        margin: 0;
        color: #e8f3ff;
        font-weight: 700;
        font-size: 1.05rem;
        letter-spacing: 0.01em;
    }

    .upload-copy {
        margin: 0.3rem 0 0.85rem 0;
        color: #a9bfd7;
        font-size: 0.93rem;
        line-height: 1.45;
    }

    div[data-testid="stFileUploader"] {
        margin-bottom: 0.2rem !important;
    }

    div[data-testid="stFileUploader"] section,
    div[data-testid="stFileUploaderDropzone"] {
        border: 1px dashed rgba(130, 198, 255, 0.44) !important;
        border-radius: 13px !important;
        background: rgba(10, 22, 37, 0.9) !important;
        min-height: 3.2rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-testid="stFileUploader"] section:hover,
    div[data-testid="stFileUploaderDropzone"]:hover {
        border-color: rgba(159, 216, 255, 0.9) !important;
        box-shadow: 0 0 0 2px rgba(93, 178, 255, 0.14) !important;
    }

    div[data-testid="stFileUploader"] section > div,
    div[data-testid="stFileUploaderDropzone"] > div {
        min-height: 3.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding: 0.35rem 0.75rem !important;
        gap: 0.8rem !important;
    }

    div[data-testid="stFileUploader"] section > div > *,
    div[data-testid="stFileUploaderDropzone"] > div > * {
        display: flex !important;
        align-items: center !important;
        align-self: center !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    div[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"],
    div[data-testid="stFileUploaderDropzone"] [data-testid="stBaseButton-secondary"],
    div[data-testid="stFileUploaderDropzoneInstructions"] {
        display: flex !important;
        align-items: center !important;
        align-self: center !important;
        min-height: 2.3rem !important;
    }

    div[data-testid="stFileUploader"] small,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploaderDropzone"] small,
    div[data-testid="stFileUploaderDropzone"] p {
        margin: 0 !important;
        color: #abc3db !important;
        text-align: left !important;
        line-height: 1.35 !important;
    }

    div[data-testid="stFileUploader"] button,
    div[data-testid="stFileUploaderDropzone"] button {
        background: linear-gradient(135deg, #1698ff, #2b7bff) !important;
        color: #ffffff !important;
        border: 1px solid rgba(126, 190, 255, 0.75) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 18px rgba(21, 123, 255, 0.35) !important;
        margin: 0 !important;
        height: 2.3rem !important;
        padding: 0 1rem !important;
        align-self: center !important;
        vertical-align: middle !important;
        margin-top: 4px !important;
    }

    div[data-testid="stFileUploader"] button:hover {
        background: linear-gradient(135deg, #3aa8ff, #3b88ff) !important;
        border-color: rgba(168, 216, 255, 0.95) !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(109, 168, 226, 0.25) !important;
        border-radius: 12px !important;
        background: rgba(9, 19, 33, 0.94) !important;
        overflow: hidden !important;
        color-scheme: dark !important;
    }

    div[data-testid="stDataFrame"] > div,
    div[data-testid="stDataFrame"] [role="grid"],
    div[data-testid="stDataFrame"] [data-testid="stDataFrameResizable"],
    div[data-testid="stDataFrame"] [data-testid="stDataFrameGlideDataEditor"] > div {
        background: #0c1a2d !important;
        color-scheme: dark !important;
    }

    div[data-testid="stDataFrame"] [data-testid="stDataFrameGlideDataEditor"] {
        --gdg-bg-cell: #0c1a2d !important;
        --gdg-bg-cell-medium: #102239 !important;
        --gdg-bg-header: #122740 !important;
        --gdg-bg-icon-header: #122740 !important;
        --gdg-bg-header-has-focus: #173252 !important;
        --gdg-bg-header-hovered: #173252 !important;
        --gdg-bg-cell-selected: #173252 !important;
        --gdg-bg-cell-hover: #13263f !important;
        --gdg-border-color: rgba(130, 182, 234, 0.45) !important;
        --gdg-header-font-style: 600 13px "Space Grotesk" !important;
        --gdg-font-style: 500 13px "Space Grotesk" !important;
        --gdg-color: #eaf4ff !important;
        --gdg-text-dark: #eaf4ff !important;
        --gdg-text-medium: #d8e9fb !important;
        --gdg-text-light: #c4dcf4 !important;
        --gdg-horizontal-border-color: rgba(120, 170, 220, 0.28) !important;
        --gdg-vertical-border-color: rgba(120, 170, 220, 0.2) !important;
        --gdg-header-bottom-border-color: rgba(146, 198, 247, 0.36) !important;
        --gdg-accent-color: #5ea9ff !important;
        background: #0c1a2d !important;
        color: #eaf4ff !important;
        color-scheme: dark !important;
    }

    div[data-testid="stDataFrame"] canvas {
        background: #0c1a2d !important;
    }

    div[data-testid="stDataFrame"] table,
    div[data-testid="stDataFrame"] thead,
    div[data-testid="stDataFrame"] tbody,
    div[data-testid="stDataFrame"] tr,
    div[data-testid="stDataFrame"] th,
    div[data-testid="stDataFrame"] td {
        background: #0c1a2d !important;
        color: #eaf4ff !important;
        border-color: #2a4666 !important;
    }

    div[data-testid="stDataFrame"] th {
        background: #122740 !important;
        color: #eef7ff !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"],
    div[data-testid="stDataFrame"] [role="rowheader"],
    div[data-testid="stDataFrame"] [role="gridcell"] {
        background: #0c1a2d !important;
        color: #eaf4ff !important;
        border-color: #2a4666 !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: #122740 !important;
        color: #eef7ff !important;
    }

    div[data-testid="stAlert"] {
        background: linear-gradient(135deg, rgba(16, 66, 44, 1), rgba(9, 52, 34, 1)) !important;
        border: 1px solid rgba(120, 218, 167, 0.62) !important;
        color: #eaf6ff !important;
    }

    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
        color: #f2f9ff !important;
        font-weight: 600 !important;
    }

    .controls-spacer-lg {
        height: 1.35rem;
    }

    .controls-spacer-md {
        height: 1rem;
    }

    .section-spacer-lg {
        height: 2rem;
    }

    .section-spacer-md {
        height: 1.4rem;
    }

    .selected-file-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.2rem;
        padding: 0.62rem 0.9rem;
        border-radius: 999px;
        border: 1px solid rgba(126, 190, 255, 0.26);
        background: linear-gradient(135deg, rgba(21, 42, 68, 0.95), rgba(11, 23, 38, 0.88));
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.22);
        color: #dfefff !important;
        font-size: 0.95rem;
        line-height: 1.2;
    }

    .selected-file-chip strong {
        color: #86d7ff !important;
        font-weight: 700;
    }

    .selected-file-name {
        color: #f7fbff !important;
        font-weight: 600;
        letter-spacing: 0.01em;
    }

    div[data-testid="stButton"] > button {
        border-radius: 10px !important;
        min-height: 2.35rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #e64b4b, #c93535) !important;
        color: #ffffff !important;
        border: 1px solid rgba(247, 161, 161, 0.78) !important;
        box-shadow: 0 6px 18px rgba(201, 53, 53, 0.28) !important;
    }

    div[data-testid="stButton"] > button[kind="primary"]:disabled,
    div[data-testid="stButton"] > button:disabled {
        background: linear-gradient(135deg, rgba(110, 44, 44, 0.95), rgba(92, 35, 35, 0.95)) !important;
        color: rgba(250, 226, 226, 0.92) !important;
        border: 1px solid rgba(218, 140, 140, 0.48) !important;
        box-shadow: none !important;
        opacity: 1 !important;
        cursor: not-allowed !important;
    }

    div.st-key-clear_result_button button {
        background: linear-gradient(135deg, #1a94ff, #2f78ff) !important;
        color: #ffffff !important;
        border: 1px solid rgba(150, 208, 255, 0.82) !important;
        box-shadow: 0 8px 18px rgba(24, 120, 255, 0.34) !important;
    }

    div.st-key-clear_result_button button:hover {
        background: linear-gradient(135deg, #36a6ff, #4a89ff) !important;
        border-color: rgba(190, 229, 255, 0.95) !important;
    }
</style>
"""
