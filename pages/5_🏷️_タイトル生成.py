import streamlit as st
from dotenv import load_dotenv

from utils.gemini_client import generate_text
from utils.ui import render_settings_sidebar

load_dotenv()

st.set_page_config(page_title="タイトル生成 | AIライティングツール", page_icon="🏷️", layout="wide")
render_settings_sidebar()

st.title("🏷️ タイトル・見出し生成")
st.caption("記事の内容やテーマから、タイトル案を複数生成します。")

with st.form("title_form"):
    content = st.text_area(
        "記事の内容・テーマ", height=200, placeholder="記事の要約や内容、伝えたいポイントを入力してください"
    )
    col1, col2 = st.columns(2)
    with col1:
        num_titles = st.number_input("生成する候補数", min_value=1, max_value=15, value=5)
    with col2:
        style = st.selectbox(
            "スタイル", ["SEOを意識した検索されやすいタイトル", "キャッチーで興味を引くタイトル", "フォーマルで信頼感のあるタイトル", "短くシンプルなタイトル"]
        )
    submitted = st.form_submit_button("タイトルを生成", type="primary")

if submitted:
    if not content:
        st.error("記事の内容やテーマを入力してください。")
    else:
        prompt = (
            f"以下の内容に対して、タイトル案を{int(num_titles)}個、番号付きの箇条書きで提案してください。\n"
            f"スタイル: {style}\n\n"
            f"内容:\n{content}"
        )
        system_instruction = (
            "あなたはコンテンツマーケティングとコピーライティングの専門家です。"
            "クリックしたくなる、かつ内容を的確に表すタイトルを考えます。"
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
                st.session_state["title_result"] = result
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")

if "title_result" in st.session_state:
    st.divider()
    st.subheader("タイトル案")
    st.markdown(st.session_state["title_result"])
