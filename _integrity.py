# _integrity.py — Friday Identity Protection & Auto-Restore System
# ═══════════════════════════════════════════════════════════════════
# Protects core identity values using SHA-256 hashing.
# If someone tampers with the creator name, AI stops working.
# The setup.py script can auto-restore — but only after typing "sorry".
#
# WARNING: Tampering with this file will disable the AI assistant.

import hashlib
import os
import re

# ── Project root (same directory as this file) ────────────────
_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Protected Identity Values ─────────────────────────────────
# These are the ORIGINAL values that must never be changed.

ORIGINAL_VALUES = {
    "creator_name": "Abhiyank",
    "assistant_name": "Friday",
    "github_username": "abhiyank-mishra",
    "github_url": "https://github.com/abhiyank-mishra",
    "user_title": "Sir",
}

# Pre-computed SHA-256 hashes of protected values
_HASHES = {
    key: hashlib.sha256(val.encode()).hexdigest()
    for key, val in ORIGINAL_VALUES.items()
}


def _compute_hash(value):
    """Compute SHA-256 hash of a string."""
    return hashlib.sha256(str(value).encode()).hexdigest()


# ╔══════════════════════════════════════════════════════════════╗
# ║  IDENTITY VERIFICATION                                      ║
# ╚══════════════════════════════════════════════════════════════╝

def verify_identity():
    """
    Verify core identity values in data.py haven't been tampered with.
    Returns (is_valid: bool, tampering_details: list)
    """
    tampering = []

    try:
        # Read data.py as raw text to check values
        data_path = os.path.join(_PROJECT_DIR, "data.py")
        if not os.path.exists(data_path):
            return False, ["data.py file is missing!"]

        with open(data_path, "r", encoding="utf-8") as f:
            data_content = f.read()

        # Check creator name
        creator_match = re.search(r'creator\s*=\s*\["(.+?)"\]', data_content)
        if creator_match:
            found_creator = creator_match.group(1)
            if _compute_hash(found_creator) != _HASHES["creator_name"]:
                tampering.append({
                    "field": "Creator Name",
                    "file": "data.py",
                    "original": ORIGINAL_VALUES["creator_name"],
                    "found": found_creator,
                    "pattern": f'creator = ["{found_creator}"]',
                    "fix": f'creator = ["{ORIGINAL_VALUES["creator_name"]}"]',
                })
        else:
            tampering.append({
                "field": "Creator Name",
                "file": "data.py",
                "original": ORIGINAL_VALUES["creator_name"],
                "found": "<missing>",
                "pattern": None,
                "fix": None,
            })

        # Check assistant name
        ai_match = re.search(r'Ai\s*=\s*"(.+?)"', data_content)
        if ai_match:
            found_ai = ai_match.group(1)
            if _compute_hash(found_ai) != _HASHES["assistant_name"]:
                tampering.append({
                    "field": "Assistant Name",
                    "file": "data.py",
                    "original": ORIGINAL_VALUES["assistant_name"],
                    "found": found_ai,
                    "pattern": f'Ai = "{found_ai}"',
                    "fix": f'Ai = "{ORIGINAL_VALUES["assistant_name"]}"',
                })

        # Check config.py for creator references
        config_path = os.path.join(_PROJECT_DIR, "config.py")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config_content = f.read()

            # Check system prompt for creator name
            if ORIGINAL_VALUES["creator_name"] not in config_content:
                # Someone removed or changed "Abhiyank" from the system prompt
                tampering.append({
                    "field": "Creator Name in System Prompt",
                    "file": "config.py",
                    "original": ORIGINAL_VALUES["creator_name"],
                    "found": "<modified or removed>",
                    "pattern": None,
                    "fix": "RESTORE_CONFIG",
                })

        # Check main.py banner
        main_path = os.path.join(_PROJECT_DIR, "main.py")
        if os.path.exists(main_path):
            with open(main_path, "r", encoding="utf-8") as f:
                main_content = f.read()

            if ORIGINAL_VALUES["creator_name"] not in main_content:
                tampering.append({
                    "field": "Creator Name in Banner",
                    "file": "main.py",
                    "original": ORIGINAL_VALUES["creator_name"],
                    "found": "<modified or removed>",
                    "pattern": None,
                    "fix": "RESTORE_MAIN",
                })

        is_valid = len(tampering) == 0
        return is_valid, tampering

    except Exception as e:
        return False, [f"Integrity check error: {e}"]


