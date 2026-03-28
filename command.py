# command.py — Tool executor for Friday AI Assistant
# The AI decides WHICH tool to use. This file EXECUTES the tool.
# No keyword matching here — just pure tool execution functions.

from data import Ai, user, opening
from speak import speak
from ai_brain import AIBrain
import random
import os
from os import getcwd
import datetime
import sys
import pywhatkit
import subprocess
import time
import webbrowser
import wikipedia
import speech_recognition as sr
import pyautogui
import data

pyautogui.FAILSAFE = False


# ── Helper ────────────────────────────────────────────────────

def print_ai(message):
    """Formatted output with Friday's name."""
    print(f"{Ai}: {message}")


# ── Website URL Map ───────────────────────────────────────────

WEBSITE_MAP = {
    "instagram": "https://www.instagram.com/",
    "whatsapp": "https://web.whatsapp.com/",
    "facebook": "https://www.facebook.com/",
    "github": "https://github.com/",
    "youtube": "https://www.youtube.com/",
    "google": "https://www.google.com/",
    "twitter": "https://www.x.com/",
    "x": "https://www.x.com/",
    "spotify": "https://open.spotify.com/",
    "gmail": "https://mail.google.com/",
    "snapchat": "https://www.snapchat.com/",
    "zoom": "https://zoom.us/",
    "reddit": "https://www.reddit.com/",
    "linkedin": "https://www.linkedin.com/",
    "chatgpt": "https://chat.openai.com/",
    "amazon": "https://www.amazon.in/",
    "netflix": "https://www.netflix.com/",
}


# ╔══════════════════════════════════════════════════════════════╗
# ║  TOOL EXECUTOR FUNCTIONS                                    ║
# ║  Each function matches a tool name from config.py TOOLS.    ║
# ║  To add a new tool: add it in config.py AND add a function  ║
# ║  here with the same name.                                   ║
# ╚══════════════════════════════════════════════════════════════╝

def tool_shutdown(params):
    os.system("shutdown /s /t 1")

def tool_restart(params):
    os.system("shutdown /r /t 1")

def tool_lock_screen(params):
    pyautogui.hotkey('win', 'l')

def tool_sleep_mode(params):
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def tool_open_task_manager(params):
    pyautogui.hotkey('win', 'r')
    time.sleep(1)
    pyautogui.write("taskmgr")
    pyautogui.press('enter')

def tool_open_control_panel(params):
    pyautogui.hotkey('win', 'r')
    time.sleep(1)
    pyautogui.write("control")
    pyautogui.press('enter')

def tool_open_settings(params):
    pyautogui.hotkey('win', 'i')

def tool_open_cmd(params):
    pyautogui.hotkey('win', 'r')
    time.sleep(0.5)
    pyautogui.write("cmd")
    pyautogui.press('enter')

def tool_open_powershell(params):
    pyautogui.hotkey('win', 'r')
    time.sleep(0.5)
    pyautogui.write("powershell")
    pyautogui.press('enter')

def tool_open_file_explorer(params):
    pyautogui.hotkey('win', 'e')

def tool_switch_tab(params):
    pyautogui.hotkey('alt', 'esc')

def tool_close_tab(params):
    pyautogui.hotkey('alt', 'f4')

def tool_page_up(params):
    pyautogui.hotkey('ralt', 'pgup')

def tool_page_down(params):
    pyautogui.hotkey('ralt', 'pgdn')

def tool_refresh_page(params):
    pyautogui.hotkey('win', 'ctrl', 'shift', 'b')

def tool_paste_clipboard(params):
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

def tool_show_creator(params):
    webbrowser.open('https://github.com/abhiyank-mishra')

def tool_open_website(params):
    app_name = params.get("app_name", "").lower().strip()
    url = WEBSITE_MAP.get(app_name)
    if url:
        webbrowser.open(url)
    elif app_name.startswith("http"):
        webbrowser.open(app_name)
    else:
        # Try as a direct URL
        webbrowser.open(f"https://www.{app_name}.com/")

def tool_google_search(params):
    query = params.get("query", "")
    if query:
        webbrowser.open(f"https://www.google.com/search?q={query}")

