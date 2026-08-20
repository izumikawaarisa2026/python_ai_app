"""Gemini APIとの通信をまとめたモジュール。"""
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-2.5-flash"


def generate_text(
    prompt: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    system_instruction: str | None = None,
    temperature: float = 0.9,
) -> str:
    """Geminiにプロンプトを送り、生成されたテキストを返す。"""
    if not api_key:
        raise ValueError("Gemini APIキーが設定されていません。サイドバーから入力してください。")
    try:
        api_key.encode("ascii")
    except UnicodeEncodeError as e:
        raise ValueError(
            "Gemini APIキーに日本語や全角文字などの不正な文字が含まれています。"
            "サイドバーのAPIキー欄を空にして、Google AI Studioで発行したキーだけを貼り直してください。"
        ) from e

    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    return (response.text or "").strip()
