# Jarvis Voice Assistant

A Windows desktop voice assistant with a wake-word flow, microphone transcription,
offline text-to-speech, OpenAI-powered conversation, and a deliberately small local-command
allowlist. Jarvis does **not** expose a general shell or execute arbitrary model output.

## What it can do

- Activate on `Jarvis ...` or wait for a follow-up after hearing only `Jarvis`
- Answer conversational questions using the OpenAI Responses API
- Tell the time and date
- Open the browser, Calculator, Notepad, Paint, or File Explorer
- Search the web in your default browser
- Report basic Windows, CPU, and memory information
- Exit when you say `Jarvis, goodbye`

## Windows installation

1. Install 64-bit Python 3.11 or newer from https://www.python.org/downloads/windows/.
   During installation, enable **Add Python to PATH**.
2. Open PowerShell in this folder.
3. If Windows blocks local scripts for this one window, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   ```

4. Run the installer:

   ```powershell
   .\setup.ps1
   ```

5. Open `.env.local` and replace `replace_me` with your OpenAI API key. Never commit this file.
   In the Codex-generated copy, the securely provisioned workspace key is also detected
   automatically, so you can start without copying the secret.
6. Start Jarvis:

   ```powershell
   .\run.ps1
   ```

Say: `Jarvis, what time is it?`, `Jarvis, open calculator`, or
`Jarvis, search for weather in Johannesburg`.

## Configuration

Copy `.env.example` to `.env.local` if setup did not create it. Available settings:

- `OPENAI_API_KEY` — required
- `JARVIS_MODEL` — conversation model; defaults to `gpt-5-mini`
- `JARVIS_TRANSCRIBE_MODEL` — defaults to `gpt-4o-mini-transcribe`
- `JARVIS_WAKE_WORD` — defaults to `jarvis`
- `JARVIS_LANGUAGE` — ISO language code, defaults to `en`
- `JARVIS_VOICE_RATE` — offline speech rate
- `JARVIS_LISTEN_TIMEOUT` and `JARVIS_PHRASE_TIME_LIMIT` — microphone timing

## Safety design

Local actions are implemented in `src/jarvis/commands.py` and matched against an explicit
allowlist. The language model cannot add commands, choose executables, or pass arguments to a
shell. Add new actions by creating another narrowly scoped handler and validating every input.

## Troubleshooting

- **No microphone found:** select a default input device in Windows Settings > System > Sound.
- **PyAudio installation fails:** update pip, confirm you installed 64-bit Python, then rerun
  `setup.ps1`. The supplied SpeechRecognition audio extra installs the Windows dependency.
- **Jarvis hears itself:** use headphones or lower the speaker volume.
- **API error:** confirm `.env.local` contains a valid key and that the project has API billing.
- **Wrong language:** set `JARVIS_LANGUAGE`, for example `en`, `af`, or `zu`.

## Development checks

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest
```

OpenAI speech input uses the audio transcription API, while conversational replies use the
Responses API. See the official OpenAI [Audio API reference](https://developers.openai.com/api/reference/resources/audio)
and [Responses API reference](https://developers.openai.com/api/reference/resources/responses).
