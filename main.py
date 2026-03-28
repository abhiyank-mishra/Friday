import os
import platform
import random
import time
import data
import pyautogui
from command import Command, print_ai
from speak import speak

pyautogui.FAILSAFE = False

# ── Import speech recognition with error guidance ─────────────
try:
    import speech_recognition as sr
except ImportError:
    print("❌ SpeechRecognition is not installed.")
    print("   Run: python setup.py")
    exit(1)


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


# ── Microphone Setup ──────────────────────────────────────────

def find_working_microphone():
    """
    Try to find a working microphone.
    Tests the default mic first, then tries each available mic index.
    Returns the mic index that works, or None.
    """
    r = sr.Recognizer()

    # 1) Try default microphone (no index)
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
        print_ai("🎙️  Default microphone detected and working.")
        return None  # None means "use default"
    except (OSError, AttributeError):
        pass

    # 2) Try each available microphone by index
    try:
        mic_names = sr.Microphone.list_microphone_names()
    except (OSError, AttributeError):
        mic_names = []

    if not mic_names:
        return -1  # No mic found at all

    print_ai(f"Default mic failed. Scanning {len(mic_names)} audio devices...")

    for i, name in enumerate(mic_names):
        try:
            with sr.Microphone(device_index=i) as source:
                r.adjust_for_ambient_noise(source, duration=0.3)
            print_ai(f"🎙️  Found working mic: [{i}] {name}")
            return i
        except (OSError, AttributeError, Exception):
            continue

    return -1  # Nothing worked


def setup_microphone():
    """
    Initialize microphone with robust fallback.
    Provides clear error messages and fixes for common issues.
    """
    mic_index = find_working_microphone()

    if mic_index == -1:
        print()
        print_ai("=" * 50)
        print_ai("⚠️  NO WORKING MICROPHONE DETECTED")
        print_ai("=" * 50)
        print_ai("Common fixes:")
        print_ai("  1. Check if a microphone is plugged in")
        print_ai("  2. Run 'python setup.py' to install audio drivers")
        print_ai("  3. Windows → Settings → Privacy → Microphone → Allow")
        print_ai("  4. Right-click speaker icon → Sound Settings → Input")
        print_ai("     → Make sure a mic is selected as default")
        print_ai("=" * 50)
        print()
        print_ai("Retrying in 5 seconds...")
        time.sleep(5)

        # Retry once
        mic_index = find_working_microphone()
        if mic_index == -1:
            print_ai("❌ Still no microphone. Please fix and restart Friday.")
            print_ai("   Run 'python setup.py' for diagnostics.")
            exit(1)

    return mic_index


# ── Voice Input ───────────────────────────────────────────────

def take_command(mic_index=None):
    """
    Capture voice command with robust error handling.
    - Dynamic energy threshold for noisy environments
    - Auto-retry on transient failures
    - Timeout handling so it doesn't hang forever
    """
    r = sr.Recognizer()

    # Dynamic settings for better recognition
    r.pause_threshold = 1          # Seconds of silence to end a phrase
    r.phrase_threshold = 0.3       # Min seconds of speech to register
    r.non_speaking_duration = 0.5  # Seconds of non-speaking before phrase ends
    r.dynamic_energy_threshold = True  # Auto-adjust for ambient noise

    mic_args = {"device_index": mic_index} if mic_index is not None else {}

    try:
        with sr.Microphone(**mic_args) as source:
            print()
            print_ai(f"🎙️  Listening... ({data.user})")

            # Calibrate for ambient noise (important for noisy environments)
            r.adjust_for_ambient_noise(source, duration=0.8)

            try:
                # Listen with timeout so it doesn't hang forever
                audio = r.listen(source, timeout=10, phrase_time_limit=20)
            except sr.WaitTimeoutError:
                print_ai("🔇 No speech detected. Try again...")
                return None

        # ── Recognize speech ──
        try:
            # Primary: Google (best accuracy, needs internet)
            query = r.recognize_google(audio, language='en-in')
            print(f"\n  🎤 {data.user}: {query}")
            return query

        except sr.UnknownValueError:
            # Heard something but couldn't understand
            random_confused = random.choice(data.confused)
            print_ai(random_confused)
            speak(random_confused)
            return None

        except sr.RequestError:
            # Google API down or no internet — try offline recognition
            print_ai("⚠️  Online speech service unavailable. Checking internet...")
            try:
                # Retry with Google once more (sometimes transient)
                query = r.recognize_google(audio, language='en-in')
                print(f"\n  🎤 {data.user}: {query}")
                return query
            except Exception:
                print_ai("❌ No internet connection. Speech recognition needs internet.")
                print_ai("   Please check your connection and try again.")
                speak("I need internet for speech recognition, Sir. Please check your connection.")
                return None

    except OSError as e:
        # Microphone disconnected or access denied
        error_msg = str(e).lower()
        if "denied" in error_msg or "permission" in error_msg:
            print_ai("❌ Microphone access denied!")
            print_ai("   Go to: Windows Settings → Privacy → Microphone → Allow")
        elif "device" in error_msg or "not found" in error_msg:
            print_ai("❌ Microphone disconnected! Please reconnect and try again.")
        else:
            print_ai(f"❌ Microphone error: {e}")
        speak("I'm having trouble with the microphone, Sir.")
        time.sleep(2)
        return None

    except Exception as e:
        print_ai(f"⚠️  Unexpected error: {e}")
        time.sleep(1)
        return None


# ── Main Loop ─────────────────────────────────────────────────

def main():
    clear_screen()

    # Setup microphone (with auto-detection and retry)
    print_ai("Initializing microphone...")
    mic_index = setup_microphone()

    # Initialize AI command processor
    friday = Command()

    print_ai("All systems online. AI Brain initialized.")
    print_ai(f"🎙️  Speak your command, {data.user}...\n")

    consecutive_failures = 0

    while True:
        command = take_command(mic_index)

        if command is None:
            consecutive_failures += 1

            # After 10 consecutive failures, re-scan microphones
            if consecutive_failures >= 10:
                print_ai("⚠️  Too many failed attempts. Re-scanning microphones...")
                mic_index = find_working_microphone()
                if mic_index == -1:
                    print_ai("❌ No microphone available. Retrying in 10 seconds...")
                    time.sleep(10)
                    mic_index = find_working_microphone()
                    if mic_index == -1:
                        print_ai("❌ Microphone still unavailable. Please reconnect and restart.")
                        exit(1)
                else:
                    print_ai("🎙️  Microphone re-connected!")
                consecutive_failures = 0
            continue

        # Reset failure counter on successful input
        consecutive_failures = 0

        # Process through AI brain
        friday.process(command)


if __name__ == "__main__":
    main()
