import streamlit as st
from dotenv import load_dotenv

from utils.gemini_client import generate_text
from utils.ui import render_settings_sidebar

load_dotenv()

st.set_page_config(page_title="リライト・校正 | AIライティングツール", page_icon="✨", layout="wide")
render_settings_sidebar()

st.title("✨ リライト・校正")
st.caption("文章の誤字脱字チェック、ブラッシュアップ、トーン変換などを行います。")

source_text = st.text_area("原文", height=250, placeholder="チェック・書き直したい文章を貼り付けてください")

mode = st.selectbox(
    "モード",
    [
        "誤字脱字・文法チェック",
        "文章を洗練する（同じ意味でより良く）",
        "トーンを変える",
        "文字数を調整する",
    ],
)

target_tone = None
target_length = None
adjust_direction = None
if mode == "トーンを変える":
    target_tone = st.selectbox(
        "変更後のトーン", ["フォーマル", "カジュアル", "丁寧・ビジネス", "親しみやすい", "簡潔"]
    )
elif mode == "文字数を調整する":
    col1, col2 = st.columns(2)
    with col1:
        adjust_direction = st.radio("方向", ["短くする", "長くする"], horizontal=True)
    with col2:
        target_length = st.text_input("目安の文字数", placeholder="例: 300字程度")

if st.button("実行", type="primary"):
    if not source_text:
        st.error("原文を入力してください。")
    else:
        if mode == "誤字脱字・文法チェック":
            instruction = "誤字脱字、文法の誤り、不自然な言い回しを修正してください。修正箇所が分かるように簡単な説明も添えてください。"
        elif mode == "文章を洗練する（同じ意味でより良く）":
            instruction = "意味を変えずに、より読みやすく洗練された文章に書き直してください。"
        elif mode == "トーンを変える":
            instruction = f"文章のトーンを「{target_tone}」に変更してリライトしてください。"
        else:
            instruction = f"文章を{adjust_direction}方向で調整してください。目安の文字数: {target_length or '指定なし'}"
        prompt = f"以下の文章に対して次の指示を実行してください。\n\n指示: {instruction}\n\n文章:\n{source_text}"
        system_instruction = (
            "あなたは日本語のプロ編集者です。指示に忠実に、自然で読みやすい文章に仕上げます。"
        )
        with st.spinner("処理中..."):
            try:
                result = generate_text(
                    prompt,
                    api_key=st.session_state.gemini_api_key,
                    model=st.session_state.gemini_model,
                    system_instruction=system_instruction,
                    temperature=0.5,
                )
                st.session_state["rewrite_result"] = result
            except Exception as e:
                st.error(f"生成に失敗しました: {e}")

if "rewrite_result" in st.session_state:
    st.divider()
    st.subheader("結果")
    st.markdown(st.session_state["rewrite_result"])
