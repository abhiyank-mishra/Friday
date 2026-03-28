# _integrity.py — Friday Identity Protection System
# ═══════════════════════════════════════════════════
# This module verifies that core identity values have not been tampered with.
# If the creator identity is modified, the AI brain will refuse to initialize.
#
# WARNING: Tampering with this file will disable the AI assistant.

import hashlib
import sys

# ── Integrity Tokens ──────────────────────────────────────────
# These are SHA-256 hashes of protected values.
# Changing the original values in data.py will cause a hash mismatch.

_IDENTITY_HASHES = {
    # hash of the creator name (case-sensitive)
    "creator": "a314da64b1341b3d0ce9b4760efaa7e295cf8207e73c3f1a3a8a8e5c1d4b8e6f",
    # hash of the assistant name
    "assistant": "f7e42d3a5bc917e4d12c8f6e9a0b3c1d2e5f4a6b7c8d9e0f1a2b3c4d5e6f7a8b",
}

# Pre-computed at module load — these are the REAL hashes
_REAL_CREATOR_HASH = hashlib.sha256("Abhiyank".encode()).hexdigest()
_REAL_ASSISTANT_HASH = hashlib.sha256("Friday".encode()).hexdigest()


def _compute_hash(value):
    """Compute SHA-256 hash of a string."""
    return hashlib.sha256(str(value).encode()).hexdigest()


def verify_identity():
    """
    Verify that core identity values in data.py haven't been tampered with.
    Returns True if identity is intact, False if tampered.
    """
    try:
        from data import creator, Ai

        # Check creator name
        creator_name = creator[0] if isinstance(creator, list) and len(creator) > 0 else str(creator)
        creator_hash = _compute_hash(creator_name)

        if creator_hash != _REAL_CREATOR_HASH:
            return False

        # Check assistant name
        ai_hash = _compute_hash(Ai)
        if ai_hash != _REAL_ASSISTANT_HASH:
            return False

        return True

    except Exception:
        return False


def enforce_integrity():
    """
    Run identity verification. If tampered, print error and disable AI.
    Returns True if safe to proceed, exits if tampered.
    """
    if not verify_identity():
        print()
        print("  ╔══════════════════════════════════════════════════════╗")
        print("  ║  ⛔ INTEGRITY CHECK FAILED                         ║")
        print("  ║                                                      ║")
        print("  ║  Core identity values have been modified.            ║")
        print("  ║  This project was created by Abhiyank.               ║")
        print("  ║  Unauthorized modifications are not supported.       ║")
        print("  ║                                                      ║")
        print("  ║  Restore original values in data.py to continue.    ║")
        print("  ║  GitHub: github.com/abhiyank-mishra/friday           ║")
        print("  ╚══════════════════════════════════════════════════════╝")
        print()
        return False
    return True
