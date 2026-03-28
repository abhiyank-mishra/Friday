# data.py — Friday's personality data, response templates, and capabilities catalog

Ai = "Friday"
user = "Sir"


# ── CAPABILITIES CATALOG ──────────────────────────────────────
# This is the master list of everything Friday can do.
# The AI reads this to know its own features and explain them to the user.

capabilities = {
    "🖥️ System Control": [
        "Shut down, restart, lock, or put your computer to sleep",
        "Open Task Manager, Control Panel, Settings, File Explorer",
        "Open Command Prompt (CMD) or PowerShell",
        "Refresh the current page or screen",
        "Switch between tabs/windows or close the current one",
        "Scroll pages up and down",
        "Paste from clipboard",
    ],
    "🌐 Web & Apps": [
        "Open any website — Instagram, YouTube, Google, WhatsApp, Facebook, GitHub, Twitter/X, Spotify, Gmail, Snapchat, Zoom, and more",
        "Search anything on Google",
        "Search or play videos on YouTube",
        "Search Wikipedia for information on any topic",
    ],
    "📱 Phone Control (via ADB)": [
        "Connect to your Android phone wirelessly",
        "Press the home button on your phone",
        "Increase or decrease phone volume",
        "Take a screenshot on your phone",
        "Open the camera and click photos remotely",
        "Start and stop screen recording on your phone",
        "List all installed apps on your phone",
    ],
    "💬 WhatsApp": [
        "Send messages on WhatsApp",
    ],
    "🤖 AI-Powered Chat": [
        "Answer any general knowledge question using AI",
        "Have natural conversations in English or Hinglish",
        "Remember context from previous messages in the same session",
        "Explain what I can do when asked",
        "Tell jokes, give advice, and chat casually",
    ],
    "🕐 Utility": [
        "Tell the current time",
        "Search for files or apps on your computer",
        "Show who created me (Abhiyank — GitHub profile)",
    ],
    "🧠 Memory Management": [
        "Clear my conversation memory on command",
        "Check how many conversation exchanges are stored",
    ],
}

# Build a flat text version for the AI system prompt
capabilities_text = ""
for category, features in capabilities.items():
    capabilities_text += f"\n{category}:\n"
    for feature in features:
        capabilities_text += f"  - {feature}\n"


# ── PERSONALITY RESPONSES ─────────────────────────────────────

opening = [
    "Hello, I'm Friday. AI systems are online.",
    "Friday here, fully charged and ready to assist.",
    "Hello Sir, How can I assist you today?",
    "Hello Sir, What can I do for you?",
    "Glad to see you Sir! All systems operational.",
    "Good to have you back, Sir. What's on the agenda?",
]  

confused = [
    "Say that again please..",
    "I don't get it Sir..",
    "Ohh I didn't hear that..",
    "Excuse me Sir..",
    "Repeat that again Sir..",
    "Could you speak a bit clearer, Sir?",
]

exiting = [
    "Goodbye Sir! Have a Great Day.",
    "See you later Sir..",
    "Take care Sir!",
    "Until next time Sir!",
    "Signing off, Sir. Stay sharp.",
]

help_commands = [
    "You can ask me to search for files, run programs, or answer questions.",
    "I'm here to assist you with your daily tasks, just ask!",
    "Need help? Just say what you need assistance with.",
    "I can also answer general questions using AI, Sir.",
]

acknowledgments = [
    "Got it, Sir!",
    "Sure thing, Sir!",
    "As you wish, Sir!",
    "Understood, Sir!",
    "On it, Sir!",
]

jokes = [
    "Why did the computer go to the doctor? It had a virus!",
    "I told my computer I needed a break, and now it won't stop sending me beach wallpapers!",
    "Why was the computer cold? Because it left its Windows open!",
    "I'd tell you a joke about UDP, but you might not get it.",
]

affirmative_responses = [
    "Absolutely, Sir!",
    "Definitely, Sir!",
    "Of course, Sir!",
    "Consider it done, Sir!",
]

default_responses = [
    "I'm not sure I understand, Sir. Could you rephrase that?",
    "My AI systems seem offline right now. Could you try again?",
    "I couldn't process that, Sir. Perhaps try a different phrasing.",
    "That sounds interesting, but I need more context to help.",
    "I'm having trouble connecting to my AI brain. Please check the API key in config.py.",
]

ai_thinking = [
    "Let me think about that...",
    "Processing your request, Sir...",
    "Analyzing... one moment please.",
    "Consulting my AI brain, Sir...",
]

creator = ["Abhiyank"]