import streamlit as st
from dotenv import load_dotenv

from utils.gemini_client import generate_text
from utils.ui import render_settings_sidebar

load_dotenv()

st.set_page_config(page_title="メール返信 | AIライティングツール", page_icon="📧", layout="wide")
render_settings_sidebar()

st.title("📧 メール返信文の作成")
st.caption("受け取ったメールと返信したい内容から、返信文の下書きを生成します。")

with st.form("email_form"):
    original_email = st.text_area("受信したメール本文", height=200, placeholder="相手から届いたメールを貼り付けてください")
    reply_points = st.text_area(
        "返信で伝えたいこと（要点）",
        height=120,
        placeholder="例: 提案内容に同意する、来週の火曜14時に打ち合わせ可能と伝える",
    )
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("トーン", ["丁寧・ビジネス", "フォーマル", "カジュアル", "親しみやすい"])
    with col2:
        language = st.selectbox("言語", ["日本語", "English"])
    include_greeting = st.checkbox("冒頭の挨拶・署名を含める", value=True)
    sender_name = st.text_input("差出人名（任意・署名に使用）", placeholder="例: 山田")
    submitted = st.form_submit_button("返信文を生成", type="primary")

if submitted:
    if not original_email or not reply_points:
        st.error("受信メール本文と返信の要点を入力してください。")
    else:
        prompt_parts = [
            f"受信したメール:\n{original_email}",
            f"返信で伝えたい要点:\n{reply_points}",
            f"トーン: {tone}",
            f"言語: {language}",
            "冒頭の挨拶と結びの署名を含めてください。" if include_greeting else "挨拶や署名は省略し、本文のみにしてください。",
            f"差出人名: {sender_name}" if sender_name else "",
        ]
        prompt = "以下の条件でメールの返信文を作成してください。\n\n" + "\n\n".join(
            p for p in prompt_parts if p
        )
        system_instruction = (
            "あなたはビジネスメール作成のプロです。受け取ったメールの文脈を踏まえ、"
            "自然で失礼のない返信文を作成します。件名は不要で、本文のみを出力してください。"
        )
        with st.spinner("返信文を生成中..."):
            try:
                result = generate_text(
                    prompt,
                    api_key=st.session_state.gemini_api_key,
                    model=st.session_state.gemini_model,
                    system_instruction=system_instruction,
                )
                st.session_state["email_result"] = result
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")

if "email_result" in st.session_state:
    st.divider()
    st.subheader("生成結果")
    st.text_area("返信文", value=st.session_state["email_result"], height=300)
