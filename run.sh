#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "仮想環境を作成しています..."
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --prefer-binary -r requirements.txt
else
  source .venv/bin/activate
fi

echo ""
echo "起動中... ブラウザで http://localhost:8501 を開いてください"
echo "終了するには Ctrl+C を押してください"
echo ""

streamlit run app.py
