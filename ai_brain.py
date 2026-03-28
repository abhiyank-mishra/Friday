# ai_brain.py — Friday's AI Brain powered by OpenRouter
# The AI decides WHAT to do — no keyword matching needed.

import requests
import json
from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    AI_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    MAX_MEMORY_TURNS,
    SYSTEM_PROMPT,
    TOOLS,
)


class AIBrain:
    """
    Friday's AI Brain — analyzes user intent via OpenRouter API,
    decides which tool to use (if any), and generates a response.
    """

    def __init__(self):
        self.conversation_history = []
        self.is_configured = OPENROUTER_API_KEY != "YOUR_OPENROUTER_API_KEY_HERE"

        # Build the system prompt with tool definitions baked in
        tools_summary = json.dumps(
            [{"name": t["name"], "description": t["description"], "parameters": t.get("parameters", [])} for t in TOOLS],
            indent=2
        )
        self.system_prompt = SYSTEM_PROMPT.replace("{tools_json}", tools_summary)

        if self.is_configured:
            print("[AI Brain] ✓ OpenRouter API key detected. AI mode active.")
            print(f"[AI Brain]   Model: {AI_MODEL}")
            print(f"[AI Brain]   Tools loaded: {len(TOOLS)}")
        else:
            print("[AI Brain] ✗ No API key found. Running in offline mode.")
            print("[AI Brain]   Set your key in config.py to enable AI features.")

    def _build_messages(self, user_input):
        """Build the message payload with system prompt + conversation history."""
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history (limited to MAX_MEMORY_TURNS)
        for exchange in self.conversation_history[-(MAX_MEMORY_TURNS * 2):]:
            messages.append(exchange)

        # Add current user input
        messages.append({"role": "user", "content": user_input})
        return messages

    def think(self, user_input):
        """
        Send the user's input to the AI.
        Returns a dict: {"tool": "tool_name" or "none", "params": {}, "response": "text"}
        Returns None if AI is unavailable.
        """
        if not self.is_configured:
            return None

        messages = self._build_messages(user_input)

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/abhiyank-mishra/friday",
            "X-Title": "Friday AI Assistant",
        }

        payload = {
            "model": AI_MODEL,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        }

        try:
            response = requests.post(
                OPENROUTER_BASE_URL,
                headers=headers,
                json=payload,
                timeout=20,
            )
            response.raise_for_status()

            data = response.json()
            raw_content = data["choices"][0]["message"]["content"].strip()

            # Parse the JSON response from AI
            result = self._parse_ai_response(raw_content)

            # Save to conversation memory
            self.conversation_history.append(
                {"role": "user", "content": user_input}
            )
            self.conversation_history.append(
                {"role": "assistant", "content": result.get("response", raw_content)}
            )

            # Trim memory
            if len(self.conversation_history) > MAX_MEMORY_TURNS * 2:
                self.conversation_history = self.conversation_history[-(MAX_MEMORY_TURNS * 2):]

            return result

        except requests.exceptions.Timeout:
            print("[AI Brain] ⚠ Request timed out.")
            return None
        except requests.exceptions.ConnectionError:
            print("[AI Brain] ⚠ No internet connection.")
            return None
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "unknown"
            print(f"[AI Brain] ⚠ API error (HTTP {status}).")
            if status == 401:
                print("[AI Brain]   → Invalid API key. Check config.py.")
            elif status == 429:
                print("[AI Brain]   → Rate limited. Try again shortly.")
            return None
        except Exception as e:
            print(f"[AI Brain] ⚠ Unexpected error: {e}")
            return None

    def _parse_ai_response(self, raw_content):
        """
        Parse the AI's response. It should be JSON like:
        {"tool": "...", "params": {...}, "response": "..."}
        
        If parsing fails, treat the whole response as a chat reply.
        """
        # Try to extract JSON from the response
        content = raw_content.strip()

        # Remove markdown code fences if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        try:
            result = json.loads(content)
            # Validate required fields
            if "response" not in result:
                result["response"] = raw_content
            if "tool" not in result:
                result["tool"] = "none"
            if "params" not in result:
                result["params"] = {}
            return result
        except json.JSONDecodeError:
            # AI didn't return valid JSON — treat as pure chat response
            return {
                "tool": "none",
                "params": {},
                "response": raw_content,
            }

    def clear_memory(self):
        """Clear the conversation history."""
        self.conversation_history = []
        return "Memory cleared, Sir. Starting fresh."

    def get_memory_status(self):
        """Return the number of exchanges stored in memory."""
        turns = len(self.conversation_history) // 2
        return f"I have {turns} conversation exchanges in memory, Sir."
