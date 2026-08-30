from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str
    transcribe_model: str
    wake_word: str
    language: str
    voice_rate: int
    listen_timeout: float
    phrase_time_limit: float


def load_settings() -> Settings:
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env.local")
    load_dotenv(root / ".env")
    # Codex may provision the key one level above the exported project directory.
    load_dotenv(root.parents[1] / ".env.local")

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env.local.")

    return Settings(
        api_key=api_key,
        model=os.getenv("JARVIS_MODEL", "gpt-5-mini"),
        transcribe_model=os.getenv("JARVIS_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"),
        wake_word=os.getenv("JARVIS_WAKE_WORD", "jarvis").strip().lower(),
        language=os.getenv("JARVIS_LANGUAGE", "en"),
        voice_rate=int(os.getenv("JARVIS_VOICE_RATE", "185")),
        listen_timeout=float(os.getenv("JARVIS_LISTEN_TIMEOUT", "5")),
        phrase_time_limit=float(os.getenv("JARVIS_PHRASE_TIME_LIMIT", "12")),
    )
