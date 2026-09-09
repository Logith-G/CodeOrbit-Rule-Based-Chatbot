# 🤖 Rule-Based Chatbot

A Python-based rule-driven chatbot developed as part of a Code Orbit internship project.

## 📌 Project Overview

This project implements a simple rule-based chatbot using Python. Instead of machine learning or external AI APIs, the chatbot uses predefined rules and regular expressions to understand user messages and generate suitable responses.

The chatbot provides both:

- 💻 Command Line Interface (CLI)
- 🖥️ Graphical User Interface (GUI) using Tkinter

## ✨ Features

- Keyword and pattern-based conversation
- Regular expression matching
- Greeting and farewell responses
- Basic small talk
- Chatbot identity and capability responses
- Dynamic current time and date
- Multiple responses for the same type of input
- Fallback responses for unknown questions
- Interactive Tkinter GUI
- Scrollable chat interface
- User and chatbot chat bubbles
- Enter-key support for sending messages
- CLI mode for testing

## 🧠 How It Works

The chatbot follows a simple rule-based decision process:

1. User enters a message.
2. The message is converted to lowercase and cleaned.
3. The chatbot checks the predefined rules in order.
4. Regular expressions are used to find matching patterns.
5. The first matching rule is selected.
6. A response is selected from the available responses.
7. If no rule matches, a fallback response is returned.

The project does not use machine learning or external AI APIs.

## 🛠️ Technologies Used

- Python
- Regular Expressions (`re`)
- Tkinter
- Random
- DateTime
- System Arguments

## ▶️ How to Run

### GUI Mode

Open a terminal inside the project folder and run:

```bash
python rule_based_chatbot.py
```

The graphical chatbot interface will open.

### CLI Mode

To run the chatbot in the terminal:

```bash
python rule_based_chatbot.py --cli
```

## 💬 Example Conversations

```text
You: Hello
RuleBot: Hi there! What can I do for you?

You: What can you do?
RuleBot: I'm a rule-based bot — I match keywords in your message to give relevant replies.

You: What is the time?
RuleBot: The current time is 06:30 PM.

You: Thank you
RuleBot: You're welcome!

You: Bye
RuleBot: Goodbye! Have a great day.
```

## 📂 Project Structure

```text
Rule-Based-Chatbot/
│
├── rule_based_chatbot.py
├── README.md
└── .gitignore
```

## 🎓 Internship Project

Developed as part of a Python internship project at Code Orbit.

## 📄 Project Type


Rule-Based Chatbot / Python GUI Application

## 🖥️ Screenshots

### Chatbot GUI

![RuleBot GUI](screenshots/chatbot_gui.png)

### Chatbot Conversation

![RuleBot Conversation](screenshots/chatbot_conversation.png)
