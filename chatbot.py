"""
TASK 4 — Basic Rule-Based Chatbot
Goal  : Respond to user input with predefined replies.
Scope : Greetings, feelings, farewells, help, jokes, time, name.
Key   : if-elif, functions, loops, input/output
"""

import random
import datetime


# ── Response table ───────────────────────────────────────────────────────────
# Each key is a tuple of trigger words/phrases the user might type.
# Each value is a list of possible replies (one is chosen at random).
RESPONSES = {
    ("hello", "hi", "hey", "howdy", "hiya", "greetings", "sup"): [
        "Hi there! How can I help you today?",
        "Hey! Great to see you.",
        "Hello! What's on your mind?",
    ],
    ("how are you", "how do you do", "how's it going", "you okay", "you good"): [
        "I'm doing great, thanks for asking!",
        "Fantastic! Ready to chat.",
        "All systems go! How about you?",
    ],
    ("what is your name", "who are you", "your name"): [
        "I'm PyBot — your friendly rule-based assistant!",
        "They call me PyBot. Nice to meet you!",
    ],
    ("bye", "goodbye", "see you", "later", "farewell", "exit", "quit"): [
        "Goodbye! Have a wonderful day.",
        "See you later! Take care.",
        "Bye! Come back anytime.",
    ],
    ("help", "what can you do", "commands", "options"): [
        "I can respond to: greetings, 'how are you', my name, jokes, "
        "the time, and farewells. Try one!",
    ],
    ("joke", "tell me a joke", "funny", "make me laugh"): [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
        "Why did the developer go broke? Because he used up all his cache.",
    ],
    ("time", "what time is it", "current time", "what's the time"): [
        # This one is filled dynamically in get_response()
        "__TIME__",
    ],
    ("thanks", "thank you", "cheers", "thx"): [
        "You're welcome!",
        "Happy to help!",
        "Anytime!",
    ],
    ("age", "how old are you", "when were you born"): [
        "I was born the moment someone typed 'python chatbot.py'. Ageless!",
    ],
}

DEFAULT_REPLIES = [
    "Hmm, I'm not sure I understand. Try asking for 'help'.",
    "I didn't catch that. Type 'help' to see what I can do.",
    "Could you rephrase that? Or type 'help' for options.",
]


# ── Core logic ───────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase and strip punctuation from user input."""
    return text.lower().strip().rstrip("!?.,;:")


def get_response(user_input: str) -> str:
    """
    Match user_input against RESPONSES and return an appropriate reply.

    Strategy:
      1. Exact substring match against every trigger phrase.
      2. First match wins (order of dict keys is preserved in Python 3.7+).
      3. If no match → return a random DEFAULT_REPLY.
    """
    cleaned = normalize(user_input)

    for triggers, replies in RESPONSES.items():
        for trigger in triggers:
            if trigger in cleaned:
                reply = random.choice(replies)
                # Dynamic time substitution
                if reply == "__TIME__":
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    return f"The current time is {now}."
                return reply

    return random.choice(DEFAULT_REPLIES)


def is_farewell(text: str) -> bool:
    """Return True if the user wants to end the conversation."""
    farewell_words = ("bye", "goodbye", "see you", "later", "farewell",
                      "exit", "quit")
    cleaned = normalize(text)
    return any(word in cleaned for word in farewell_words)


# ── Main loop ────────────────────────────────────────────────────────────────

def run_chatbot():
    """Start the chatbot and keep the conversation going until the user exits."""
    print("=" * 48)
    print("  PyBot — Rule-Based Chatbot")
    print("  (Type 'bye' or 'quit' to exit)")
    print("=" * 48)
    print("PyBot: Hello! I'm PyBot. How can I help you?\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nPyBot: Goodbye!")
            break

        if not user_input:
            print("PyBot: (waiting for your message…)\n")
            continue

        response = get_response(user_input)
        print(f"PyBot: {response}\n")

        if is_farewell(user_input):
            break


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_chatbot()