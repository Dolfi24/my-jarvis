from __future__ import annotations

import speech_recognition as sr

from jarvis.assistant import ConversationalAssistant
from jarvis.commands import handle_local_command
from jarvis.config import load_settings
from jarvis.voice import VoiceIO


def _activated_text(transcript: str, wake_word: str) -> str | None:
    normalized = transcript.strip()
    lower = normalized.lower()
    if lower == wake_word:
        return ""
    prefix = wake_word + " "
    if lower.startswith(prefix):
        return normalized[len(prefix):].strip(" ,.!?")
    return None


def main() -> None:
    settings = load_settings()
    voice = VoiceIO(
        settings.api_key,
        settings.transcribe_model,
        settings.language,
        settings.voice_rate,
    )
    assistant = ConversationalAssistant(settings.api_key, settings.model)

    print(f"Calibrating microphone. Say '{settings.wake_word}' followed by a request.")
    voice.calibrate()
    voice.speak("Jarvis is ready.")

    while True:
        try:
            transcript = voice.listen(settings.listen_timeout, settings.phrase_time_limit)
            if not transcript:
                continue
            print(f"Heard: {transcript}")
            request = _activated_text(transcript, settings.wake_word)
            if request is None:
                continue
            if not request:
                voice.speak("Yes?")
                request = voice.listen(settings.listen_timeout, settings.phrase_time_limit)
                if not request:
                    continue

            result = handle_local_command(request)
            if result.handled:
                voice.speak(result.message)
                if result.should_exit:
                    break
                continue

            voice.speak(assistant.reply(request))
        except sr.WaitTimeoutError:
            continue
        except KeyboardInterrupt:
            voice.speak("Goodbye.")
            break
        except Exception as exc:
            print(f"Jarvis error: {exc}")
            voice.speak("Something went wrong. Check the console for details.")

