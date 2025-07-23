# **🤖 Jarvis Voice Assistant

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Anaconda%20%7C%20Tkinter-informational)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

---

## **🧠 About the Project**

**Jarvis Voice Assistant** is a desktop-based smart assistant developed in Python that allows users to interact with their computer using natural voice commands. It responds in a human-like voice, performs real-time tasks, and has a user-friendly GUI interface. Inspired by Iron Man’s Jarvis, this assistant can perform web searches, fetch weather data, tell jokes, send emails, translate languages, play music, launch apps, check stock prices, and much more.

Designed with modularity and real-time feedback, it’s a perfect project to showcase your Python, API integration, and GUI development skills.

---

## **🖼️ Demo Screenshot**
<img width="1256" height="755" alt="image" src="https://github.com/user-attachments/assets/99274aa1-f2e1-415e-8b96-399b8e8492c1" />



-

## **✨ Key Features**

- 🎙️ Real-time voice recognition & TTS response
- 🌤️ Live weather info (OpenWeatherMap API)
- 📆 Time & date announcement
- 🌐 Web search & Wikipedia Q&A
- 📬 Voice-controlled email sending
- 📈 Stock market prices (Yahoo Finance)
- 📰 Latest news headlines (via NewsAPI or Bing)
- 💬 Language translation between major languages
- 🧠 Personality Mode: Jarvis-like smart replies
- ⚙️ App launcher (Notepad, VS Code, Calculator, etc.)
- 🪟 GUI with status labels & user feedback
- 🧊 Glassmorphism UI style using Tkinter
- 🎤 Wake-word mode & system tray background support
- 💾 Save chat history to .txt or .xlsx
- 📦 Exportable to .exe with custom icon

---

## **🛠️ Technologies Used**

- **Python 3.10** – Core programming language
- **Tkinter** – GUI framework for desktop interface
- **SpeechRecognition** – Captures user voice input
- **pyttsx3** – Converts text to speech (offline TTS)
- **OpenWeatherMap API** – Provides weather data
- **OpenAI / OpenRouter API** – Powers smart Q&A
- **NewsAPI / Bing News API** – For headlines
- **smtplib** – Email functionality
- **googletrans / translate** – Language translation
- **yfinance** – Stock price lookup
- **PIL (Pillow)** – Tray icon support
- **keyboard & pystray** – Hotkeys & system tray

---

## **⚙️ Installation**

```bash
git clone https://github.com/yourusername/Jarvis-Voice-Assistant.git
cd Jarvis-Voice-Assistant
conda activate jarvis310_py10  # Or use: python -m venv env && env\Scripts\activate
pip install -r requirements.txt
python main.py
 
