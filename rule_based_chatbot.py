"""
================================================================================
 RULE-BASED CHATBOT  |  Code Orbit Internship Project
================================================================================
A simple but professionally structured chatbot that uses keyword/pattern
matching (NOT machine learning) to generate responses. Includes:

  1. A rule engine (regex-based keyword matching) — the "brain"
  2. A CLI mode (for quick testing / grading in a terminal)
  3. A Tkinter GUI chat window (for a polished, industry-style demo)

HOW THE CHATBOT "DECIDES" A RESPONSE
--------------------------------------------------------------------------
  - Every incoming message is lower-cased and stripped of extra spaces.
  - We keep an ordered list of RULES. Each rule = (regex_pattern, responses).
  - We scan the rules IN ORDER and use re.search() to check if the pattern
    appears anywhere in the user's message.
  - The FIRST rule that matches wins (order matters — put specific rules
    like "bye" before generic ones).
  - If a rule matches, we randomly pick one of its possible responses
    (so the bot doesn't sound robotic/repetitive).
  - If NO rule matches, we fall back to a random "I don't understand"
    style response — this is the fallback/default case every chatbot
    needs so it never crashes or stays silent.
================================================================================
"""

import re
import random
import datetime
import sys

# ------------------------------------------------------------------------
# 1. RULE DEFINITIONS
# ------------------------------------------------------------------------
# Each rule is a tuple: (regex pattern, list of possible responses)
# Using regex (instead of plain "==") lets us match a keyword anywhere
# inside a sentence, e.g. "hey there!" still matches the greeting rule.
# NOTE: Order matters. More specific rules are placed before generic ones.
# ------------------------------------------------------------------------

RULES = [
    # --- Greetings ---
    (r"\b(hi|hello|hey|hola|good morning|good evening|good afternoon)\b",
     ["Hello! How can I help you today?",
      "Hi there! What can I do for you?",
      "Hey! Great to see you. How can I assist?"]),

    # --- Farewells (checked before generic word matches) ---
    (r"\b(bye|goodbye|see you|exit|quit)\b",
     ["Goodbye! Have a great day.",
      "See you soon! Take care.",
      "Bye! Feel free to come back anytime."]),

    # --- Gratitude ---
    (r"\b(thanks|thank you|thx)\b",
     ["You're welcome!",
      "Glad I could help!",
      "Anytime! Let me know if you need more help."]),

    # --- Identity questions ---
    (r"\b(your name|who are you)\b",
     ["I'm RuleBot, a simple rule-based chatbot built with Python.",
      "I'm a chatbot created for the Code Orbit internship project!"]),

    # --- Capability questions ---
    (r"\b(what can you do|help|capabilities|features)\b",
     ["I can chat about greetings, answer simple questions, tell you the "
      "time/date, and respond to common phrases. Try asking me the time!",
      "I'm a rule-based bot — I match keywords in your message to give "
      "relevant replies. Ask me something like 'how are you' or 'time'."]),

    # --- Wellbeing / small talk ---
    (r"\b(how are you|how're you|how you doing)\b",
     ["I'm just a program, but I'm running smoothly! How about you?",
      "Doing great, thanks for asking! How can I help?"]),

    # --- Bot creator ---
    (r"\b(who (made|created|built) you|your creator)\b",
     ["I was built in Python as part of a Code Orbit internship task."]),

    # --- Date / Time (dynamic response, not a fixed string) ---
    (r"\b(time)\b",
     None),  # handled dynamically below
    (r"\b(date|today)\b",
     None),  # handled dynamically below

    # --- Yes / No small talk ---
    (r"^\s*(yes|yeah|yep|sure)\s*$",
     ["Great! Let's continue.", "Awesome, glad to hear it."]),
    (r"^\s*(no|nope|nah)\s*$",
     ["No worries, let me know if that changes.",
      "Alright, is there something else I can help with?"]),

    # --- Emotions ---
    (r"\b(sad|upset|unhappy|depressed)\b",
     ["I'm sorry you're feeling that way. I'm just a simple bot, but I'm "
      "here to chat if it helps."]),
    (r"\b(happy|great|awesome|good news)\b",
     ["That's wonderful to hear! 🎉"]),

    # --- Chatbot-topic questions (nice touch for an "industry" demo) ---
    (r"\b(rule.?based|how do you work|how does this work)\b",
     ["I work by matching keywords/patterns in your message against a "
      "predefined set of rules using regular expressions, then choosing "
      "an appropriate response — no AI/ML involved, just logic!"]),
]

# ------------------------------------------------------------------------
# 2. FALLBACK RESPONSES (used when nothing in RULES matches)
# ------------------------------------------------------------------------
FALLBACK_RESPONSES = [
    "I'm not sure I understand. Could you rephrase that?",
    "Sorry, I didn't quite get that. Try asking about my capabilities!",
    "Hmm, I don't have a rule for that yet. Can you try something else?",
    "I'm a simple rule-based bot, so I might not understand everything. "
    "Try 'help' to see what I can do.",
]


