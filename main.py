import os
import platform
import random
import data
import pyautogui
from command import Command, print_ai
from speak import speak

pyautogui.FAILSAFE = False

# ── Input Mode Detection ──────────────────────────────────────
# Try to detect if microphone/voice input is available.
# If not, fall back to text input automatically.

MIC_AVAILABLE = False

try:
    import speech_recognition as sr
    # Test if any microphone exists
    mics = sr.Microphone.list_microphone_names()
    if mics:
        # Try opening a microphone to confirm it works
        try:
            _test_r = sr.Recognizer()
            with sr.Microphone() as _src:
                _test_r.adjust_for_ambient_noise(_src, duration=0.3)
            MIC_AVAILABLE = True
        except (OSError, AttributeError, Exception):
            MIC_AVAILABLE = False
    else:
        MIC_AVAILABLE = False
except (ImportError, OSError, AttributeError, Exception):
    MIC_AVAILABLE = False


# ── UI ────────────────────────────────────────────────────────

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    print("=" * 55)
    print("  ███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗")
    print("  ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝")
    print("  █████╗  ██████╔╝██║██║  ██║███████║ ╚████╔╝ ")
    print("  ██╔══╝  ██╔══██╗██║██║  ██║██╔══██║  ╚██╔╝  ")
    print("  ██║     ██║  ██║██║██████╔╝██║  ██║   ██║   ")
    print("  ╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ")
    print("=" * 55)
    print("  AI-Powered Voice Assistant | Created by Abhiyank")
    print("=" * 55)
    print()

    random_greeting = random.choice(data.opening)
    print_ai(random_greeting)
    speak(random_greeting)


# ── Input Methods ─────────────────────────────────────────────

def take_voice_command():
    """Capture voice input via microphone."""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print()
            print_ai(f"🎙️  Listening... ({data.user})")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=8, phrase_time_limit=15)
            try:
                query = r.recognize_google(audio, language='en-in')
                print(f"\n  🎤 {data.user}: {query}")
                return query
            except sr.UnknownValueError:
                random_confused = random.choice(data.confused)
                print_ai(random_confused)
                speak(random_confused)
                return None
            except sr.RequestError:
                print_ai("⚠️  Speech recognition service unavailable. Switching to text input.")
                return "__SWITCH_TO_TEXT__"
    except (OSError, AttributeError) as e:
        print_ai(f"⚠️  Microphone error: {e}")
        print_ai("Switching to text input mode.")
        return "__SWITCH_TO_TEXT__"


def take_text_command():
    """Take typed text input as fallback."""
    print()
    try:
        query = input(f"  ⌨️  {data.user}: ").strip()
        if not query:
            return None
        return query
    except (EOFError, KeyboardInterrupt):
        return "exit"


# ── Main Loop ─────────────────────────────────────────────────

def main():
    global MIC_AVAILABLE
    clear_screen()
    friday = Command()

    # Show input mode
    if MIC_AVAILABLE:
        print_ai("All systems online. AI Brain initialized.")
        print_ai("🎙️  Voice input detected — you can speak or type.")
        print_ai(f"    (Type 'text mode' to switch, 'voice mode' to switch back)\n")
    else:
        print_ai("All systems online. AI Brain initialized.")
        print_ai("⌨️  No microphone detected — using text input mode.")
        print_ai(f"    (Type 'voice mode' to try enabling voice)\n")

    use_voice = MIC_AVAILABLE
    voice_fail_count = 0  # Track consecutive voice failures

    while True:
        command = None

        if use_voice:
            command = take_voice_command()

            # Handle voice failure — auto-switch after 3 consecutive failures
            if command == "__SWITCH_TO_TEXT__":
                use_voice = False
                MIC_AVAILABLE = False
                print_ai("⌨️  Switched to text input mode permanently.")
                print_ai("    (Type 'voice mode' to try again)\n")
                continue
            
            if command is None:
                voice_fail_count += 1
                if voice_fail_count >= 5:
                    print_ai("⚠️  Too many voice failures. Switching to text input.")
                    print_ai("    (Type 'voice mode' to switch back)\n")
                    use_voice = False
                continue
            else:
                voice_fail_count = 0  # Reset on success
        else:
            command = take_text_command()

        if command is None:
            continue

        # ── Mode switching commands ──
        command_lower = command.lower().strip()

        if command_lower in ("text mode", "type mode", "keyboard mode"):
            use_voice = False
            print_ai("⌨️  Switched to text input mode.")
            print_ai("    (Type 'voice mode' to switch back)\n")
            continue

        if command_lower in ("voice mode", "mic mode", "speak mode"):
            if MIC_AVAILABLE:
                use_voice = True
                voice_fail_count = 0
                print_ai("🎙️  Switched to voice input mode.\n")
            else:
                # Re-test microphone
                print_ai("Testing microphone...")
                try:
                    _r = sr.Recognizer()
                    with sr.Microphone() as _s:
                        _r.adjust_for_ambient_noise(_s, duration=0.3)
                    MIC_AVAILABLE = True
                    use_voice = True
                    voice_fail_count = 0
                    print_ai("🎙️  Microphone found! Switched to voice mode.\n")
                except Exception:
                    print_ai("❌ Microphone still not available. Staying in text mode.\n")
            continue

        # ── Process command through AI ──
        friday.process(command)


if __name__ == "__main__":
    main()
