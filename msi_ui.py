"""
MSI - ADVANCED AI VOICE ASSISTANT WITH UI
Complete Laptop Control System with Beautiful Interface
"""

import customtkinter as ctk
import threading
import os
import sys
import time
import datetime
import subprocess
import webbrowser
import random
import shutil
import psutil
from pathlib import Path
import pyttsx3
import speech_recognition as sr
import requests
import winreg
import ctypes
import json

# Import login system
from login import LoginApp, DatabaseManager

# --- CONFIGURATION ---
WEATHER_API_KEY = "f1b3b5e16ef92c419c6dffec5c7de505"  # Replace with your key from openweathermap.org
CITY = "Vijayawada"

# --- CHAT HISTORY CONFIGURATION ---
HISTORY_DIR = Path.home() / ".msi_history"
HISTORY_DIR.mkdir(exist_ok=True)
CURRENT_SESSION_FILE = HISTORY_DIR / f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==================== CHAT HISTORY MANAGER ====================
class ChatHistoryManager:
    """Manages chat history storage and retrieval"""
    
    def __init__(self):
        self.history_dir = HISTORY_DIR
        self.current_session = []
        self.load_previous_sessions()
    
    def load_previous_sessions(self):
        """Load chat history from previous sessions"""
        try:
            all_sessions = []
            if self.history_dir.exists():
                for session_file in sorted(self.history_dir.glob("session_*.json")):
                    try:
                        with open(session_file, 'r', encoding='utf-8') as f:
                            session_data = json.load(f)
                            all_sessions.append({
                                'file': session_file.name,
                                'messages': session_data
                            })
                    except:
                        pass
            return all_sessions
        except:
            return []
    
    def add_to_history(self, sender: str, message: str):
        """Add message to current session history"""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.current_session.append({
            'timestamp': timestamp,
            'sender': sender,
            'message': message
        })
        self.save_current_session()
    
    def save_current_session(self):
        """Save current session to file"""
        try:
            with open(CURRENT_SESSION_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.current_session, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def get_session_summary(self) -> str:
        """Get summary of previous sessions"""
        sessions = self.load_previous_sessions()
        if not sessions:
            return "No previous sessions found."
        
        summary = f"Found {len(sessions)} previous sessions:\n"
        for i, session in enumerate(sessions[-5:], 1):  # Show last 5 sessions
            msg_count = len(session['messages'])
            summary += f"{i}. {session['file']}: {msg_count} messages\n"
        return summary

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==================== ADVANCED COMMAND EXECUTOR ====================
class AdvancedCommandExecutor:
    """COMPLETE LAPTOP CONTROL"""
    
    def __init__(self):
        self.user = os.getlogin()
        
    def set_volume(self, level: int):
        """Set volume level (0-100)"""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            return f"Volume set to {level}%"
        except:
            os.system(f"nircmd.exe setsysvolume {int(level * 655.35)}")
            return f"Volume adjusted to {level}%"
    
    def get_battery_status(self):
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "Plugged in" if battery.power_plugged else "On battery"
                time_left = f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m" if battery.secsleft > 0 else "Calculating"
                return f"Battery: {percent}%. {plugged}. Time remaining: {time_left}"
            return "Battery information not available"
        except:
            return "Could not get battery status"
    
    def get_system_stats(self):
        """Get CPU, RAM, and Disk usage"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            return f"CPU: {cpu}%, RAM: {ram}%, Disk: {disk}%"
        except:
            return "Could not get system stats"
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            import pyautogui
            import time as time_module
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            desktop_path = Path.home() / "Desktop"
            desktop_path.mkdir(exist_ok=True)
            path = desktop_path / filename
            
            # Add small delay to ensure window is ready
            time_module.sleep(0.5)
            pyautogui.screenshot(str(path))
            
            if path.exists():
                return f"Screenshot saved to Desktop as {filename}"
            else:
                return "Screenshot capture failed - file not created"
        except ImportError:
            return "Could not take screenshot. Install pyautogui: pip install pyautogui"
        except Exception as e:
            return f"Screenshot error: {str(e)}"
    
    def set_brightness(self, level: int):
        """Set screen brightness (0-100)"""
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except:
            return "Could not set brightness"
    
    def open_file(self, filename: str):
        """Open a file by name"""
        try:
            # Common file locations
            search_paths = [
                Path.home() / "Desktop",
                Path.home() / "Documents",
                Path.home() / "Downloads",
                Path.home()
            ]
            
            for path in search_paths:
                for file in path.rglob(f"*{filename}*"):
                    if file.is_file():
                        os.startfile(str(file))
                        return f"Opened {file.name}"
            
            return f"Could not find file: {filename}"
        except Exception as e:
            return f"Error opening file: {str(e)}"
    
    def open_telegram(self, person_name: str = None, use_installed: bool = False):
        """Open Telegram - installed app or web version"""
        try:
            # Try to find Telegram executable
            telegram_paths = [
                os.path.expandvars(r"%APPDATA%\Telegram Desktop\Telegram.exe"),
                r"C:\Program Files\Telegram Desktop\Telegram.exe",
                r"C:\Program Files (x86)\Telegram Desktop\Telegram.exe"
            ]
            
            # If user explicitly wants installed version
            if use_installed:
                for path in telegram_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path])
                        
                        if person_name:
                            time.sleep(2)
                            webbrowser.open(f"tg://resolve?domain={person_name}")
                            return f"Opening Telegram (Installed) chat with {person_name}"
                        return "Opening Telegram (Installed)"
                # If installed not found, fall back to web
                return self.open_telegram_web(person_name)
            
            # Default: Try web version first
            return self.open_telegram_web(person_name)
            
        except Exception as e:
            return f"Error opening Telegram: {str(e)}"
    
    def open_telegram_web(self, person_name: str = None):
        """Open Telegram Web version"""
        try:
            webbrowser.open("https://web.telegram.org")
            if person_name:
                return f"Opening Telegram Web. Please search for {person_name}"
            return "Opening Telegram Web"
        except:
            return "Could not open Telegram Web"
    
    def open_whatsapp(self, person_name: str = None, use_installed: bool = False):
        """Open WhatsApp - installed app or web version"""
        try:
            # WhatsApp Desktop paths
            whatsapp_paths = [
                os.path.expandvars(r"%APPDATA%\WhatsApp\WhatsApp.exe"),
                r"C:\Program Files\WhatsApp\WhatsApp.exe",
                r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe"
            ]
            
            # If user explicitly wants installed version
            if use_installed:
                for path in whatsapp_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path])
                        if person_name:
                            return f"Opening WhatsApp (Installed). Please search for {person_name}"
                        return "Opening WhatsApp (Installed)"
                # If installed not found, fall back to web
                return self.open_whatsapp_web(person_name)
            
            # Default: Try web version first
            return self.open_whatsapp_web(person_name)
        except Exception as e:
            return f"Error opening WhatsApp: {str(e)}"
    
    def open_whatsapp_web(self, person_name: str = None):
        """Open WhatsApp Web version"""
        try:
            webbrowser.open("https://web.whatsapp.com")
            if person_name:
                return f"Opening WhatsApp Web. Please search for {person_name}"
            return "Opening WhatsApp Web"
        except:
            return "Could not open WhatsApp Web"
    
    def open_spotify(self, song_name: str = None):
        """Open Spotify and optionally play a song"""
        try:
            # Spotify Desktop paths
            spotify_paths = [
                os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
                r"C:\Users" + os.path.expanduser("~").split("Users")[1].split("\\")[0] + r"\AppData\Roaming\Spotify\Spotify.exe",
                r"C:\Program Files\Spotify\Spotify.exe",
                r"C:\Program Files (x86)\Spotify\Spotify.exe"
            ]
            
            # Try to find and open installed Spotify
            spotify_found = False
            for path in spotify_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    spotify_found = True
                    break
            
            if song_name:
                # Wait for Spotify to start
                time.sleep(2)
                # Use Spotify protocol to search and play song
                # Remove special characters and convert spaces to %20
                song_query = song_name.strip().replace(" ", "%20")
                webbrowser.open(f"spotify:search:{song_query}")
                return f"Opening Spotify - Playing: {song_name}"
            
            if spotify_found:
                return "Opening Spotify Desktop"
            else:
                # Fallback to web version
                webbrowser.open("https://open.spotify.com")
                if song_name:
                    return f"Opening Spotify Web. Please search and play: {song_name}"
                return "Opening Spotify Web"
                
        except Exception as e:
            return f"Error opening Spotify: {str(e)}"

# ==================== MAIN COMMAND EXECUTOR ====================
class CommandExecutor:
    """EXECUTES ALL COMMANDS"""
    
    def __init__(self):
        self.user = os.getlogin()
        self.advanced = AdvancedCommandExecutor()
    
    def execute(self, command: str) -> str:
        """Execute command - COMPLETE LAPTOP CONTROL"""
        cmd = command.lower().strip()
        
        # ========== VOLUME CONTROL ==========
        if "volume" in cmd or "sound" in cmd:
            if "up" in cmd or "increase" in cmd:
                return self.advanced.set_volume(100)
            elif "down" in cmd or "decrease" in cmd:
                return self.advanced.set_volume(20)
            elif "mute" in cmd or "zero" in cmd:
                return self.advanced.set_volume(0)
            elif "50" in cmd or "fifty" in cmd or "half" in cmd:
                return self.advanced.set_volume(50)
            elif "75" in cmd or "seventy" in cmd:
                return self.advanced.set_volume(75)
            elif "100" in cmd or "full" in cmd or "max" in cmd:
                return self.advanced.set_volume(100)
            else:
                words = cmd.split()
                for word in words:
                    if word.isdigit():
                        level = int(word)
                        if 0 <= level <= 100:
                            return self.advanced.set_volume(level)
                return "Specify volume level (0-100)"
        
        # ========== BRIGHTNESS CONTROL ==========
        elif "brightness" in cmd or "screen brightness" in cmd:
            if "up" in cmd or "increase" in cmd or "high" in cmd:
                return self.advanced.set_brightness(100)
            elif "down" in cmd or "decrease" in cmd or "low" in cmd:
                return self.advanced.set_brightness(30)
            elif "50" in cmd or "fifty" in cmd or "half" in cmd or "medium" in cmd:
                return self.advanced.set_brightness(50)
            else:
                words = cmd.split()
                for word in words:
                    if word.isdigit():
                        level = int(word)
                        if 0 <= level <= 100:
                            return self.advanced.set_brightness(level)
                return "Specify brightness level (0-100)"
        
        # ========== BATTERY STATUS ==========
        elif "battery" in cmd or "power status" in cmd:
            return self.advanced.get_battery_status()
        
        # ========== SYSTEM STATS ==========
        elif "system stats" in cmd or "performance" in cmd or "cpu" in cmd or "ram usage" in cmd:
            return self.advanced.get_system_stats()
        
        # ========== SCREENSHOT ==========
        elif "screenshot" in cmd or "screen shot" in cmd or "capture screen" in cmd:
            return self.advanced.take_screenshot()
        
        # ========== OPEN FILE ==========
        elif "open file" in cmd:
            filename = cmd.replace("open file", "").strip()
            if filename:
                return self.advanced.open_file(filename)
            return "Please specify a file name"
        
        # ========== TELEGRAM ==========
        elif "telegram" in cmd or "open telegram" in cmd:
            use_installed = "installed" in cmd
            if "chat" in cmd or "message" in cmd:
                # Extract person name
                person = cmd.replace("telegram", "").replace("open", "").replace("chat", "").replace("message", "").replace("installed", "").strip()
                return self.advanced.open_telegram(person if person else None, use_installed=use_installed)
            return self.advanced.open_telegram(use_installed=use_installed)
        
        # ========== WHATSAPP ==========
        elif "whatsapp" in cmd or "open whatsapp" in cmd:
            use_installed = "installed" in cmd
            person = cmd.replace("whatsapp", "").replace("open", "").replace("chat", "").replace("message", "").replace("installed", "").strip()
            return self.advanced.open_whatsapp(person if person else None, use_installed=use_installed)
        
        # ========== SPOTIFY ==========
        elif "spotify" in cmd or "open spotify" in cmd or "play" in cmd and "spotify" in cmd:
            if "play" in cmd:
                # Extract song name - remove keywords to get song
                song = cmd.replace("spotify", "").replace("open", "").replace("play", "").replace("and", "").strip()
                if song:
                    return self.advanced.open_spotify(song)
                else:
                    return self.advanced.open_spotify()
            return self.advanced.open_spotify()
        
        # ========== FOLDER COMMANDS ==========
        elif "open folder" in cmd:
            folder = cmd.replace("open folder", "").strip()
            
            if not folder:
                os.startfile('.')
                return "Opened current folder"
            
            if "desktop" in folder:
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                os.startfile(desktop)
                return "Opened Desktop"
            
            elif "documents" in folder:
                docs = os.path.join(os.path.expanduser("~"), "Documents")
                os.startfile(docs)
                return "Opened Documents"
            
            elif "downloads" in folder:
                downloads = os.path.join(os.path.expanduser("~"), "Downloads")
                os.startfile(downloads)
                return "Opened Downloads"
        
        # ========== OPEN APPLICATIONS ==========
        elif "open notepad" in cmd:
            os.system("start notepad")
            return "Opening Notepad"
        
        elif "open calculator" in cmd:
            os.system("start calc")
            return "Opening Calculator"
        
        elif "open paint" in cmd:
            os.system("start mspaint")
            return "Opening Paint"
        
        elif "open chrome" in cmd:
            os.system("start chrome")
            return "Opening Chrome"
        
        elif "task manager" in cmd:
            os.system("taskmgr")
            return "Opening Task Manager"
        
        # ========== SYSTEM CONTROL ==========
        elif "shutdown" in cmd:
            os.system("shutdown /s /t 5")
            return "Shutting down in 5 seconds!"
        
        elif "restart" in cmd:
            os.system("shutdown /r /t 5")
            return "Restarting in 5 seconds!"
        
        elif "lock" in cmd:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Computer locked!"
        
        # ========== WEB BROWSING ==========
        elif "open youtube" in cmd:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube"
        
        elif "open google" in cmd:
            webbrowser.open("https://google.com")
            return "Opening Google"
        
        elif cmd.startswith("search "):
            query = cmd[7:].strip()
            webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
            return f"Searching: {query}"
        
        elif cmd.startswith("play "):
            query = cmd[5:].strip()
            webbrowser.open(f"https://youtube.com/results?search_query={query.replace(' ', '+')}")
            return f"Playing: {query}"
        
        # ========== TIME & DATE ==========
        elif "time" in cmd or "what time" in cmd:
            current = datetime.datetime.now().strftime("%I:%M %p")
            return f"The time is {current}"
        
        elif "date" in cmd or "today's date" in cmd:
            current = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current}"
        
        # ========== JOKES ==========
        elif "joke" in cmd or "tell joke" in cmd:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the computer go to the doctor? Because it had a virus!",
                "What do you call a fake noodle? An impasta!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
            ]
            return random.choice(jokes)
        
        # ========== GREETINGS ==========
        elif any(word in cmd for word in ["hello", "hi", "hey"]):
            return f"Hello {self.user}! How can I assist you?"
        
        elif "how are you" in cmd:
            return "All systems operational! Ready to assist."
        
        elif "your name" in cmd:
            return "I am MSI, your advanced AI voice assistant!"
        
        # ========== DEFAULT ==========
        else:
            return f"Command not recognized: '{cmd}'. Say 'help' for available commands."

# ==================== MSI UI APPLICATION ====================
class MSIApp(ctk.CTk):
    def __init__(self, username=None):
        super().__init__()

        self.title("M.S.I. Control System")
        self.geometry("1000x750")
        self.logged_in_user = username if username else os.getlogin()
        
        # Update window title with username
        self.title(f"M.S.I. Control System - Welcome {self.logged_in_user}")
        
        # Show login first
        self.withdraw()  # Hide main window initially
        login_app = LoginApp(callback=self.on_login_success)
        self.wait_window(login_app)
        self.deiconify()  # Show main window after login
        
        # Core Systems
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)
        self.recognizer = sr.Recognizer()
        # Lower energy threshold for better mic sensitivity
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.is_listening = False
        self.command_executor = CommandExecutor()
        self.chat_history = ChatHistoryManager()
        self.db = DatabaseManager()
        
        self.setup_ui()

        # Start diagnostics
        threading.Thread(target=self.run_startup_diagnostics, daemon=True).start()
    
    def on_login_success(self, username):
        """Callback when user logs in successfully"""
        self.current_user = username
        self.title(f"M.S.I. Control System - User: {username}")

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)  # Chat history sidebar
        self.grid_rowconfigure(1, weight=1)

        # 1. LEFT SIDEBAR (System Widgets)
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#1a1a1a")
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=0)
        
        self.side_label = ctk.CTkLabel(self.sidebar, text="SYSTEM WIDGETS", 
                                       font=("Orbitron", 20, "bold"), text_color="#00d4ff")
        self.side_label.pack(pady=20)
        
        # System Stats
        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="#0a0a0a", corner_radius=10)
        self.stats_frame.pack(pady=10, padx=15, fill="x")
        
        self.cpu_label = ctk.CTkLabel(self.stats_frame, text="CPU: ---%", 
                                      font=("Consolas", 12), text_color="#00ff00")
        self.cpu_label.pack(pady=5, padx=10, anchor="w")
        
        self.ram_label = ctk.CTkLabel(self.stats_frame, text="RAM: ---%", 
                                      font=("Consolas", 12), text_color="#00ff00")
        self.ram_label.pack(pady=5, padx=10, anchor="w")
        
        self.disk_label = ctk.CTkLabel(self.stats_frame, text="DISK: ---%", 
                                       font=("Consolas", 12), text_color="#00ff00")
        self.disk_label.pack(pady=5, padx=10, anchor="w")
        
        # Battery
        self.battery_frame = ctk.CTkFrame(self.sidebar, fg_color="#0a0a0a", corner_radius=10)
        self.battery_frame.pack(pady=10, padx=15, fill="x")
        
        self.battery_label = ctk.CTkLabel(self.battery_frame, text="BATTERY: ---%", 
                                         font=("Consolas", 12), text_color="#ffcc00")
        self.battery_label.pack(pady=10, padx=10)
        
        # Weather
        self.weather_frame = ctk.CTkFrame(self.sidebar, fg_color="#0a0a0a", corner_radius=10)
        self.weather_frame.pack(pady=10, padx=15, fill="x")
        
        self.weather_label = ctk.CTkLabel(self.weather_frame, text="WEATHER: Loading...", 
                                         font=("Consolas", 11), justify="left")
        self.weather_label.pack(pady=10, padx=10)
        
        # Quick Actions
        self.quick_frame = ctk.CTkFrame(self.sidebar, fg_color="#0a0a0a", corner_radius=10)
        self.quick_frame.pack(pady=10, padx=15, fill="x")
        
        ctk.CTkLabel(self.quick_frame, text="QUICK ACTIONS", 
                    font=("Orbitron", 12, "bold"), text_color="#00d4ff").pack(pady=5)
        
        ctk.CTkButton(self.quick_frame, text="📸 Screenshot", width=200,
                     command=lambda: self.execute_quick_command("screenshot")).pack(pady=3)
        ctk.CTkButton(self.quick_frame, text="🔊 Volume 50%", width=200,
                     command=lambda: self.execute_quick_command("volume 50")).pack(pady=3)
        ctk.CTkButton(self.quick_frame, text="💡 Brightness 50%", width=200,
                     command=lambda: self.execute_quick_command("brightness 50")).pack(pady=3)

        # 2. MAIN CONSOLE
        self.logo_label = ctk.CTkLabel(self, text="SYSTEM STATUS: INITIALIZING", 
                                       font=("Orbitron", 24, "bold"), text_color="#ffcc00")
        self.logo_label.grid(row=0, column=1, padx=30, pady=(20, 10))
        
        self.console = ctk.CTkTextbox(self, fg_color="#0a0a0a", border_color="#00d4ff", 
                                      border_width=2, font=("Consolas", 13), 
                                      text_color="#00ff00")
        self.console.grid(row=1, column=1, padx=30, pady=10, sticky="nsew")
        self.console.configure(state="disabled")

        # 3. INPUT/BUTTONS
        self.cmd_entry = ctk.CTkEntry(self, placeholder_text="Awaiting system check...", 
                                      height=40, font=("Consolas", 14), 
                                      border_color="#00d4ff", border_width=2)
        self.cmd_entry.grid(row=2, column=1, padx=30, pady=10, sticky="ew")
        self.cmd_entry.bind("<Return>", lambda e: self.process_text_command())
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=1, pady=(10, 20))
        
        self.mic_button = ctk.CTkButton(self.button_frame, text="🎤 TESTING MIC...", 
                                       state="disabled", command=self.toggle_voice_mode, 
                                       fg_color="#555555", width=180, height=40,
                                       font=("Orbitron", 14, "bold"))
        self.mic_button.pack(side="left", padx=10)
        
        self.clear_button = ctk.CTkButton(self.button_frame, text="🗑️ CLEAR LOG", 
                                         command=self.clear_console, width=150, height=40,
                                         font=("Orbitron", 14, "bold"), fg_color="#a11d1d")
        self.clear_button.pack(side="left", padx=10)
        
        self.history_toggle_button = ctk.CTkButton(self.button_frame, text="📜 TOGGLE HISTORY", 
                                           command=self.toggle_history_sidebar, width=180, height=40,
                                           font=("Orbitron", 14, "bold"), fg_color="#1f538d")
        self.history_toggle_button.pack(side="left", padx=10)
        
        # 4. RIGHT SIDEBAR - CHAT HISTORY
        self.history_sidebar_visible = True
        self.history_sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="#1a1a1a")
        self.history_sidebar.grid(row=0, column=2, rowspan=4, sticky="nsew", padx=0)
        
        # Chat History Title
        self.history_title = ctk.CTkLabel(self.history_sidebar, text="💬 CHAT HISTORY", 
                                         font=("Orbitron", 18, "bold"), text_color="#00d4ff")
        self.history_title.pack(pady=15)
        
        # Scrollable frame for chat list
        self.chat_list_frame = ctk.CTkScrollableFrame(self.history_sidebar, 
                                                      fg_color="#0a0a0a",
                                                      height=600)
        self.chat_list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Load chat sessions
        self.load_chat_sessions()

    def run_startup_diagnostics(self):
        """Perform hardware and mic check before starting"""
        self.log("DIAGNOSTICS: Starting Microphone Test...")
        self.log("=" * 50)
        
        # Show previous chat history summary
        self.log("📜 CHAT HISTORY:")
        sessions = self.chat_history.load_previous_sessions()
        if sessions:
            self.log(f"   Found {len(sessions)} previous chat sessions")
            self.log("   View them in the sidebar →")
        else:
            self.log("   No previous sessions found.")
            self.log("   Your conversations will be saved automatically!")
        
        self.log("=" * 50)
        
        try:
            with sr.Microphone() as source:
                self.log("DIAGNOSTICS: Adjusting for ambient noise (Stay quiet for 2 seconds)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                current_threshold = self.recognizer.energy_threshold
                self.log(f"DIAGNOSTICS: Mic sensitivity set to {round(current_threshold, 2)}")
                
                # Set a reasonable threshold if too high
                if current_threshold > 1000:
                    self.recognizer.energy_threshold = 300
                    self.log(f"DIAGNOSTICS: Adjusted threshold to 300 for better sensitivity")
                
                self.log("DIAGNOSTICS: Performing audio check...")
                self.log("DIAGNOSTICS: Say something to test the microphone...")
                
                # Test listening
                try:
                    test_audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=2)
                    test_text = self.recognizer.recognize_google(test_audio)
                    self.log(f"DIAGNOSTICS: Test successful! Heard: '{test_text}'")
                except:
                    self.log("DIAGNOSTICS: No speech detected, but mic is ready.")
                
            self.log("DIAGNOSTICS: Hardware check PASSED.")
            self.logo_label.configure(text="SYSTEM STATUS: ONLINE", text_color="#00ff00")
            self.mic_button.configure(text="🎤 ACTIVATE VOICE", state="normal", fg_color="#1f538d")
            self.cmd_entry.configure(placeholder_text="System ready. Type or speak command...")
            
            self.update_widgets()
            welcome_msg = f"Welcome {self.logged_in_user}! System diagnostics complete. All hardware operational. M S I initialized."
            self.speak(welcome_msg)
            self.log(f"MSI: Welcome {self.logged_in_user}!")
            self.log("MSI: Ready for commands. Click ACTIVATE VOICE and speak!")
            self.log(f"MSI: Energy threshold: {round(self.recognizer.energy_threshold, 2)}")
            
            # Start continuous widget updates
            self.update_stats_loop()
            
        except Exception as e:
            self.log(f"CRITICAL ERROR: {str(e)}")
            self.log("HELP: Ensure microphone is connected and accessible.")
            self.log("HELP: Check Windows Privacy Settings > Microphone > Allow apps")
            self.logo_label.configure(text="STATUS: HARDWARE ERROR", text_color="#ff0000")
            self.speak("Alert. Microphone hardware not detected.")

    def update_stats_loop(self):
        """Continuously update system stats"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            self.cpu_label.configure(text=f"CPU: {cpu}%")
            self.ram_label.configure(text=f"RAM: {ram}%")
            self.disk_label.configure(text=f"DISK: {disk}%")
            
            # Battery
            try:
                battery = psutil.sensors_battery()
                if battery:
                    self.battery_label.configure(text=f"BATTERY: {battery.percent}%")
            except:
                pass
                
        except:
            pass
        
        # Schedule next update
        self.after(5000, self.update_stats_loop)

    def update_widgets(self):
        """Fetch weather data"""
        def fetch():
            try:
                if WEATHER_API_KEY != "YOUR_OPENWEATHER_KEY":
                    w_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
                    w_data = requests.get(w_url, timeout=5).json()
                    temp = w_data['main']['temp']
                    desc = w_data['weather'][0]['description']
                    self.weather_label.configure(text=f"CITY: {CITY}\nTEMP: {temp}°C\n{desc.title()}")
                else:
                    self.weather_label.configure(text="WEATHER: API Key Required")
            except:
                self.weather_label.configure(text="WEATHER: Offline")
        threading.Thread(target=fetch, daemon=True).start()

    def execute_command(self, cmd):
        """Execute command through executor"""
        response = self.command_executor.execute(cmd)
        self.log(f"MSI: {response}")
        threading.Thread(target=self.speak, args=(response,), daemon=True).start()

    def execute_quick_command(self, cmd):
        """Execute quick action button"""
        self.log(f"QUICK ACTION: {cmd}")
        self.execute_command(cmd)

    def log(self, message):
        """Add message to console and save to history"""
        self.console.configure(state="normal")
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.console.insert("end", f"[{timestamp}] {message}\n")
        self.console.see("end")
        self.console.configure(state="disabled")
        
        # Save to chat history
        sender = "SYSTEM"
        if "YOU:" in message:
            sender = "USER"
        elif "MSI:" in message:
            sender = "MSI"
        
        self.chat_history.add_to_history(sender, message)

    def speak(self, text):
        """Text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass

    def toggle_voice_mode(self):
        """Toggle voice recognition"""
        if not self.is_listening:
            self.is_listening = True
            self.mic_button.configure(text="🛑 STOP LISTENING", fg_color="#a11d1d")
            self.log("VOICE MODE: ACTIVATED - Listening continuously...")
            threading.Thread(target=self.voice_recognition_loop, daemon=True).start()
        else:
            self.is_listening = False
            self.mic_button.configure(text="🎤 ACTIVATE VOICE", fg_color="#1f538d")
            self.log("VOICE MODE: DEACTIVATED")

    def voice_recognition_loop(self):
        """Continuous voice recognition"""
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.log("🎤 Listening... (Speak now)")
                    # Adjust for ambient noise briefly
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # Listen for longer phrases
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    self.log("🔄 Processing speech...")
                    text = self.recognizer.recognize_google(audio).lower()
                    self.log(f"✅ YOU: {text}")
                    
                    # Remove optional "msi" prefix if present
                    if text.startswith("msi "):
                        text = text[4:]
                    
                    self.execute_command(text)
                    
            except sr.WaitTimeoutError:
                self.log("⏱️ Timeout - No speech detected. Still listening...")
                continue
            except sr.UnknownValueError:
                self.log("❌ Could not understand audio. Please speak clearly.")
                continue
            except Exception as e:
                if self.is_listening:
                    self.log(f"⚠️ Voice error: {str(e)}")
                time.sleep(0.5)
            except Exception as e:
                if self.is_listening:
                    self.log(f"Voice error: {str(e)}")
                time.sleep(0.5)

    def process_text_command(self):
        """Process text input"""
        cmd = self.cmd_entry.get()
        if cmd:
            self.log(f"YOU: {cmd}")
            self.cmd_entry.delete(0, 'end')
            self.execute_command(cmd)
    
    def load_chat_sessions(self):
        """Load and display chat sessions in sidebar"""
        # Clear existing items
        for widget in self.chat_list_frame.winfo_children():
            widget.destroy()
        
        # Load sessions
        sessions = self.chat_history.load_previous_sessions()
        
        if not sessions:
            no_history_label = ctk.CTkLabel(self.chat_list_frame, 
                                           text="No previous chats\n\nStart chatting to\nsave history!", 
                                           font=("Consolas", 12),
                                           text_color="#888888",
                                           justify="center")
            no_history_label.pack(pady=50)
        else:
            # Display sessions (most recent first)
            for idx, session in enumerate(reversed(sessions), 1):
                session_file = session['file']
                messages = session['messages']
                
                # Create chat name
                chat_name = f"Chat {idx}"
                
                # Get first user message as preview
                preview = "No messages"
                for msg in messages:
                    if 'YOU:' in msg.get('message', '') or msg.get('sender') == 'USER':
                        preview = msg.get('message', '')[:50]
                        if len(msg.get('message', '')) > 50:
                            preview += "..."
                        break
                
                # Create button for this chat
                chat_btn = ctk.CTkButton(
                    self.chat_list_frame,
                    text=f"📝 {chat_name}\n{preview}",
                    width=260,
                    height=60,
                    fg_color="#2b2b2b",
                    hover_color="#3b3b3b",
                    font=("Consolas", 11),
                    anchor="w",
                    command=lambda s=session: self.load_chat_into_console(s)
                )
                chat_btn.pack(pady=5, padx=5, fill="x")
    
    def load_chat_into_console(self, session):
        """Load selected chat into main console"""
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        
        # Add session header
        session_name = session['file'].replace('session_', '').replace('.json', '')
        self.console.insert("end", f"📅 LOADED SESSION: {session_name}\n")
        self.console.insert("end", "=" * 60 + "\n\n")
        
        # Add all messages
        for msg in session['messages']:
            timestamp = msg.get('timestamp', 'N/A')
            message = msg.get('message', '')
            self.console.insert("end", f"[{timestamp}] {message}\n")
        
        self.console.insert("end", "\n" + "=" * 60 + "\n")
        self.console.insert("end", "End of session. Continue chatting below.\n")
        self.console.see("end")
        self.console.configure(state="disabled")
    
    def toggle_history_sidebar(self):
        """Toggle chat history sidebar visibility"""
        if self.history_sidebar_visible:
            self.history_sidebar.grid_forget()
            self.history_sidebar_visible = False
            self.history_toggle_button.configure(text="📜 SHOW HISTORY")
        else:
            self.history_sidebar.grid(row=0, column=2, rowspan=4, sticky="nsew", padx=0)
            self.history_sidebar_visible = True
            self.history_toggle_button.configure(text="📜 HIDE HISTORY")
            self.load_chat_sessions()  # Refresh the list
    
    def clear_console(self):
        """Clear the console"""
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        self.log("Console cleared.")

# ==================== MAIN ====================
if __name__ == "__main__":
    print("🚀 Starting MSI UI Application...")
    try:
        app = MSIApp()
        app.mainloop()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📦 Install required packages:")
        print("pip install customtkinter pyttsx3 speechrecognition pyaudio psutil")
        print("pip install pycaw comtypes screen-brightness-control pyautogui")
        input("\nPress Enter to exit...")