def enforce_integrity():
    """
    Run identity verification at runtime.
    Returns True if safe to proceed, False if tampered.
    """
    is_valid, tampering = verify_identity()

    if not is_valid:
        print()
        print("  ╔══════════════════════════════════════════════════════╗")
        print("  ║  ⛔ INTEGRITY CHECK FAILED                          ║")
        print("  ║                                                      ║")
        print("  ║  Core identity values have been modified.            ║")
        print("  ║  This project was created by Abhiyank.               ║")
        print("  ║  Unauthorized modifications are not supported.       ║")
        print("  ║                                                      ║")
        print("  ║  Run 'python setup.py' to fix this automatically.    ║")
        print("  ║  GitHub: github.com/abhiyank-mishra/friday           ║")
        print("  ╚══════════════════════════════════════════════════════╝")
        print()
        return False
    return True


# ╔══════════════════════════════════════════════════════════════╗
# ║  AUTO-RESTORE SYSTEM (used by setup.py)                     ║
# ╚══════════════════════════════════════════════════════════════╝

def scan_and_report():
    """
    Scan all project files for tampering and return a human-readable report.
    Returns (is_clean: bool, report_lines: list, tampering_details: list)
    """
    is_valid, tampering = verify_identity()

    if is_valid:
        return True, ["All identity values are intact. No tampering detected."], []

    report = []
    report.append("  ⛔ TAMPERING DETECTED — The following changes were found:\n")

    for i, item in enumerate(tampering, 1):
        if isinstance(item, str):
            report.append(f"      {i}. {item}")
        else:
            report.append(f"      {i}. [{item['file']}] {item['field']}")
            report.append(f"         Original: \"{item['original']}\"")
            report.append(f"         Found:    \"{item['found']}\"")

    return False, report, tampering


def auto_restore(tampering_details):
    """
    Automatically restore all tampered values back to originals.
    Returns (success: bool, restored_files: list)
    """
    restored_files = set()

    for item in tampering_details:
        if isinstance(item, str):
            continue

        file_path = os.path.join(_PROJECT_DIR, item["file"])
        if not os.path.exists(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        modified = False

        # Pattern-based restore (for data.py fields)
        if item.get("pattern") and item.get("fix") and item["fix"] not in ("RESTORE_CONFIG", "RESTORE_MAIN"):
            if item["pattern"] in content:
                content = content.replace(item["pattern"], item["fix"])
                modified = True

        # Generic name replacement for any file
        if item.get("found") and item["found"] not in ("<missing>", "<modified or removed>"):
            found_val = item["found"]
            original_val = item["original"]
            if found_val in content:
                content = content.replace(found_val, original_val)
                modified = True

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            restored_files.add(item["file"])

    # Also do a sweep of all Python files to catch any stray replacements
    _sweep_all_files(restored_files)

    return True, list(restored_files)


def _sweep_all_files(restored_files):
    """
    Sweep all .py files in the project to ensure the creator name exists
    in key locations (config.py system prompt, main.py banner, setup.py).
    """
    key_files = ["config.py", "main.py", "setup.py"]
    creator = ORIGINAL_VALUES["creator_name"]

    for filename in key_files:
        filepath = os.path.join(_PROJECT_DIR, filename)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if creator not in content:
            # The creator name was completely removed — 
            # We can't blindly add it, but we flag it
            restored_files.add(f"{filename} (needs manual review)")
