# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

個人用のAIライティングツール（Streamlit製）。Google Gemini APIを使い、ブログ執筆・メール返信・要約・リライト校正・タイトル生成・SNS投稿文生成を行う。

## Commands

```bash
# Setup + run (creates .venv on first run)
./run.sh

# Manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install --prefer-binary -r requirements.txt
streamlit run app.py
```

There are no lint, test, or build scripts configured in this repo.

## Configuration

- Gemini APIキーは `.env` の `GEMINI_API_KEY`、または各ページのサイドバーで直接入力する（`.env.example` を参照）。
- `.streamlit/config.toml` で `gatherUsageStats = false` と `headless = true` を設定済み。

## Architecture

Streamlitのマルチページ機能をそのまま利用している。ページ間の共通ロジックは `utils/` にまとめ、各ページはUIとプロンプト組み立てのみを担当する。

- `app.py` — ホーム画面。機能一覧を表示するだけの静的ページで、実際の機能は持たない。
- `pages/N_<emoji>_<name>.py` — 各機能ページ（ブログ執筆・メール返信・要約・リライト校正・タイトル生成・SNS投稿文）。Streamlitの規約によりファイル名の先頭の数字がサイドバー表示順を決める。全ページが共通の構成に従う: `st.set_page_config()` → `render_settings_sidebar()` → `st.form` でユーザー入力を収集 → プロンプト文字列を組み立て → `generate_text()` を呼び出し → 結果を `st.session_state` に保存して表示・ダウンロードボタンを出す。
- `utils/gemini_client.py` — `generate_text()` 一つだけを提供する薄いラッパー。`google.genai.Client` を呼び出し、APIキー未設定時は `ValueError` を送出する。全ページはここを経由してGemini APIを呼ぶ。
- `utils/ui.py` — `render_settings_sidebar()` がサイドバーの設定UI（APIキー入力・モデル選択）を全ページ共通で描画する。`st.session_state.gemini_api_key` / `gemini_model` を初期化・保持し、各ページはこのセッション状態を読んで `generate_text()` に渡す。

新しい機能ページを追加する場合は、既存ページと同じ構成（フォーム → プロンプト組み立て → `generate_text()` → `session_state` に結果保存 → ダウンロードボタン）に合わせること。
