#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║    Friday AI Assistant — Setup Script                       ║
║    Run this ONCE to install dependencies and configure API  ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    python setup.py
"""

import subprocess
import sys
import os


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

ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
REQ_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")


def print_step(step_num, message):
    print(f"\n  [{step_num}] {message}")
    print("  " + "─" * 50)


def print_ok(message):
    print(f"      ✅ {message}")


def print_warn(message):
    print(f"      ⚠️  {message}")


def print_fail(message):
    print(f"      ❌ {message}")


def install_dependencies():
    """Install all required Python packages."""
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
        # Retry without --quiet to show errors
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


def check_api_key():
    """Check if OpenRouter API key is configured in .env file."""
    print_step(2, "Checking OpenRouter API Key")

    existing_key = ""

    # Read existing .env if it exists
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

    # Prompt for API key
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

        # Save to .env file
        _save_env_key(api_key)
        print_ok(f"API key saved to .env file.")
        return True


def _save_env_key(api_key):
    """Write or update the API key in the .env file."""
    lines = []
    key_found = False

    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()

    # Update existing key or add new one
    with open(ENV_FILE, "w") as f:
        for line in lines:
            if line.strip().startswith("OPENROUTER_API_KEY="):
                f.write(f"OPENROUTER_API_KEY={api_key}\n")
                key_found = True
            else:
                f.write(line)

        if not key_found:
            f.write(f"OPENROUTER_API_KEY={api_key}\n")


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


def show_summary(deps_ok, key_ok, imports_ok):
    """Display the final setup summary."""
    print("\n")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║          Setup Complete — Summary            ║")
    print("  ╠══════════════════════════════════════════════╣")
    print(f"  ║  Dependencies:  {'✅ Installed' if deps_ok else '❌ Failed':>24s}   ║")
    print(f"  ║  API Key:       {'✅ Configured' if key_ok else '⚠️  Not set (offline)':>24s}   ║")
    print(f"  ║  Imports:       {'✅ All passed' if imports_ok else '❌ Some failed':>24s}   ║")
    print("  ╠══════════════════════════════════════════════╣")

    if deps_ok and imports_ok:
        print("  ║                                              ║")
        print("  ║   🚀 Ready! Run: python main.py              ║")
        print("  ║                                              ║")
    else:
        print("  ║                                              ║")
        print("  ║   ⚠️  Fix the issues above, then try again.  ║")
        print("  ║                                              ║")

    print("  ╚══════════════════════════════════════════════╝\n")


def main():
    print(BANNER)

    deps_ok = install_dependencies()
    key_ok = check_api_key()
    imports_ok = verify_imports()

    show_summary(deps_ok, key_ok, imports_ok)


if __name__ == "__main__":
    main()
