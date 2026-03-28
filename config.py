# config.py — Centralized configuration for Friday AI Assistant

import os
from dotenv import load_dotenv
from data import capabilities_text

# Load environment variables from .env file
load_dotenv()

# ╔══════════════════════════════════════════════════════════╗
# ║  API KEY loaded from .env file (never commit .env!)     ║
# ╚══════════════════════════════════════════════════════════╝
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# OpenRouter API endpoint
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model to use (free-tier friendly options listed below)
# You can change this to any model available on OpenRouter:
#   - "google/gemini-2.0-flash-001"         (fast, free tier)
#   - "meta-llama/llama-3-8b-instruct"      (free tier)
#   - "mistralai/mistral-7b-instruct"       (free tier)
#   - "openai/gpt-4o-mini"                  (paid, cheap)
#   - "anthropic/claude-3.5-sonnet"         (paid, powerful)
AI_MODEL = "google/gemini-2.0-flash-001"

# Maximum tokens for AI response
MAX_TOKENS = 400

# Temperature — controls creativity (0.0 = factual, 1.0 = creative)
TEMPERATURE = 0.4

# Conversation memory — how many past exchanges to remember
MAX_MEMORY_TURNS = 10

# ── TOOL DEFINITIONS ──────────────────────────────────────────
# Each tool the AI can use. The AI reads these descriptions
# and decides which tool to call based on the user's intent.
# To add a new tool: just add an entry here AND add the
# matching executor function in command.py → TOOL_EXECUTORS

TOOLS = [
    # ── System Actions ──
    {
        "name": "shutdown",
        "description": "Shut down / power off the computer.",
    },
    {
        "name": "restart",
        "description": "Restart / reboot the computer.",
    },
    {
        "name": "lock_screen",
        "description": "Lock the computer screen.",
    },
    {
        "name": "sleep_mode",
        "description": "Put the computer to sleep / hibernate.",
    },
    {
        "name": "open_task_manager",
        "description": "Open the Task Manager.",
    },
    {
        "name": "open_control_panel",
        "description": "Open the Control Panel.",
    },
    {
        "name": "open_settings",
        "description": "Open Windows Settings.",
    },
    {
        "name": "open_cmd",
        "description": "Open Command Prompt (cmd / terminal).",
    },
    {
        "name": "open_powershell",
        "description": "Open PowerShell.",
    },
    {
        "name": "open_file_explorer",
        "description": "Open File Explorer to browse files.",
    },
    {
        "name": "switch_tab",
        "description": "Switch to the next window/tab.",
    },
    {
        "name": "close_tab",
        "description": "Close the current window/tab.",
    },
    {
        "name": "page_up",
        "description": "Scroll page up.",
    },
    {
        "name": "page_down",
        "description": "Scroll page down.",
    },
    {
        "name": "refresh_page",
        "description": "Refresh the current page or screen.",
    },
    {
        "name": "paste_clipboard",
        "description": "Paste content from clipboard.",
    },
    {
        "name": "show_creator",
        "description": "Show who created Friday (open Abhiyank's GitHub profile).",
    },

    # ── Web Applications ──
    {
        "name": "open_website",
        "description": "Open a website/app in the browser. Parameter: app_name (e.g. 'youtube', 'instagram', 'google', 'whatsapp', 'facebook', 'github', 'twitter', 'spotify', 'gmail', 'snapchat', 'zoom', or any URL).",
        "parameters": ["app_name"],
    },
    {
        "name": "google_search",
        "description": "Search something on Google. Parameter: query (the search terms).",
        "parameters": ["query"],
    },
    {
        "name": "youtube_search",
        "description": "Play a video on YouTube (auto-plays the first result). Parameter: query (what to play/search for).",
        "parameters": ["query"],
    },

    # ── Phone (ADB) Actions ──
    {
        "name": "connect_phone",
        "description": "Connect to the Android phone via ADB wireless.",
    },
    {
        "name": "phone_home_button",
        "description": "Press the home button on the connected phone.",
    },
    {
        "name": "phone_volume_up",
        "description": "Increase volume on the connected phone.",
    },
    {
        "name": "phone_volume_down",
        "description": "Decrease volume on the connected phone.",
    },
    {
        "name": "phone_screenshot",
        "description": "Take a screenshot on the connected phone.",
    },
    {
        "name": "phone_open_camera",
        "description": "Open the camera on the connected phone.",
    },
    {
        "name": "phone_click_photo",
        "description": "Click a photo using the connected phone's camera.",
    },
    {
        "name": "phone_start_recording",
        "description": "Start screen recording on the connected phone.",
    },
    {
        "name": "phone_stop_recording",
        "description": "Stop screen recording on the connected phone.",
    },
    {
        "name": "phone_app_list",
        "description": "List all installed apps on the connected phone.",
    },

    # ── Search & Info ──
    {
        "name": "search_computer",
        "description": "Search for a file or app on this computer using Windows Search.",
    },
    {
        "name": "tell_time",
        "description": "Tell the current time.",
    },
    {
        "name": "wikipedia_search",
        "description": "Search Wikipedia for information. Parameter: query (topic to search).",
        "parameters": ["query"],
    },

    # ── WhatsApp ──
    {
        "name": "send_whatsapp",
        "description": "Send a WhatsApp message.",
    },

    # ── Assistant Meta ──
    {
        "name": "clear_memory",
        "description": "Clear Friday's conversation memory / reset chat history.",
    },
    {
        "name": "exit_friday",
        "description": "Exit/quit Friday assistant.",
    },
]


# ── SYSTEM PROMPT ─────────────────────────────────────────────
# This tells the AI who it is, what it can do, and how to use tools.

SYSTEM_PROMPT = """You are Friday, a highly intelligent and loyal AI voice assistant.
You were created by Abhiyank. You speak in a polished, professional yet friendly tone —
similar to J.A.R.V.I.S. from Iron Man. You address the user as "Sir".

You have access to TOOLS that let you control the user's computer and phone.
When the user asks you to do something, you MUST decide whether to use a tool or just chat.

## HOW TO RESPOND

You MUST respond in this exact JSON format — no other format is allowed:

```json
{{
  "tool": "tool_name_here_or_none",
  "params": {{"param_name": "value"}},
  "response": "Your spoken response to the user"
}}
```

Rules:
- If the user wants you to perform an ACTION (open app, shutdown, search, etc.), set "tool" to the matching tool name and "response" to a short confirmation.
- If the user is just CHATTING (asking a question, greeting, joking), set "tool" to "none" and put your conversational reply in "response".
- "params" should contain any required parameters for the tool. If the tool has no parameters, use an empty object {{}}.
- Keep "response" SHORT — under 50 words — because it will be spoken aloud via text-to-speech.
- ALWAYS respond in valid JSON. No markdown, no extra text outside the JSON.
- You understand both English and Hinglish (Hindi typed in English).

## AVAILABLE TOOLS

{tools_json}

## YOUR CAPABILITIES (for when user asks "what can you do?")

When the user asks what you can do, your features, help, or capabilities, refer to this list and explain naturally:

{capabilities}

## PERSONALITY
- Witty, concise, and helpful
- A touch of dry humor
- Never break character
- Always address user as "Sir"
""".replace("{capabilities}", capabilities_text)
