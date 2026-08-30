from __future__ import annotations

import tempfile
from pathlib import Path

import pyttsx3
import speech_recognition as sr
from openai import OpenAI


class VoiceIO:
    def __init__(self, api_key: str, transcribe_model: str, language: str, rate: int) -> None:
        self._client = OpenAI(api_key=api_key)
        self._transcribe_model = transcribe_model
        self._language = language
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._engine = pyttsx3.init()
        self._engine.setProperty("rate", rate)

    def calibrate(self) -> None:
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=1)

    def listen(self, timeout: float, phrase_time_limit: float) -> str:
        with self._microphone as source:
            audio = self._recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        wav_bytes = audio.get_wav_data()
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp:
                temp.write(wav_bytes)
                temp_path = Path(temp.name)
            with temp_path.open("rb") as audio_file:
                transcript = self._client.audio.transcriptions.create(
                    model=self._transcribe_model,
                    file=audio_file,
                    language=self._language,
                )
            return transcript.text.strip()
        finally:
            if temp_path:
                temp_path.unlink(missing_ok=True)

    def speak(self, text: str) -> None:
        print(f"Jarvis: {text}")
        self._engine.say(text)
        self._engine.runAndWait()