def tool_youtube_search(params):
    query = params.get("query", "")
    if query:
        try:
            pywhatkit.playonyt(query)  # Auto-plays the first YouTube result
        except Exception:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def tool_connect_phone(params):
    os.system("adb connect 192.168.29.193:5555")

def tool_phone_home_button(params):
    os.system("adb shell input keyevent 3")

def tool_phone_volume_up(params):
    os.system("adb shell input keyevent 24")

def tool_phone_volume_down(params):
    os.system("adb shell input keyevent 25")

def tool_phone_screenshot(params):
    os.system("adb shell screencap -p /sdcard/screenshot.png")
    destination = rf"{getcwd()}\phone\screenrecord\screenshot.png"
    os.system(f'adb pull /sdcard/screenshot.png "{destination}"')

def tool_phone_open_camera(params):
    os.system("adb shell am start -a android.media.action.IMAGE_CAPTURE")

def tool_phone_click_photo(params):
    os.system("adb shell am start -a android.media.action.IMAGE_CAPTURE")
    time.sleep(2)
    os.system("adb shell input keyevent 27")

def tool_phone_start_recording(params):
    duration = 20
    process = subprocess.Popen("adb shell screenrecord /sdcard/video.mp4", shell=True)
    for remaining in range(duration, 0, -1):
        print(f"\r{Ai}: Recording... {remaining} seconds remaining", end="")
        time.sleep(1)
    print()
    process.terminate()
    destination = rf"{getcwd()}\phone\screenrecord\video.mp4"
    os.system(f'adb pull /sdcard/video.mp4 "{destination}" --no-progress')

def tool_phone_stop_recording(params):
    os.system('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED --es files "file:///sdcard/video.mp4"')
    destination = rf"{getcwd()}\phone\screenrecord\video.mp4"
    os.system(f'adb pull /sdcard/video.mp4 "{destination}"')

def tool_phone_app_list(params):
    result = subprocess.run(
        ["adb", "shell", "pm", "list", "packages", "-3"],
        capture_output=True, text=True
    )
    app_list = result.stdout.splitlines()
    formatted = [app.replace("package:", "").split('.')[-1].capitalize() for app in app_list]
    print_ai(f"Installed apps on your phone, {user}:")
    for app in formatted:
        print_ai(f"  • {app}")

def tool_search_computer(params):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(f"What should I find, {user}?")
        print_ai(f"What should I find, {user}?")
        try:
            audio = recognizer.listen(source, timeout=5)
            search_term = recognizer.recognize_google(audio)
            print_ai(f"Heard: {search_term}")
            pyautogui.hotkey('win', 's')
            time.sleep(1)
            pyautogui.write(search_term)
        except sr.UnknownValueError:
            speak(f"I didn't catch that, {user}.")
        except sr.RequestError:
            speak(f"Sorry, speech service unavailable.")

def tool_tell_time(params):
    # Time is already in the AI response, but we can also show it
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    print_ai(f"Current time: {current_time}")

def tool_wikipedia_search(params):
    query = params.get("query", "")
    if query:
        try:
            summary = wikipedia.summary(query, sentences=2)
            print_ai(f"Wikipedia: {summary}")
            speak(summary)
        except Exception:
            speak("Sorry, I couldn't find that on Wikipedia.")

def tool_send_whatsapp(params):
    pywhatkit.sendwhatmsg("+91987654321", "Hello, how are you?")

def tool_clear_memory(params):
    # Handled in Command class directly
    pass

def tool_exit_friday(params):
    # Handled in Command class directly
    pass


# ── TOOL REGISTRY ─────────────────────────────────────────────
# Maps tool names (from config.py) to executor functions above.

