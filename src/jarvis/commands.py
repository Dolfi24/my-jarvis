from __future__ import annotations

import datetime as dt
import platform
import shutil
import subprocess
import urllib.parse
import webbrowser
from dataclasses import dataclass

import psutil


@dataclass(frozen=True)
class CommandResult:
    handled: bool
    message: str = ""
    should_exit: bool = False


APP_ALLOWLIST = {
    "calculator": ["calc.exe"],
    "calc": ["calc.exe"],
    "notepad": ["notepad.exe"],
    "paint": ["mspaint.exe"],
    "file explorer": ["explorer.exe"],
    "explorer": ["explorer.exe"],
}


def _open_app(name: str) -> CommandResult:
    command = APP_ALLOWLIST.get(name)
    if not command:
        return CommandResult(False)
    executable = shutil.which(command[0]) or command[0]
    subprocess.Popen([executable], shell=False)
    return CommandResult(True, f"Opening {name}.")


def handle_local_command(text: str) -> CommandResult:
    command = " ".join(text.lower().strip().split())

    if command in {"quit", "exit", "goodbye", "stop listening"}:
        return CommandResult(True, "Goodbye.", should_exit=True)

    if command in {"what time is it", "tell me the time", "time"}:
        return CommandResult(True, f"It is {dt.datetime.now():%I:%M %p}.")

    if command in {"what is the date", "tell me the date", "date"}:
        return CommandResult(True, f"Today is {dt.datetime.now():%A, %d %B %Y}.")

    if command.startswith("search for ") or command.startswith("web search "):
        query = command.split(" ", 2)[2].strip()
        if not query:
            return CommandResult(True, "Tell me what you want to search for.")
        url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
        webbrowser.open(url)
        return CommandResult(True, f"Searching the web for {query}.")

    if command in {"open browser", "open the browser"}:
        webbrowser.open("https://www.google.com")
        return CommandResult(True, "Opening your browser.")

    if command.startswith("open "):
        return _open_app(command.removeprefix("open ").strip())

    if command in {"system info", "system information", "computer status"}:
        memory = psutil.virtual_memory()
        return CommandResult(
            True,
            f"This is {platform.system()} {platform.release()}. "
            f"CPU usage is {psutil.cpu_percent(interval=0.25):.0f} percent and "
            f"memory usage is {memory.percent:.0f} percent.",
        )

    return CommandResult(False)

