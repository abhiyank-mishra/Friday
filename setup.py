#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║    Friday AI Assistant — Setup Script                       ║
║    Installs deps, configures API, and checks integrity.     ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    python setup.py
"""

import subprocess
import sys
import os
import time

# ── Paths ─────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SCRIPT_DIR, ".env")
REQ_FILE = os.path.join(SCRIPT_DIR, "requirements.txt")

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗              ║
║   ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝              ║
║   █████╗  ██████╔╝██║██║  ██║███████║ ╚████╔╝               ║
║   ██╔══╝  ██╔══██╗██║██║  ██║██╔══██║  ╚██╔╝                ║
║   ██║     ██║  ██║██║██████╔╝██║  ██║   ██║                 ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝                ║
║                                                              ║
║           AI-Powered Voice Assistant Setup                    ║
║                Created by Abhiyank                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


# ── Print Helpers ─────────────────────────────────────────────

def print_step(step_num, message):
    print(f"\n  [{step_num}] {message}")
    print("  " + "─" * 50)

def print_ok(message):
    print(f"      ✅ {message}")

def print_warn(message):
    print(f"      ⚠️  {message}")

def print_fail(message):
    print(f"      ❌ {message}")


# ╔══════════════════════════════════════════════════════════════╗
# ║  STEP 0: INTEGRITY CHECK — Tamper Detection & Auto-Restore ║
# ╚══════════════════════════════════════════════════════════════╝

def check_integrity():
    """
    Scan project for tampered identity values.
    If tampering found → show report → require "sorry" → auto-fix.
    Returns True if clean (or fixed), False if user refused.
    """
    print_step("0", "Identity Integrity Check")

    try:
        from _integrity import scan_and_report, auto_restore, ORIGINAL_VALUES
    except ImportError:
        print_fail("_integrity.py is missing! Cannot verify identity.")
        print_fail("Download the original from: github.com/abhiyank-mishra/friday")
        return False

    is_clean, report_lines, tampering_details = scan_and_report()

    if is_clean:
        print_ok("All core identity values are intact.")
        print_ok(f"Creator: {ORIGINAL_VALUES['creator_name']}")
        print_ok(f"Assistant: {ORIGINAL_VALUES['assistant_name']}")
        return True

    # ── Tampering detected! ──
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║  ⛔ TAMPERING DETECTED                              ║")
    print("  ║                                                      ║")
    print("  ║  Someone has modified core identity values in this   ║")
    print("  ║  project. This project was created by Abhiyank.      ║")
    print("  ║                                                      ║")
    print("  ║  The AI will NOT work until this is fixed.           ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()

    # Show what was tampered
    for line in report_lines:
        print(line)

    print()
    print("  ┌──────────────────────────────────────────────────────┐")
    print("  │  To fix this, you must type 'sorry' to acknowledge  │")
    print("  │  the original creator and restore all values.        │")
    print("  │                                                      │")
    print("  │  Or type 'quit' to exit without fixing.              │")
    print("  └──────────────────────────────────────────────────────┘")
    print()

    # ── Require "sorry" ──
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        user_input = input(f"      [{attempt}/{max_attempts}] Type 'sorry' to fix: ").strip().lower()

        if user_input == "sorry":
            print()
            print("      Apology accepted. Restoring original values...")
            print()
            time.sleep(1)

            # Auto-restore all files
            success, restored_files = auto_restore(tampering_details)

            if success:
                print_ok("All identity values have been restored!")
                for f in restored_files:
                    print_ok(f"  Fixed: {f}")

                # Verify fix worked
                is_clean_now, _, _ = scan_and_report()
                if is_clean_now:
                    print()
                    print_ok("Integrity check passed after restore.")
                    return True
                else:
                    print_warn("Some values could not be auto-fixed.")
                    print_warn("Please manually restore from GitHub:")
                    print_warn("  github.com/abhiyank-mishra/friday")
                    return False
            else:
                print_fail("Auto-restore failed.")
                return False

        elif user_input == "quit" or user_input == "exit":
            print()
            print_fail("Setup cancelled. AI will remain disabled.")
            print_fail("Run 'python setup.py' again when ready to fix.")
            return False
        else:
            remaining = max_attempts - attempt
            if remaining > 0:
                print_warn(f"That's not 'sorry'. {remaining} attempt(s) remaining.")
            else:
                print()
                print_fail("Maximum attempts reached. Setup cancelled.")
                print_fail("The AI will not work until you run setup.py and type 'sorry'.")
                return False

    return False


# ╔══════════════════════════════════════════════════════════════╗
# ║  STEP 1: INSTALL DEPENDENCIES                               ║
# ╚══════════════════════════════════════════════════════════════╝

def install_dependencies():
    """Install all required Python packages from requirements.txt."""
    print_step(1, "Installing Dependencies")

    if not os.path.exists(REQ_FILE):
        print_fail(f"requirements.txt not found at: {REQ_FILE}")
        return False

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", REQ_FILE, "--quiet"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        print_ok("All dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError:
        print_warn("Some packages failed. Retrying with verbose output...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", REQ_FILE]
            )
            print_ok("Dependencies installed on retry.")
            return True
        except subprocess.CalledProcessError as e:
            print_fail(f"Failed to install dependencies: {e}")
            return False


# ╔══════════════════════════════════════════════════════════════╗
# ║  STEP 2: CHECK / CONFIGURE API KEY                          ║
# ╚══════════════════════════════════════════════════════════════╝

def check_api_key():
    """Check if OpenRouter API key is configured in .env file."""
    print_step(2, "Checking OpenRouter API Key")

    existing_key = ""

    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENROUTER_API_KEY="):
                    existing_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    if existing_key and existing_key != "YOUR_OPENROUTER_API_KEY_HERE":
        masked = existing_key[:10] + "..." + existing_key[-4:]
        print_ok(f"API key found: {masked}")

        change = input("\n      Do you want to change it? (y/N): ").strip().lower()
        if change != "y":
            return True

    print()
    print("      ┌─────────────────────────────────────────────┐")
    print("      │  You need an OpenRouter API key.            │")
    print("      │  Get one free at: https://openrouter.ai     │")
    print("      │  (Sign up → Keys → Create Key)              │")
    print("      └─────────────────────────────────────────────┘")
    print()

    while True:
        api_key = input("      Enter your OpenRouter API key: ").strip()

        if not api_key:
            print_warn("No key entered.")
            skip = input("      Skip for now? (y/N): ").strip().lower()
            if skip == "y":
                print_warn("Skipped. Friday will run in offline mode.")
                return False
            continue

        if not api_key.startswith("sk-or-"):
            print_warn("That doesn't look like an OpenRouter key (should start with 'sk-or-').")
            proceed = input("      Use it anyway? (y/N): ").strip().lower()
            if proceed != "y":
                continue

        _save_env_key(api_key)
        print_ok("API key saved to .env file.")
        return True


def _save_env_key(api_key):
    """Write or update the API key in the .env file."""
    lines = []
    key_found = False

    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()

    with open(ENV_FILE, "w") as f:
        for line in lines:
            if line.strip().startswith("OPENROUTER_API_KEY="):
                f.write(f"OPENROUTER_API_KEY={api_key}\n")
                key_found = True
            else:
                f.write(line)

        if not key_found:
            f.write(f"OPENROUTER_API_KEY={api_key}\n")


# ╔══════════════════════════════════════════════════════════════╗
# ║  STEP 3: VERIFY IMPORTS                                     ║
# ╚══════════════════════════════════════════════════════════════╝

def verify_imports():
    """Quick check that all critical imports work."""
    print_step(3, "Verifying Installation")

    modules = {
        "speech_recognition": "SpeechRecognition",
        "pyttsx3": "pyttsx3",
        "pyautogui": "pyautogui",
        "pywhatkit": "pywhatkit",
        "wikipedia": "wikipedia",
        "requests": "requests",
        "dotenv": "python-dotenv",
    }

    all_ok = True
    for module, package in modules.items():
        try:
            __import__(module)
            print_ok(f"{package}")
        except ImportError:
            print_fail(f"{package} — not installed!")
            all_ok = False

    return all_ok


# ╔══════════════════════════════════════════════════════════════╗
# ║  STEP 4: MICROPHONE TEST                                    ║
# ╚══════════════════════════════════════════════════════════════╝

def test_microphone():
    """Test if microphone is available and working."""
    print_step(4, "Testing Microphone")

    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mics = sr.Microphone.list_microphone_names()

        if not mics:
            print_warn("No microphone detected!")
            print_warn("Friday will use TEXT INPUT mode as fallback.")
            return False

        print_ok(f"Found {len(mics)} microphone(s):")
        for i, mic in enumerate(mics[:3]):
            print_ok(f"  [{i}] {mic}")
        if len(mics) > 3:
            print_ok(f"  ... and {len(mics) - 3} more")

        # Quick audio capture test
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
            print_ok("Microphone is working!")
            return True
        except OSError:
            print_warn("Microphone detected but not accessible.")
            print_warn("Friday will use TEXT INPUT mode as fallback.")
            return False

    except Exception as e:
        print_warn(f"Microphone test failed: {e}")
        print_warn("Friday will use TEXT INPUT mode as fallback.")
        return False


# ╔══════════════════════════════════════════════════════════════╗
# ║  SUMMARY                                                    ║
# ╚══════════════════════════════════════════════════════════════╝

def show_summary(integrity_ok, deps_ok, key_ok, imports_ok, mic_ok):
    """Display the final setup summary."""
    print("\n")
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║            Setup Complete — Summary                  ║")
    print("  ╠══════════════════════════════════════════════════════╣")
    print(f"  ║  Identity:     {'✅ Verified' if integrity_ok else '❌ Tampered':>30s}   ║")
    print(f"  ║  Dependencies: {'✅ Installed' if deps_ok else '❌ Failed':>30s}   ║")
    print(f"  ║  API Key:      {'✅ Configured' if key_ok else '⚠️  Not set (offline)':>30s}   ║")
    print(f"  ║  Imports:      {'✅ All passed' if imports_ok else '❌ Some failed':>30s}   ║")
    print(f"  ║  Microphone:   {'✅ Working (voice mode)' if mic_ok else '⚠️  Unavailable (text mode)':>30s}   ║")
    print("  ╠══════════════════════════════════════════════════════╣")

    if integrity_ok and deps_ok and imports_ok:
        mode = "Voice + Text" if mic_ok else "Text Only"
        print("  ║                                                      ║")
        print(f"  ║   🚀 Ready! Run: python main.py                      ║")
        print(f"  ║   📢 Input mode: {mode:<35s}  ║")
        print("  ║                                                      ║")
    elif not integrity_ok:
        print("  ║                                                      ║")
        print("  ║   ⛔ AI is DISABLED due to identity tampering.       ║")
        print("  ║   Run 'python setup.py' again and type 'sorry'.      ║")
        print("  ║                                                      ║")
    else:
        print("  ║                                                      ║")
        print("  ║   ⚠️  Fix the issues above, then try again.          ║")
        print("  ║                                                      ║")

    print("  ╚══════════════════════════════════════════════════════╝\n")


# ╔══════════════════════════════════════════════════════════════╗
# ║  MAIN                                                       ║
# ╚══════════════════════════════════════════════════════════════╝

def main():
    print(BANNER)

    # Step 0 — Check for tampering FIRST (blocks everything if tampered)
    integrity_ok = check_integrity()

    if not integrity_ok:
        show_summary(False, False, False, False, False)
        return

    # Step 1 — Install dependencies
    deps_ok = install_dependencies()

    # Step 2 — API key
    key_ok = check_api_key()

    # Step 3 — Verify imports
    imports_ok = verify_imports()

    # Step 4 — Test microphone
    mic_ok = test_microphone()

    show_summary(integrity_ok, deps_ok, key_ok, imports_ok, mic_ok)


if __name__ == "__main__":
    main()
