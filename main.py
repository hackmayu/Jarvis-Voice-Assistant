
import customtkinter as ctk
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import httpx
import re
import datetime
import subprocess
import os
import yfinance as yf
from googletrans import Translator
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import keyboard
from pystray import Icon, MenuItem, Menu
from PIL import Image

# API Keys and config
OPENROUTER_API_KEY = "Your API Key"
OPENWEATHER_API_KEY = "Your API Key"
NEWSAPI_KEY = "Your API key"
EMAIL_USER = "your.email@example.com"
EMAIL_PASS = "your_app_password"

# Text-to-Speech Setup
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Default voice

chat_history = []

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()
    chat_history.append(("Jarvis", text))
    chat_box.insert(ctk.END, f"Jarvis: {text}\n")
    chat_box.see(ctk.END)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except:
        speak("Sorry, I didn’t catch that.")
        return ""

def get_response(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are Jarvis, a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    }
    try:
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=20)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Sorry, I couldn't process that."



def handle_weather(command):
    match = re.search(r"\bweather(?: in)? ([a-zA-Z ]+)", command)
    if not match:
        return False  # ⛔ Not a weather-related command

    city = match.group(1).strip()
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = httpx.get(url)
        data = res.json()

        if data.get("cod") != 200:
            speak(f"I couldn't find weather info for {city}.")
        else:
            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feel = data["main"]["feels_like"]
            speak(f"{city.title()} weather is {desc}, temp {temp}°C, feels like {feel}°C.")
    except Exception as e:
        speak("Weather service is down.")
        print("Weather error:", e)

    return True  # ✅ Only return True if weather command handled


def handle_time_date(command):
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True
    if "date" in command:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")
        return True
    return False

