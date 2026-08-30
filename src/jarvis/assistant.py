from __future__ import annotations

from openai import OpenAI


SYSTEM_PROMPT = """You are Jarvis, a concise and friendly Windows desktop voice assistant.
Answer in natural spoken language, normally in two or three sentences. Never claim that you
opened an app, changed the computer, or ran a command. Local actions are handled separately by
an explicit allowlist. If asked to perform a risky or unsupported computer action, explain that
you cannot do it and offer a safe alternative."""


class ConversationalAssistant:
    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._previous_response_id: str | None = None

    def reply(self, user_text: str) -> str:
        kwargs: dict[str, object] = {
            "model": self._model,
            "instructions": SYSTEM_PROMPT,
            "input": user_text,
        }
        if self._previous_response_id:
            kwargs["previous_response_id"] = self._previous_response_id
        response = self._client.responses.create(**kwargs)
        self._previous_response_id = response.id
        return response.output_text.strip() or "I could not form a response just now."

