import streamlit as st
from dotenv import load_dotenv

from utils.gemini_client import generate_text
from utils.ui import render_settings_sidebar

load_dotenv()

st.set_page_config(page_title="要約 | AIライティングツール", page_icon="📄", layout="wide")
render_settings_sidebar()

st.title("📄 文章の要約")
st.caption("長い文章を貼り付けると、指定した粒度・形式で要約します。")

with st.form("summary_form"):
    source_text = st.text_area("要約したい文章", height=300, placeholder="ここに文章を貼り付けてください")
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.selectbox(
            "要約の長さ",
            ["一言でざっくり", "3〜5行程度", "10行程度", "詳細に（重要点を網羅）"],
        )
    with col2:
        summary_format = st.selectbox("出力形式", ["段落形式", "箇条書き"])
    submitted = st.form_submit_button("要約する", type="primary")

if submitted:
    if not source_text:
        st.error("要約したい文章を入力してください。")
    else:
        prompt = (
            "以下の文章を要約してください。\n\n"
            f"要約の長さ: {summary_length}\n"
            f"出力形式: {summary_format}\n\n"
            f"文章:\n{source_text}"
        )
        system_instruction = (
            "あなたは文章要約のプロです。原文の意図やニュアンスを損なわず、"
            "指定された長さと形式で簡潔にまとめます。"
        )
        with st.spinner("要約中..."):
            try:
                result = generate_text(
                    prompt,
                    api_key=st.session_state.gemini_api_key,
                    model=st.session_state.gemini_model,
                    system_instruction=system_instruction,
                    temperature=0.3,
                )
                st.session_state["summary_result"] = result
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")

if "summary_result" in st.session_state:
    st.divider()
    st.subheader("要約結果")
    st.markdown(st.session_state["summary_result"])