TOOL_EXECUTORS = {
    "shutdown": tool_shutdown,
    "restart": tool_restart,
    "lock_screen": tool_lock_screen,
    "sleep_mode": tool_sleep_mode,
    "open_task_manager": tool_open_task_manager,
    "open_control_panel": tool_open_control_panel,
    "open_settings": tool_open_settings,
    "open_cmd": tool_open_cmd,
    "open_powershell": tool_open_powershell,
    "open_file_explorer": tool_open_file_explorer,
    "switch_tab": tool_switch_tab,
    "close_tab": tool_close_tab,
    "page_up": tool_page_up,
    "page_down": tool_page_down,
    "refresh_page": tool_refresh_page,
    "paste_clipboard": tool_paste_clipboard,
    "show_creator": tool_show_creator,
    "open_website": tool_open_website,
    "google_search": tool_google_search,
    "youtube_search": tool_youtube_search,
    "connect_phone": tool_connect_phone,
    "phone_home_button": tool_phone_home_button,
    "phone_volume_up": tool_phone_volume_up,
    "phone_volume_down": tool_phone_volume_down,
    "phone_screenshot": tool_phone_screenshot,
    "phone_open_camera": tool_phone_open_camera,
    "phone_click_photo": tool_phone_click_photo,
    "phone_start_recording": tool_phone_start_recording,
    "phone_stop_recording": tool_phone_stop_recording,
    "phone_app_list": tool_phone_app_list,
    "search_computer": tool_search_computer,
    "tell_time": tool_tell_time,
    "wikipedia_search": tool_wikipedia_search,
    "send_whatsapp": tool_send_whatsapp,
    "clear_memory": tool_clear_memory,
    "exit_friday": tool_exit_friday,
}


# ╔══════════════════════════════════════════════════════════════╗
# ║  COMMAND CLASS — AI-Driven Tool Orchestrator                ║
# ╚══════════════════════════════════════════════════════════════╝

class Command:
    def __init__(self):
        self.ai = AIBrain()

    def process(self, user_command):
        """
        Main entry point. Flow:
        1. Send user's voice command to AI
        2. AI decides: tool + response
        3. Execute the tool (if any)
        4. Speak the AI's response
        """
        # Ask the AI brain what to do
        print_ai("Thinking...")
        result = self.ai.think(user_command)

        if result is None:
            # AI is offline — use offline fallback
            self._offline_fallback(user_command)
            return

        tool_name = result.get("tool", "none")
        params = result.get("params", {})
        response = result.get("response", "I'm not sure how to respond to that, Sir.")

        # ── Execute the tool if AI chose one ──
        if tool_name and tool_name != "none":
            # Special cases handled here
            if tool_name == "clear_memory":
                msg = self.ai.clear_memory()
                self._respond(user_command, msg)
                return
            
            if tool_name == "exit_friday":
                self._respond(user_command, response)
                sys.exit()

            # Look up and execute the tool
            executor = TOOL_EXECUTORS.get(tool_name)
            if executor:
                print_ai(f"[Tool: {tool_name}]")
                try:
                    executor(params)
                except Exception as e:
                    print_ai(f"[Tool Error: {e}]")
            else:
                print_ai(f"[Unknown tool: {tool_name}]")

        # ── Speak the AI's response ──
        self._respond(user_command, response)

    def _respond(self, command, message):
        """Speak, print, and log the response."""
        speak(message)
        print_ai(message)
        self.log_chat(f"You: {command}\nFriday: {message}")

    def _offline_fallback(self, command):
        """
        When AI is offline, use basic keyword matching as a fallback.
        This keeps Friday functional even without an API key.
        """
        command_lower = command.lower()
        
        # Basic greetings
        if "hello" in command_lower or "hi" in command_lower:
            self._respond(command, random.choice(opening))
            return
        
        # Time
        if "time" in command_lower:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self._respond(command, f"The current time is {current_time}, {user}.")
            return
        
        # Exit
        if "exit" in command_lower or "goodbye" in command_lower or "good night" in command_lower:
            self._respond(command, random.choice(data.exiting))
            sys.exit()
        
        # What can you do
        if "what can you do" in command_lower or "help" in command_lower:
            capabilities_msg = "I can control your computer, open apps, search the web, control your phone, and chat with you. But my AI brain is offline right now — set your API key in config.py to unlock my full potential, Sir."
            self._respond(command, capabilities_msg)
            return
        
        # Default
        self._respond(command, random.choice(data.default_responses))

    def log_chat(self, message):
        """Append to chat log file."""
        try:
            with open('chat.txt', 'a') as file:
                file.write(message + '\n')
        except Exception:
            pass
