from jarvis.app import _activated_text
from jarvis.commands import handle_local_command


def test_wake_word_activation() -> None:
    assert _activated_text("Jarvis what time is it", "jarvis") == "what time is it"
    assert _activated_text("hello there", "jarvis") is None


def test_allowlisted_command() -> None:
    result = handle_local_command("date")
    assert result.handled is True
    assert result.should_exit is False


def test_unknown_command_is_not_executed() -> None:
    result = handle_local_command("delete all my files")
    assert result.handled is False

