import streamlit as st
from dotenv import load_dotenv

from utils.gemini_client import generate_text
from utils.ui import render_settings_sidebar

load_dotenv()

st.set_page_config(page_title="ブログ執筆 | AIライティングツール", page_icon="📝", layout="wide")
render_settings_sidebar()

st.title("📝 ブログ記事執筆")
st.caption("テーマやキーワードを入力すると、ブログ記事の下書きを生成します。")

with st.form("blog_form"):
    topic = st.text_input("テーマ・タイトル案", placeholder="例: 在宅勤務の生産性を上げる方法")
    keywords = st.text_input(
        "盛り込みたいキーワード（任意・カンマ区切り）",
        placeholder="例: タイムマネジメント, 集中力, ツール",
    )
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("トーン", ["親しみやすい", "フォーマル", "専門的", "カジュアル"])
    with col2:
        length = st.selectbox(
            "文字数の目安", ["短め（800字程度）", "標準（1500字程度）", "長め（3000字程度）"]
        )
    include_outline = st.checkbox("見出し構成（H2/H3）を含める", value=True)
    extra = st.text_area("追加の指示（任意）", placeholder="例: 初心者向けに、具体例を交えて")
    submitted = st.form_submit_button("記事を生成", type="primary")

if submitted:
    if not topic:
        st.error("テーマを入力してください。")
    else:
        prompt_parts = [
            f"テーマ: {topic}",
            f"キーワード: {keywords}" if keywords else "",
            f"トーン: {tone}",
            f"文字数目安: {length}",
            "見出し構成（H2/H3）を使ってMarkdown形式で書いてください。"
            if include_outline
            else "見出しなしの読み物として書いてください。",
            f"追加の指示: {extra}" if extra else "",
        ]
        prompt = "以下の条件でブログ記事を執筆してください。\n" + "\n".join(
            p for p in prompt_parts if p
        )
        system_instruction = (
            "あなたはプロのブログライターです。読者にとって分かりやすく、"
            "自然な日本語で説得力のある文章を書きます。Markdown形式で出力してください。"
        )
        with st.spinner("記事を生成中..."):
            try:
                result = generate_text(
                    prompt,
                    api_key=st.session_state.gemini_api_key,
                    model=st.session_state.gemini_model,
                    system_instruction=system_instruction,
                )
                st.session_state["blog_result"] = result
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")

if "blog_result" in st.session_state:
    st.divider()
    st.subheader("生成結果")
    st.markdown(st.session_state["blog_result"])
    st.download_button(
        "Markdownでダウンロード",
        data=st.session_state["blog_result"],
        file_name="blog_article.md",
        mime="text/markdown",
    )
