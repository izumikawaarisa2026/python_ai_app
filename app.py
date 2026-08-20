import streamlit as st
from dotenv import load_dotenv

from utils.ui import render_settings_sidebar

load_dotenv()

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="wide")

render_settings_sidebar()

st.title("✍️ AIライティングツール")
st.write("個人用のAI文章作成アシスタントです。左のメニューから使いたい機能を選んでください。")

st.markdown(
    """
### 使える機能

| 機能 | 説明 |
| --- | --- |
| 📝 ブログ執筆 | テーマとキーワードからブログ記事の下書きを生成 |
| 📧 メール返信 | 受信メールと返信の要点から返信文を生成 |
| 📄 要約 | 長い文章を要約・箇条書き化 |
| ✨ リライト・校正 | 誤字脱字チェック、文章のブラッシュアップ、トーン変換 |
| 🏷️ タイトル生成 | 記事内容からタイトル・見出し案を複数生成 |
| 📱 SNS投稿文 | 記事やお知らせをSNS用の投稿文に変換 |
"""
)

st.info("初回はサイドバーでGemini APIキーを入力してください（Google AI Studioで取得できます）。")