def get_response(user_input: str) -> str:
    """
    Core decision function of the chatbot.

    Steps:
      1. Normalize the input (lowercase + strip whitespace) so matching
         is case-insensitive and consistent.
      2. Loop through RULES in order and test each regex pattern.
      3. On the first match:
           - If the rule has a dynamic handler (response list is None),
             compute a live value (like current time/date).
           - Otherwise, return a random response from that rule's list.
      4. If no rule matches after checking them all, return a random
         fallback response so the bot always replies with *something*.
    """
    text = user_input.lower().strip()

    if not text:
        return "You didn't type anything — go ahead, say something!"

    for pattern, responses in RULES:
        if re.search(pattern, text):
            # --- Dynamic rules handled here instead of a fixed list ---
            if responses is None:
                if "time" in pattern:
                    now = datetime.datetime.now().strftime("%I:%M %p")
                    return f"The current time is {now}."
                if "date" in pattern:
                    today = datetime.datetime.now().strftime("%A, %d %B %Y")
                    return f"Today's date is {today}."
            return random.choice(responses)

    # No rule matched -> fallback
    return random.choice(FALLBACK_RESPONSES)


# ============================================================================
# 3A. CLI MODE — simple terminal chat loop (good for quick testing/grading)
# ============================================================================
def run_cli():
    print("=" * 60)
    print(" RuleBot (CLI Mode) — type 'bye' or 'quit' to exit")
    print("=" * 60)
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nRuleBot: Goodbye!")
            break

        reply = get_response(user_input)
        print(f"RuleBot: {reply}")

        if re.search(r"\b(bye|goodbye|exit|quit)\b", user_input.lower()):
            break


# ============================================================================
# 3B. GUI MODE — polished Tkinter chat window (industry-style UI)
# ============================================================================
def run_gui():
    import tkinter as tk
    from tkinter import font as tkfont

    # ---- Colors / theme (simple modern "chat app" look) ----
    BG_MAIN = "#f0f2f5"
    BG_HEADER = "#075E54"
    BG_BOT_BUBBLE = "#ffffff"
    BG_USER_BUBBLE = "#DCF8C6"
    TEXT_COLOR = "#111111"
    HEADER_TEXT = "#ffffff"

    root = tk.Tk()
    root.title("RuleBot — Rule-Based Chatbot")
    root.geometry("420x600")
    root.configure(bg=BG_MAIN)
    root.minsize(360, 480)

    base_font = tkfont.Font(family="Segoe UI", size=10)
    bold_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")

    # ---- Header bar ----
    header = tk.Frame(root, bg=BG_HEADER, height=55)
    header.pack(side="top", fill="x")
    tk.Label(header, text="🤖 RuleBot", bg=BG_HEADER, fg=HEADER_TEXT,
              font=bold_font, pady=12).pack(side="left", padx=12)
    tk.Label(header, text="Online", bg=BG_HEADER, fg="#c8f7c5",
              font=base_font).pack(side="right", padx=12)

    # ---- Scrollable chat area ----
    chat_frame_container = tk.Frame(root, bg=BG_MAIN)
    chat_frame_container.pack(side="top", fill="both", expand=True)

    canvas = tk.Canvas(chat_frame_container, bg=BG_MAIN, highlightthickness=0)
    scrollbar = tk.Scrollbar(chat_frame_container, orient="vertical",
                              command=canvas.yview)
    chat_frame = tk.Frame(canvas, bg=BG_MAIN)

    chat_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=chat_frame, anchor="nw", width=400)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def add_bubble(text, sender="bot"):
        """Adds a chat bubble to the window and auto-scrolls down."""
        is_user = sender == "user"
        bubble_bg = BG_USER_BUBBLE if is_user else BG_BOT_BUBBLE
        anchor_side = "e" if is_user else "w"

        row = tk.Frame(chat_frame, bg=BG_MAIN)
        row.pack(fill="x", pady=4, padx=8, anchor=anchor_side)

        bubble = tk.Label(
            row, text=text, bg=bubble_bg, fg=TEXT_COLOR, font=base_font,
            wraplength=260, justify="left", padx=10, pady=8,
            relief="flat", bd=0
        )
        bubble.pack(side="right" if is_user else "left")

        # Let the UI redraw then scroll to bottom
        root.update_idletasks()
        canvas.yview_moveto(1.0)

    # ---- Input area ----
    input_frame = tk.Frame(root, bg=BG_MAIN, pady=8)
    input_frame.pack(side="bottom", fill="x")

    entry_var = tk.StringVar()
    entry = tk.Entry(input_frame, textvariable=entry_var, font=base_font,
                      relief="flat", bg="#ffffff")
    entry.pack(side="left", fill="x", expand=True, padx=(10, 6), ipady=8)
    entry.focus()

    def send_message(event=None):
        user_text = entry_var.get().strip()
        if not user_text:
            return
        add_bubble(user_text, sender="user")
        entry_var.set("")

        reply = get_response(user_text)
        # Small delay-free "typing" feel: just add the bot reply directly
        add_bubble(reply, sender="bot")

        if re.search(r"\b(bye|goodbye|exit|quit)\b", user_text.lower()):
            root.after(1200, root.destroy)

    send_btn = tk.Button(
        input_frame, text="Send", command=send_message,
        bg=BG_HEADER, fg="white", font=base_font,
        relief="flat", padx=16, pady=6, cursor="hand2"
    )
    send_btn.pack(side="right", padx=(0, 10))

    entry.bind("<Return>", send_message)

    # ---- Welcome message ----
    add_bubble("Hi! I'm RuleBot 👋 Ask me a question or say hello to get "
               "started. Type 'help' to see what I can do.", sender="bot")

    root.mainloop()


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Run with:  python rule_based_chatbot.py        -> GUI mode (default)
    #            python rule_based_chatbot.py --cli   -> terminal mode
    if "--cli" in sys.argv:
        run_cli()
    else:
        try:
            run_gui()
        except Exception as e:
            # Fallback to CLI if Tkinter isn't available on this machine
            print(f"[GUI unavailable: {e}] Falling back to CLI mode.\n")
            run_cli()