def handle_web_commands(command):
    sites = {
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com"
    }
    for name, url in sites.items():
        if f"open {name}" in command:
            speak(f"Opening {name}")
            webbrowser.open(url)
            return True
    if command.startswith("play "):
        song = command.replace("play ", "").strip()
        if song:
            speak(f"Searching {song} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
        else:
            speak("Name the song you want to play")
        return True
    return False

def handle_news(command):
    if "news" in command:
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&pageSize=3&apiKey={NEWSAPI_KEY}"
            articles = httpx.get(url).json().get("articles", [])
            if not articles:
                speak("No headlines found.")
            else:
                speak("Latest tech news:")
                for i, a in enumerate(articles, 1):
                    speak(f"{i}. {a['title']}")
        except:
            speak("Couldn't load news.")
        return True
    return False

def handle_stock(command):
    match = re.search(r"stock price of ([a-zA-Z ]+)", command)
    if match:
        name = match.group(1).strip()
        tickers = {"apple": "AAPL", "google": "GOOGL", "amazon": "AMZN", "microsoft": "MSFT"}
        symbol = tickers.get(name.lower(), name.upper())
        try:
            price = yf.Ticker(symbol).info["regularMarketPrice"]
            speak(f"{name.title()} stock is ${price:.2f}")
        except:
            speak("Stock info not found.")
        return True
    return False

def handle_translation(command):
    match = re.search(r'translate [\'"](.+?)[\'"] to (\w+)', command)
    if match:
        text = match.group(1)
        lang = match.group(2).lower()
        try:
            translator = Translator()
            result = translator.translate(text, dest=lang)
            speak(f"Translation: {result.text}")
        except Exception as e:
            speak("Translation failed.")
            print("Translation error:", e)
        return True
    return False

def handle_email(command):
    if "send email to" in command and "saying" in command:
        try:
            parts = command.split("saying")
            recipient_part = parts[0].replace("send email to", "").strip()
            message = parts[1].strip().strip("\"'")
            
            recipients = {"john": "john@example.com", "alex": "alex@example.com"}
            to_email = recipients.get(recipient_part.lower())
            
            if not to_email:
                speak(f"No email address found for {recipient_part}.")
                return True

            msg = MIMEText(message)
            msg["Subject"] = "Message from Jarvis"
            msg["From"] = EMAIL_USER
            msg["To"] = to_email

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.send_message(msg)
            
            speak("Email sent successfully.")
        except Exception as e:
            speak("Failed to send email.")
        return True
    return False

import subprocess
import os

def handle_app_launch(command):
    command = command.lower()

    # Basic Windows Utilities
    if "notepad" in command:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")
        return True

    elif "calculator" in command:
        speak("Opening Calculator")
        subprocess.Popen("calc.exe")
        return True

    elif "paint" in command:
        speak("Opening Paint")
        subprocess.Popen("mspaint.exe")
        return True

    elif "command prompt" in command or "cmd" in command:
        speak("Opening Command Prompt")
        subprocess.Popen("cmd.exe")
        return True

    elif "file explorer" in command:
        speak("Opening File Explorer")
        subprocess.Popen("explorer.exe")
        return True

    elif "task manager" in command:
        speak("Opening Task Manager")
        subprocess.Popen("taskmgr")
        return True

    elif "control panel" in command:
        speak("Opening Control Panel")
        subprocess.Popen("control")
        return True

    # Browsers
    elif "chrome" in command:
        speak("Opening Google Chrome")
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        return True

    elif "firefox" in command:
        speak("Opening Mozilla Firefox")
        subprocess.Popen(r"C:\Program Files\Mozilla Firefox\firefox.exe")
        return True

    elif "edge" in command:
        speak("Opening Microsoft Edge")
        subprocess.Popen("msedge")
        return True

    # Office Applications
    elif "word" in command:
        speak("Opening Microsoft Word")
        subprocess.Popen(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")
        return True

    elif "excel" in command:
        speak("Opening Microsoft Excel")
        subprocess.Popen(r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE")
        return True

    elif "powerpoint" in command:
        speak("Opening Microsoft PowerPoint")
        subprocess.Popen(r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE")
        return True

    # Developer Tools
    elif "vs code" in command or "visual studio code" in command:
        speak("Opening Visual Studio Code")
        subprocess.Popen(r"C:\Users\jalan\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        return True

    elif "pycharm" in command:
        speak("Opening PyCharm")
        subprocess.Popen(r"C:\Program Files\JetBrains\PyCharm Community Edition 2023.1\bin\pycharm64.exe")
        return True

    elif "jupyter notebook" in command:
        speak("Launching Jupyter Notebook")
        subprocess.Popen("jupyter-notebook")
        return True

    elif "anaconda prompt" in command or "anaconda navigator" in command:
        speak("Opening Anaconda Navigator")
        subprocess.Popen(r"C:\Users\jalan\anaconda3\Scripts\anaconda-navigator.exe")
        return True

    # Media Apps
    elif "spotify" in command:
        speak("Opening Spotify")
        subprocess.Popen(r"C:\Users\jalan\AppData\Roaming\Spotify\Spotify.exe")
        return True

    elif "vlc" in command:
        speak("Opening VLC Player")
        subprocess.Popen(r"C:\Program Files\VideoLAN\VLC\vlc.exe")
        return True

    elif "camera" in command:
        speak("Opening Camera")
        os.system("start microsoft.windows.camera:")
        return True

    return False


def process_command(command):
    if not command:
        return
    chat_history.append(("You", command))
    
    if handle_web_commands(command): return
    if handle_weather(command): return
    if handle_time_date(command): return
    if handle_news(command): return
    if handle_stock(command): return
    if handle_translation(command): return
    if handle_email(command): return
    if handle_app_launch(command): return  # 🔥 ADD THIS LINE

    response = get_response(command)
    speak(response)

def listen_thread():
    command = listen()
    chat_box.insert(ctk.END, f"You: {command}\n")
    chat_box.see(ctk.END)
    process_command(command)

def on_send():
    command = user_entry.get().lower()
    user_entry.delete(0, ctk.END)
    chat_box.insert(ctk.END, f"You: {command}\n")
    chat_box.see(ctk.END)
    threading.Thread(target=process_command, args=(command,), daemon=True).start()

def save_chat():
    with open("jarvis_chat.txt", "w") as f:
        for speaker, msg in chat_history:
            f.write(f"{speaker}: {msg}\n")
    pd.DataFrame(chat_history, columns=["Speaker", "Message"]).to_excel("jarvis_chat.xlsx", index=False)
    speak("Chat history saved.")

def quit_app(icon, item):
    save_chat()
    icon.stop()
    app.quit()

def show_gui(icon, item):
    app.deiconify()

def hide_gui():
    app.withdraw()
from PIL import Image, ImageDraw

def setup_tray_icon():
    # Create a simple blue square icon dynamically
    image = Image.new("RGB", (64, 64), color=(0, 102, 204))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), "J", fill="white")  # Optional: Draw 'J' for Jarvis

    menu = Menu(MenuItem('Show Jarvis', show_gui), MenuItem('Quit', quit_app))
    tray = Icon("Jarvis", image, menu=menu)
    threading.Thread(target=tray.run, daemon=True).start()


def background_hotkey_listener():
    keyboard.add_hotkey("ctrl+shift+j", lambda: threading.Thread(target=listen_thread, daemon=True).start())

# GUI Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("600x500")
app.title("Jarvis AI Assistant")

chat_box = ctk.CTkTextbox(app, width=580, height=400, font=("Consolas", 14))
chat_box.pack(padx=10, pady=(10, 0))
chat_box.insert(ctk.END, "Jarvis: Jarvis GUI loaded.\n")

user_entry = ctk.CTkEntry(app, placeholder_text="Ask something...", width=360, font=("Arial", 14))
user_entry.pack(side="left", padx=(10, 0), pady=10)

send_btn = ctk.CTkButton(app, text="Send", command=on_send)
send_btn.pack(side="left", padx=5)

voice_btn = ctk.CTkButton(app, text="🎤 Voice", command=lambda: threading.Thread(target=listen_thread, daemon=True).start())
voice_btn.pack(side="left", padx=5)

save_btn = ctk.CTkButton(app, text="💾 Save Chat", command=save_chat)
save_btn.pack(side="left", padx=5)

#hide_gui()
setup_tray_icon()
background_hotkey_listener()

app.mainloop()
