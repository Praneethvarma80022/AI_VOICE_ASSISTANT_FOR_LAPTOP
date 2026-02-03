"""
MSI - INTEGRATED AI VOICE ASSISTANT
Complete system with login integrated into main UI
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
import sqlite3
import hashlib
import json
from PIL import ImageGrab

# Configuration
WEATHER_API_KEY = "e4fe22b06b47e80eca6159c4f6950f46"  # OpenWeatherMap API Key
CITY = "Vijayawada"

# Chat History Configuration (JSON-based like msi_ui.py)
HISTORY_DIR = Path.home() / ".msi_history"
HISTORY_DIR.mkdir(exist_ok=True)
# Note: CURRENT_SESSION_FILE will be set per user after login
CURRENT_SESSION_FILE = None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Database configuration
DB_PATH = Path.home() / ".msi_data" / "users.db"
DB_PATH.parent.mkdir(exist_ok=True)

# ==================== CHAT HISTORY MANAGER ====================
class ChatHistoryManager:
    """Manages chat history storage and retrieval - JSON based like msi_ui.py"""
    
    def __init__(self, username: str = None):
        self.history_dir = HISTORY_DIR
        self.current_session = []
        self.username = username
        self.current_session_file = None
        if username:
            self.set_user(username)
    
    def set_user(self, username: str):
        """Set the current user and create their session file"""
        self.username = username
        user_history_dir = self.history_dir / username
        user_history_dir.mkdir(exist_ok=True)
        self.current_session_file = user_history_dir / f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def load_previous_sessions(self, username: str = None):
        """Load chat history from previous sessions for a specific user"""
        try:
            all_sessions = []
            target_username = username or self.username
            if not target_username:
                return []
            
            user_history_dir = self.history_dir / target_username
            if user_history_dir.exists():
                for session_file in sorted(user_history_dir.glob("session_*.json")):
                    try:
                        with open(session_file, 'r', encoding='utf-8') as f:
                            session_data = json.load(f)
                            all_sessions.append({
                                'file': session_file.name,
                                'path': session_file,
                                'messages': session_data
                            })
                    except:
                        continue
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
            if self.current_session_file:
                with open(self.current_session_file, 'w', encoding='utf-8') as f:
                    json.dump(self.current_session, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def delete_session(self, session_path):
        """Delete a specific chat session file"""
        try:
            if os.path.exists(session_path):
                os.remove(session_path)
                return True
            return False
        except:
            return False

# ==================== DATABASE MANAGER ====================
class DatabaseManager:
    """Manage SQLite database for user authentication"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database initialization error: {e}")
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, email: str, password: str) -> tuple:
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                return False, "Username already exists!"
            
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                return False, "Email already registered!"
            
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            
            conn.commit()
            conn.close()
            return True, "Registration successful!"
        
        except Exception as e:
            return False, f"Registration error: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> tuple:
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False, "User not found!"
            
            password_hash = self.hash_password(password)
            if result[1] == password_hash:
                return True, "Login successful!"
            else:
                return False, "Incorrect password!"
        
        except Exception as e:
            return False, f"Login error: {str(e)}"

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

    def get_wifi_status(self):
        """Get WiFi connection status"""
        try:
            result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
            if "connected" in result.lower():
                for line in result.split('\n'):
                    if 'SSID' in line and 'BSSID' not in line:
                        ssid = line.split(':')[1].strip()
                        return f"Connected to WiFi: {ssid}"
            return "WiFi is disconnected"
        except:
            return "Could not check WiFi status"

    def toggle_wifi(self, enable: bool):
        """Enable or disable WiFi"""
        try:
            if enable:
                os.system("netsh interface set interface 'Wi-Fi' enable")
                return "WiFi enabled"
            else:
                os.system("netsh interface set interface 'Wi-Fi' disable")
                return "WiFi disabled"
        except:
            return "Could not toggle WiFi"
    
    def get_system_stats(self):
        """Get CPU, RAM, and Disk usage"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            return f"CPU: {cpu}%, RAM: {ram}%, Disk: {disk}%"
        except:
            return "Could not get system stats"

    def create_file(self, filename: str, location: str = "Desktop"):
        """Create a new file"""
        try:
            if location.lower() == "desktop":
                path = Path.home() / "Desktop" / filename
            else:
                path = Path(location) / filename
            path.touch()
            return f"Created {filename}"
        except Exception as e:
            return f"Could not create file: {str(e)}"

    def create_folder(self, foldername: str, location: str = "Desktop"):
        """Create a new folder"""
        try:
            if location.lower() == "desktop":
                path = Path.home() / "Desktop" / foldername
            else:
                path = Path(location) / foldername
            path.mkdir(exist_ok=True)
            return f"Created folder {foldername}"
        except Exception as e:
            return f"Could not create folder: {str(e)}"

    def empty_recycle_bin(self):
        """Empty the recycle bin"""
        try:
            import winshell
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            return "Recycle bin emptied"
        except:
            os.system("rd /s /q %systemdrive%\\$Recycle.bin")
            return "Recycle bin cleared"
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            path = Path.home() / "Desktop" / filename
            screenshot = ImageGrab.grab()
            screenshot.save(str(path))
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Could not take screenshot: {str(e)}"

    def list_running_apps(self):
        """List running applications"""
        try:
            apps = []
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc.info['name'] not in apps:
                        apps.append(proc.info['name'])
                except:
                    pass
            return f"Running {len(apps)} applications"
        except:
            return "Could not list applications"

    def close_application(self, app_name: str):
        """Close an application by name"""
        try:
            os.system(f"taskkill /f /im {app_name}.exe")
            return f"Closed {app_name}"
        except:
            return f"Could not close {app_name}"
    
    def set_brightness(self, level: int):
        """Set screen brightness (0-100)"""
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except:
            return "Could not set brightness"

    def get_disk_space(self):
        """Get available disk space"""
        try:
            total, used, free = shutil.disk_usage("/")
            total_gb = total // (2**30)
            free_gb = free // (2**30)
            used_gb = used // (2**30)
            return f"Total: {total_gb}GB, Used: {used_gb}GB, Free: {free_gb}GB"
        except:
            return "Could not get disk space"

    def open_website(self, url: str):
        """Open any website"""
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            webbrowser.open(url)
            return f"Opening {url}"
        except:
            return "Could not open website"
    
    def open_file(self, filename: str):
        """Open a file by name"""
        try:
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
            telegram_paths = [
                os.path.expandvars(r"%APPDATA%\Telegram Desktop\Telegram.exe"),
                r"C:\Program Files\Telegram Desktop\Telegram.exe",
                r"C:\Program Files (x86)\Telegram Desktop\Telegram.exe"
            ]

            if use_installed:
                for path in telegram_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path])
                        if person_name:
                            time.sleep(2)
                            webbrowser.open(f"tg://resolve?domain={person_name}")
                            return f"Opening Telegram (Installed) chat with {person_name}"
                        return "Opening Telegram (Installed)"
                return self.open_telegram_web(person_name)

            return self.open_telegram_web(person_name)

        except Exception as e:
            return f"Error opening Telegram: {str(e)}"

    def open_telegram_web(self, person_name: str = None):
        """Open Telegram Web version"""
        try:
            if person_name:
                webbrowser.open(f"https://t.me/{person_name}")
                return f"Opening Telegram chat with {person_name}"
            webbrowser.open("https://web.telegram.org")
            return "Opening Telegram Web"
        except:
            return "Could not open Telegram Web"
    
    def open_whatsapp(self, person_name: str = None, use_installed: bool = False):
        """Open WhatsApp - installed app or web version"""
        try:
            whatsapp_paths = [
                os.path.expandvars(r"%APPDATA%\WhatsApp\WhatsApp.exe"),
                r"C:\Program Files\WhatsApp\WhatsApp.exe",
                r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe"
            ]

            if use_installed:
                for path in whatsapp_paths:
                    if os.path.exists(path):
                        subprocess.Popen([path])
                        if person_name:
                            return f"Opening WhatsApp (Installed). Please search for {person_name}"
                        return "Opening WhatsApp (Installed)"
                return self.open_whatsapp_web(person_name)

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

# ==================== MAIN COMMAND EXECUTOR ====================
class CommandExecutor:
    """EXECUTES ALL COMMANDS"""
    
    def __init__(self):
        self.user = os.getlogin()
        self.advanced = AdvancedCommandExecutor()

    def _extract_contact(self, cmd: str, keywords) -> str:
        """Extract contact/person name from a command string."""
        person = cmd
        for keyword in keywords:
            person = person.replace(keyword, "")
        return " ".join(person.split()).strip()
    
    def execute(self, command: str) -> str:
        """Execute command - COMPLETE LAPTOP CONTROL"""
        cmd = command.lower().strip()
        
        # VOLUME CONTROL
        if "volume" in cmd or "sound" in cmd:
            if "up" in cmd or "increase" in cmd:
                return self.advanced.set_volume(100)
            elif "down" in cmd or "decrease" in cmd:
                return self.advanced.set_volume(20)
            elif "mute" in cmd or "zero" in cmd:
                return self.advanced.set_volume(0)
            elif "50" in cmd or "fifty" in cmd or "half" in cmd:
                return self.advanced.set_volume(50)
            else:
                words = cmd.split()
                for word in words:
                    if word.isdigit():
                        level = int(word)
                        if 0 <= level <= 100:
                            return self.advanced.set_volume(level)
                return "Specify volume level (0-100)"
        
        # BRIGHTNESS CONTROL
        elif "brightness" in cmd:
            if "up" in cmd or "high" in cmd:
                return self.advanced.set_brightness(100)
            elif "down" in cmd or "low" in cmd:
                return self.advanced.set_brightness(30)
            elif "50" in cmd or "medium" in cmd:
                return self.advanced.set_brightness(50)
            else:
                words = cmd.split()
                for word in words:
                    if word.isdigit():
                        level = int(word)
                        if 0 <= level <= 100:
                            return self.advanced.set_brightness(level)
                return "Specify brightness level (0-100)"
        
        # BATTERY & SYSTEM
        elif "battery" in cmd:
            return self.advanced.get_battery_status()
        elif "system stats" in cmd or "performance" in cmd:
            return self.advanced.get_system_stats()
        elif "screenshot" in cmd:
            return self.advanced.take_screenshot()
        
        # FILE & MESSAGING
        elif "open file" in cmd:
            filename = cmd.replace("open file", "").strip()
            if filename:
                return self.advanced.open_file(filename)
            return "Please specify a file name"
        elif "telegram" in cmd:
            person = self._extract_contact(
                cmd,
                ["telegram", "open", "chat", "message", "person", "on", "with", "to", "send", "installed"],
            )
            return self.advanced.open_telegram(person if person else None)
        elif "whatsapp" in cmd:
            person = self._extract_contact(
                cmd,
                ["whatsapp", "open", "chat", "message", "person", "on", "with", "to", "send", "installed"],
            )
            return self.advanced.open_whatsapp(person if person else None)
        
        # APPLICATIONS
        elif "open notepad" in cmd:
            os.system("start notepad")
            return "Opening Notepad"
        elif "open calculator" in cmd:
            os.system("start calc")
            return "Opening Calculator"
        elif "open chrome" in cmd:
            os.system("start chrome")
            return "Opening Chrome"
        elif "task manager" in cmd:
            os.system("taskmgr")
            return "Opening Task Manager"
        
        # SYSTEM CONTROL
        elif "shutdown" in cmd:
            os.system("shutdown /s /t 5")
            return "Shutting down in 5 seconds!"
        elif "restart" in cmd:
            os.system("shutdown /r /t 5")
            return "Restarting in 5 seconds!"
        elif "lock" in cmd:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "Computer locked!"
        
        # WEB
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
        
        # TIME & DATE
        elif "time" in cmd:
            current = datetime.datetime.now().strftime("%I:%M %p")
            return f"The time is {current}"
        elif "date" in cmd:
            current = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current}"
        
        # GREETINGS
        elif any(word in cmd for word in ["hello", "hi", "hey"]):
            return f"Hello {self.user}! How can I assist you?"
        elif "how are you" in cmd:
            return "All systems operational! Ready to assist."
        elif "your name" in cmd:
            return "I am MSI, your advanced AI voice assistant!"
        
        else:
            return f"Command not recognized: '{cmd}'"

# ==================== INTEGRATED MSI APPLICATION ====================
class MSIIntegratedApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("M.S.I. AI Voice Assistant")
        self.geometry("1420x750")  # 280 + 840 + 300px width
        
        # Initialize database
        self.db = DatabaseManager()
        self.chat_history = ChatHistoryManager()
        
        # State variables
        self.logged_in = False
        self.username = None
        self.is_listening = False
        self.history_sidebar_visible = False
        
        # Show login first
        self.show_login_screen()
    
    def show_login_screen(self):
        """Show login/register screen"""
        # Clear window
        for widget in self.winfo_children():
            widget.destroy()
        
        # Main frame
        self.login_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.login_frame.pack(fill="both", expand=True)
        
        # Header
        ctk.CTkLabel(
            self.login_frame,
            text="🤖 MSI AI VOICE ASSISTANT",
            font=("Orbitron", 28, "bold"),
            text_color="#00d4ff"
        ).pack(pady=40)
        
        # Content frame
        content = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        content.pack(expand=True)
        
        # Title
        self.title_label = ctk.CTkLabel(
            content,
            text="LOGIN",
            font=("Orbitron", 22, "bold"),
            text_color="#ffcc00"
        )
        self.title_label.pack(pady=20)
        
        # Username
        ctk.CTkLabel(content, text="Username", font=("Consolas", 12), text_color="#00ff00").pack(pady=(10, 5))
        self.username_entry = ctk.CTkEntry(content, placeholder_text="Enter username", height=40, width=350,
                                          font=("Consolas", 12), border_color="#00d4ff", border_width=2)
        self.username_entry.pack(pady=(0, 15))
        
        # Password
        ctk.CTkLabel(content, text="Password", font=("Consolas", 12), text_color="#00ff00").pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(content, placeholder_text="Enter password", height=40, width=350,
                                          font=("Consolas", 12), border_color="#00d4ff", border_width=2, show="•")
        self.password_entry.pack(pady=(0, 15))
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Email (hidden initially)
        self.email_label = ctk.CTkLabel(content, text="Email", font=("Consolas", 12), text_color="#00ff00")
        self.email_entry = ctk.CTkEntry(content, placeholder_text="Enter email", height=40, width=350,
                                       font=("Consolas", 12), border_color="#00d4ff", border_width=2)
        
        # Status
        self.status_label = ctk.CTkLabel(content, text="", font=("Consolas", 11))
        self.status_label.pack(pady=10)
        
        # Buttons
        self.login_button = ctk.CTkButton(content, text="LOGIN", height=45, width=350,
                                         font=("Orbitron", 16, "bold"), fg_color="#1f538d",
                                         command=self.handle_login)
        self.login_button.pack(pady=10)
        
        self.register_button = ctk.CTkButton(content, text="CREATE ACCOUNT", height=40, width=350,
                                            font=("Orbitron", 14, "bold"), fg_color="#1d5f1d",
                                            command=self.toggle_register_mode)
        self.register_button.pack(pady=5)
        
        self.mode = "login"
    
    def toggle_register_mode(self):
        """Toggle between login and register"""
        if self.mode == "login":
            self.mode = "register"
            self.title_label.configure(text="CREATE ACCOUNT")
            self.login_button.configure(text="REGISTER", command=self.handle_register)
            self.register_button.configure(text="Back to Login", command=self.toggle_register_mode)
            self.email_label.pack(pady=(10, 5))
            self.email_entry.pack(pady=(0, 15))
            self.status_label.configure(text="")
        else:
            self.mode = "login"
            self.title_label.configure(text="LOGIN")
            self.login_button.configure(text="LOGIN", command=self.handle_login)
            self.register_button.configure(text="CREATE ACCOUNT", command=self.toggle_register_mode)
            self.email_label.pack_forget()
            self.email_entry.pack_forget()
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.status_label.configure(text="")
    
    def handle_login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.status_label.configure(text="❌ Please enter username and password!", text_color="#ff6b6b")
            return
        
        success, message = self.db.authenticate_user(username, password)
        
        if success:
            self.status_label.configure(text="✅ " + message, text_color="#00ff00")
            self.username = username
            self.logged_in = True
            # Set user for chat history
            self.chat_history.set_user(username)
            self.after(1000, self.show_msi_interface)
        else:
            self.status_label.configure(text="❌ " + message, text_color="#ff6b6b")
    
    def handle_register(self):
        """Handle registration"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not email or not password:
            self.status_label.configure(text="❌ Please fill all fields!", text_color="#ff6b6b")
            return
        
        if len(password) < 6:
            self.status_label.configure(text="❌ Password must be at least 6 characters!", text_color="#ff6b6b")
            return
        
        if "@" not in email:
            self.status_label.configure(text="❌ Invalid email address!", text_color="#ff6b6b")
            return
        
        success, message = self.db.register_user(username, email, password)
        
        if success:
            self.status_label.configure(text="✅ " + message + " Please login.", text_color="#00ff00")
            self.after(1500, self.toggle_register_mode)
        else:
            self.status_label.configure(text="❌ " + message, text_color="#ff6b6b")
    
    def show_msi_interface(self):
        """Show main MSI interface after login"""
        # Clear login screen
        for widget in self.winfo_children():
            widget.destroy()
        
        # Update title
        self.title(f"M.S.I. Control System - Welcome {self.username}")
        
        # Initialize voice systems
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.command_executor = CommandExecutor()
        
        # Setup UI
        self.setup_msi_ui()
        
        # Start diagnostics
        threading.Thread(target=self.run_startup_diagnostics, daemon=True).start()
    
    def setup_msi_ui(self):
        """Setup MSI UI"""
        self.grid_columnconfigure(0, weight=0, minsize=280)  # Left sidebar
        self.grid_columnconfigure(1, weight=1)               # Main console (expand)
        self.grid_columnconfigure(2, weight=0, minsize=300)  # Right sidebar
        self.grid_rowconfigure(1, weight=1)

        # LEFT SIDEBAR (System Widgets)
        sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#1a1a1a")
        sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=0)
        sidebar.grid_propagate(False)
        
        ctk.CTkLabel(sidebar, text="SYSTEM WIDGETS", font=("Orbitron", 20, "bold"), 
                    text_color="#00d4ff").pack(pady=20)
        
        # System Stats
        stats_frame = ctk.CTkFrame(sidebar, fg_color="#0a0a0a", corner_radius=10)
        stats_frame.pack(pady=10, padx=15, fill="x")
        
        self.cpu_label = ctk.CTkLabel(stats_frame, text="CPU: ---%", font=("Consolas", 12), text_color="#00ff00")
        self.cpu_label.pack(pady=5, padx=10, anchor="w")
        
        self.ram_label = ctk.CTkLabel(stats_frame, text="RAM: ---%", font=("Consolas", 12), text_color="#00ff00")
        self.ram_label.pack(pady=5, padx=10, anchor="w")
        
        self.disk_label = ctk.CTkLabel(stats_frame, text="DISK: ---%", font=("Consolas", 12), text_color="#00ff00")
        self.disk_label.pack(pady=5, padx=10, anchor="w")
        
        # Battery
        battery_frame = ctk.CTkFrame(sidebar, fg_color="#0a0a0a", corner_radius=10)
        battery_frame.pack(pady=10, padx=15, fill="x")
        
        self.battery_label = ctk.CTkLabel(battery_frame, text="BATTERY: ---%", font=("Consolas", 12), text_color="#ffcc00")
        self.battery_label.pack(pady=10, padx=10)
        
        # Weather
        weather_frame = ctk.CTkFrame(sidebar, fg_color="#0a0a0a", corner_radius=10)
        weather_frame.pack(pady=10, padx=15, fill="x")
        
        self.weather_label = ctk.CTkLabel(weather_frame, text="WEATHER: Loading...", 
                                         font=("Consolas", 11), justify="left")
        self.weather_label.pack(pady=10, padx=10)
        
        # Quick Actions
        quick_frame = ctk.CTkFrame(sidebar, fg_color="#0a0a0a", corner_radius=10)
        quick_frame.pack(pady=10, padx=15, fill="x")
        
        ctk.CTkLabel(quick_frame, text="QUICK ACTIONS", font=("Orbitron", 12, "bold"), text_color="#00d4ff").pack(pady=5)
        
        ctk.CTkButton(quick_frame, text="📸 Screenshot", width=200,
                     command=lambda: self.execute_quick_command("screenshot")).pack(pady=3)
        ctk.CTkButton(quick_frame, text="🔊 Volume 50%", width=200,
                     command=lambda: self.execute_quick_command("volume 50")).pack(pady=3)
        ctk.CTkButton(quick_frame, text="💡 Brightness 50%", width=200,
                     command=lambda: self.execute_quick_command("brightness 50")).pack(pady=3)

        # MAIN CONSOLE (CENTER)
        self.logo_label = ctk.CTkLabel(self, text="SYSTEM STATUS: INITIALIZING", 
                                       font=("Orbitron", 24, "bold"), text_color="#ffcc00")
        self.logo_label.grid(row=0, column=1, padx=30, pady=(20, 10))
        
        self.console = ctk.CTkTextbox(self, fg_color="#0a0a0a", border_color="#00d4ff", 
                                      border_width=2, font=("Consolas", 13), text_color="#00ff00")
        self.console.grid(row=1, column=1, padx=30, pady=10, sticky="nsew")
        self.console.configure(state="disabled")

        # INPUT/BUTTONS
        self.cmd_entry = ctk.CTkEntry(self, placeholder_text="Awaiting system check...", 
                                      height=40, font=("Consolas", 14), border_color="#00d4ff", border_width=2)
        self.cmd_entry.grid(row=2, column=1, padx=30, pady=10, sticky="ew")
        self.cmd_entry.bind("<Return>", lambda e: self.process_text_command())
        
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=1, pady=(10, 20))
        
        self.mic_button = ctk.CTkButton(button_frame, text="🎤 TESTING MIC...", state="disabled",
                                       command=self.toggle_voice_mode, fg_color="#555555", width=180, height=40,
                                       font=("Orbitron", 14, "bold"))
        self.mic_button.pack(side="left", padx=10)
        
        ctk.CTkButton(button_frame, text="🗑️ CLEAR LOG", command=self.clear_console, width=150, height=40,
                     font=("Orbitron", 14, "bold"), fg_color="#a11d1d").pack(side="left", padx=10)
        
        self.history_toggle_button = ctk.CTkButton(button_frame, text="📜 SHOW HISTORY", 
                                                   command=self.toggle_history_sidebar, width=180, height=40,
                                                   font=("Orbitron", 14, "bold"), fg_color="#1f538d")
        self.history_toggle_button.pack(side="left", padx=10)
        
        ctk.CTkButton(button_frame, text="🚪 LOGOUT", command=self.logout_user, width=150, height=40,
                     font=("Orbitron", 14, "bold"), fg_color="#8b0000").pack(side="left", padx=10)
        
        # RIGHT SIDEBAR (Chat History)
        self.setup_chat_history_sidebar()

    def setup_chat_history_sidebar(self):
        """Setup right sidebar for chat history"""
        self.history_sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="#1a1a1a")
        # Don't grid it initially - will be shown when toggle button is clicked
        self.history_sidebar.grid_propagate(False)
        
        # Header
        ctk.CTkLabel(self.history_sidebar, text="CHAT HISTORY", 
                    font=("Orbitron", 18, "bold"), text_color="#00d4ff").pack(pady=15)
        
        # Scrollable chat list
        self.chat_list_frame = ctk.CTkScrollableFrame(self.history_sidebar, 
                                                      fg_color="#0a0a0a",
                                                      corner_radius=10,
                                                      border_color="#00d4ff",
                                                      border_width=2)
        self.chat_list_frame.pack(pady=10, padx=15, fill="both", expand=True)
        
        # Refresh button
        ctk.CTkButton(self.history_sidebar, text="🔄 Refresh History", 
                     command=self.load_chat_sessions,
                     width=250, fg_color="#1f538d").pack(pady=10)
        
        # Load initial chat sessions
        self.load_chat_sessions()
    
    def load_chat_sessions(self):
        """Load and display chat sessions in sidebar for current user"""
        # Clear existing items
        for widget in self.chat_list_frame.winfo_children():
            widget.destroy()
        
        # Load sessions for current user only
        sessions = self.chat_history.load_previous_sessions(self.username)
        
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
                session_path = session['path']
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
                
                # Create frame for button and delete button
                btn_frame = ctk.CTkFrame(self.chat_list_frame, fg_color="transparent", height=60)
                btn_frame.pack(pady=5, padx=5, fill="x", expand=False)
                btn_frame.pack_propagate(False)
                
                # Create button for this chat (expandable)
                chat_btn = ctk.CTkButton(
                    btn_frame,
                    text=f"📝 {chat_name}\n{preview}",
                    width=180,
                    height=60,
                    fg_color="#2b2b2b",
                    hover_color="#3b3b3b",
                    font=("Consolas", 10),
                    anchor="w",
                    command=lambda s=session: self.load_chat_into_console(s)
                )
                chat_btn.pack(side="left", fill="both", expand=True, padx=(0, 2))
                
                # Delete button
                delete_btn = ctk.CTkButton(
                    btn_frame,
                    text="🗑️",
                    width=50,
                    height=60,
                    fg_color="#a11d1d",
                    hover_color="#cc0000",
                    command=lambda p=session_path: self.delete_chat_session(p)
                )
                delete_btn.pack(side="right", padx=(2, 0), fill="y")
    
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
    
    def delete_chat_session(self, session_path):
        """Delete a chat session and refresh the sidebar"""
        if self.chat_history.delete_session(session_path):
            self.log("📝 Chat session deleted successfully.")
            self.load_chat_sessions()  # Refresh the sidebar
        else:
            self.log("❌ Failed to delete chat session.")
    
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
    
    def update_widgets(self):
        """Fetch weather data"""
        def fetch():
            try:
                # Fetch weather only if a valid API key is configured
                if WEATHER_API_KEY and WEATHER_API_KEY != "e4fe22b06b47e80eca6159c4f6950f46":
                    w_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
                    w_data = requests.get(w_url, timeout=5).json()
                    temp = w_data['main']['temp']
                    desc = w_data['weather'][0]['description']
                    self.after(0, lambda: self.weather_label.configure(
                        text=f"CITY: {CITY}\nTEMP: {temp}°C\n{desc.title()}"
                    ))
                else:
                    self.after(0, lambda: self.weather_label.configure(
                        text=f"WEATHER: Set API Key\nin msi_integrated.py"
                    ))
            except Exception as e:
                self.after(0, lambda: self.weather_label.configure(
                    text=f"WEATHER: Offline\n({str(e)[:20]})"
                ))
        threading.Thread(target=fetch, daemon=True).start()
    
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
    
    def run_startup_diagnostics(self):
        """Perform hardware and mic check before starting"""
        self.log("DIAGNOSTICS: Starting Microphone Test...")
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
            welcome_msg = f"Welcome {self.username}! System diagnostics complete. All hardware operational. M S I initialized."
            self.speak(welcome_msg)
            self.log(f"MSI: Welcome {self.username}!")
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

    def execute_command(self, cmd):
        """Execute command"""
        response = self.command_executor.execute(cmd)
        self.log(f"MSI: {response}")
        
        # Refresh sidebar if visible (JSON history auto-saves via add_to_history)
        if self.history_sidebar_visible:
            self.after(0, self.load_chat_sessions)
        
        threading.Thread(target=self.speak, args=(response,), daemon=True).start()

    def execute_quick_command(self, cmd):
        """Execute quick action"""
        self.log(f"QUICK ACTION: {cmd}")
        self.execute_command(cmd)

    def log(self, message):
        """Add message to console and save to history"""
        if threading.current_thread() is not threading.main_thread():
            self.after(0, self.log, message)
            return

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
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    self.log("🔄 Processing speech...")
                    text = self.recognizer.recognize_google(audio).lower()
                    self.log(f"✅ YOU: {text}")
                    
                    if text.startswith("msi "):
                        text = text[4:]
                    
                    self.execute_command(text)
                    
            except sr.WaitTimeoutError:
                self.log("⏱️ Timeout - Still listening...")
                continue
            except sr.UnknownValueError:
                self.log("❌ Could not understand audio.")
                continue
            except Exception as e:
                if self.is_listening:
                    self.log(f"⚠️ Voice error: {str(e)}")
                time.sleep(0.5)

    def process_text_command(self):
        """Process text input"""
        cmd = self.cmd_entry.get()
        if cmd:
            self.log(f"YOU: {cmd}")
            self.cmd_entry.delete(0, 'end')
            self.execute_command(cmd)
    
    def clear_console(self):
        """Clear console"""
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        self.log("Console cleared.")
    
    def logout_user(self):
        """Logout current user and return to login screen"""
        # Stop voice recognition if active
        if self.is_listening:
            self.is_listening = False
        
        # Log the logout action
        self.log(f"MSI: User '{self.username}' logging out...")
        
        # Reset user state
        self.logged_in = False
        self.username = None
        
        # Reset UI
        self.show_login_screen()
    
    def show_chat_history(self):
        """Display chat history in popup window"""
        history_window = ctk.CTkToplevel(self)
        history_window.title(f"Chat History - {self.username}")
        history_window.geometry("700x600")
        
        # Header
        header = ctk.CTkLabel(history_window, text=f"📜 CHAT HISTORY - {self.username}", 
                             font=("Orbitron", 20, "bold"), text_color="#00d4ff")
        header.pack(pady=15)
        
        # History display
        history_text = ctk.CTkTextbox(history_window, fg_color="#0a0a0a", 
                                     border_color="#00d4ff", border_width=2,
                                     font=("Consolas", 12), text_color="#00ff00")
        history_text.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Load history
        try:
            history = self.history_manager.get_user_history(self.username, limit=100)
            if history:
                for entry in history:
                    timestamp = entry[4]
                    user_msg = entry[2]
                    bot_msg = entry[3]
                    
                    history_text.insert("end", f"\n[{timestamp}]\n", "timestamp")
                    history_text.insert("end", f"YOU: {user_msg}\n", "user")
                    history_text.insert("end", f"MSI: {bot_msg}\n\n", "bot")
                    history_text.insert("end", "─" * 70 + "\n", "separator")
                
                history_text.tag_config("timestamp", foreground="#ffcc00")
                history_text.tag_config("user", foreground="#00d4ff")
                history_text.tag_config("bot", foreground="#00ff00")
                history_text.tag_config("separator", foreground="#333333")
            else:
                history_text.insert("end", "\nNo chat history found.\n\nStart giving commands to build your history!")
        except Exception as e:
            history_text.insert("end", f"\nError loading history: {e}")
        
        history_text.configure(state="disabled")
        
        # Buttons
        btn_frame = ctk.CTkFrame(history_window, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Clear History", 
                     command=lambda: self.clear_history(history_window),
                     fg_color="#ff3333", hover_color="#cc0000").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Close", 
                     command=history_window.destroy).pack(side="left", padx=5)
    
    def clear_history(self, window):
        """Clear chat history for current user"""
        try:
            self.history_manager.clear_user_history(self.username)
            self.log("Chat history cleared!")
            window.destroy()
        except Exception as e:
            self.log(f"Error clearing history: {e}")

# ==================== MAIN ====================
if __name__ == "__main__":
    print("🚀 Starting MSI Integrated System...")
    try:
        app = MSIIntegratedApp()
        app.mainloop()
    except Exception as e:
        print(f"❌ Error: {e}")
        input("\nPress Enter to exit...")
