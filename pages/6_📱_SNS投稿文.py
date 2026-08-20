import streamlit as st
from dotenv import load_dotenv

from utils.gemini_client import generate_text
from utils.ui import render_settings_sidebar

load_dotenv()

st.set_page_config(page_title="SNS投稿文 | AIライティングツール", page_icon="📱", layout="wide")
render_settings_sidebar()

st.title("📱 SNS投稿文の作成")
st.caption("ブログ記事やお知らせの内容から、SNS向けの投稿文を生成します。")

with st.form("sns_form"):
    content = st.text_area(
        "投稿したい内容", height=200, placeholder="記事の要約や、お知らせしたい内容を入力してください"
    )
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("プラットフォーム", ["X (Twitter)", "Instagram", "LinkedIn", "Facebook"])
    with col2:
        tone = st.selectbox("トーン", ["親しみやすい", "カジュアル", "フォーマル・ビジネス", "熱量高め"])
    col3, col4 = st.columns(2)
    with col3:
        include_hashtags = st.checkbox("ハッシュタグ案を含める", value=True)
    with col4:
        num_variations = st.number_input("生成するパターン数", min_value=1, max_value=5, value=3)
    submitted = st.form_submit_button("投稿文を生成", type="primary")

if submitted:
    if not content:
        st.error("投稿したい内容を入力してください。")
    else:
        platform_limits = {
            "X (Twitter)": "140字前後に収めてください。",
            "Instagram": "改行を活かした読みやすい投稿文にしてください。",
            "LinkedIn": "ビジネスパーソン向けに、専門性を感じる文章にしてください。",
            "Facebook": "親近感のある、少し長めの文章でも構いません。",
        }
        prompt = (
            f"以下の内容をもとに、{platform}向けの投稿文を{int(num_variations)}パターン作成してください。\n"
            f"トーン: {tone}\n"
            f"{platform_limits[platform]}\n"
            f"{'関連するハッシュタグ案も各パターンに添えてください。' if include_hashtags else 'ハッシュタグは不要です。'}\n\n"
            f"内容:\n{content}"
        )
        system_instruction = (
            "あなたはSNSマーケティングの専門家です。プラットフォームの特性を踏まえ、"
            "読者の反応を得やすい投稿文を作成します。"
        )
        with st.spinner("生成中..."):
            try:
                result = generate_text(
                    prompt,
                    api_key=st.session_state.gemini_api_key,
                    model=st.session_state.gemini_model,
                    system_instruction=system_instruction,
                    temperature=1.0,
                )
                st.session_state["sns_result"] = result
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")

if "sns_result" in st.session_state:
    st.divider()
    st.subheader("生成結果")
    st.markdown(st.session_state["sns_result"])
