"""各ページで共有するサイドバー設定UI。"""
import os

import streamlit as st

MODEL_OPTIONS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3.6-flash"]


def init_settings() -> None:
    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
    if "gemini_model" not in st.session_state:
        st.session_state.gemini_model = MODEL_OPTIONS[0]


def render_settings_sidebar() -> None:
    init_settings()
    with st.sidebar:
        st.header("⚙️ 設定")
        st.session_state.gemini_api_key = st.text_input(
            "Gemini APIキー",
            value=st.session_state.gemini_api_key,
            type="password",
            help="Google AI StudioでAPIキーを発行し、貼り付けてください。",
        ).strip()
        st.session_state.gemini_model = st.selectbox(
            "使用モデル",
            MODEL_OPTIONS,
            index=MODEL_OPTIONS.index(st.session_state.gemini_model)
            if st.session_state.gemini_model in MODEL_OPTIONS
            else 0,
        )
        if not st.session_state.gemini_api_key:
            st.warning("APIキーが未設定です。")
        st.caption("APIキーは.envファイルのGEMINI_API_KEYでも設定できます。")
