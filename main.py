import os
import sys
import time
import datetime
import subprocess
import webbrowser
import random
import winreg
import ctypes
from pathlib import Path
import shutil
import psutil

print("🤖 Initializing MSI...")

# Simple imports
try:
    import pyttsx3
    import speech_recognition as sr
    print("✅ Voice modules loaded")
except ImportError:
    print("❌ Install: pip install pyttsx3 speechrecognition")
    sys.exit(1)

# ==================== SIMPLE WORKING VOICE ====================
class VoiceSystem:
    def __init__(self):
        # Setup TTS
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 1.0)
        
        # Setup recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        
        print("✅ Voice ready")
    
    def speak(self, text: str):
        """Speak text"""
        print(f"\n🤖 MSI: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self) -> str:
        """Listen for command"""
        try:
            with sr.Microphone() as source:
                print("\n🎤 Listening... (Speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"✅ Heard: {text}")
                return text
                
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return ""
        except Exception as e:
            print(f"⚠️ Listen error: {e}")
            return ""

# ==================== ADVANCED LAPTOP CONTROL COMMANDS ====================
class AdvancedCommandExecutor:
    """COMPLETE LAPTOP CONTROL - A TO Z"""
    
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
            # Fallback method using nircmd if available
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
                # Extract SSID
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
            # Fallback
            os.system("rd /s /q %systemdrive%\\$Recycle.bin")
            return "Recycle bin cleared"
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            import pyautogui
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            path = Path.home() / "Desktop" / filename
            pyautogui.screenshot(str(path))
            return f"Screenshot saved to Desktop as {filename}"
        except:
            return "Could not take screenshot. Install pyautogui: pip install pyautogui"
    
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
            return "Could not set brightness. Install: pip install screen-brightness-control"
    
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
    
    def open_telegram(self, person_name: str = None):
        """Open Telegram and optionally open a chat"""
        try:
            # Try to find Telegram executable
            telegram_paths = [
                os.path.expandvars(r"%APPDATA%\Telegram Desktop\Telegram.exe"),
                r"C:\Program Files\Telegram Desktop\Telegram.exe",
                r"C:\Program Files (x86)\Telegram Desktop\Telegram.exe"
            ]
            
            telegram_opened = False
            for path in telegram_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    telegram_opened = True
                    
                    if person_name:
                        # Wait a bit for Telegram to open
                        time.sleep(2)
                        # Try to open chat using telegram:// protocol
                        webbrowser.open(f"tg://resolve?domain={person_name}")
                        return f"Opening Telegram chat with {person_name}"
                    return "Opening Telegram"
            
            # If not found, try web version
            if not telegram_opened:
                webbrowser.open("https://web.telegram.org")
                return "Opening Telegram Web"
        except Exception as e:
            return f"Error opening Telegram: {str(e)}"
    
    def open_whatsapp(self, person_name: str = None):
        """Open WhatsApp"""
        try:
            webbrowser.open("https://web.whatsapp.com")
            if person_name:
                return f"Opening WhatsApp. Please search for {person_name}"
            return "Opening WhatsApp Web"
        except:
            return "Could not open WhatsApp"

# ==================== ENHANCED COMMAND EXECUTOR ====================
class CommandExecutor:
    """EXECUTES ALL COMMANDS"""
    
    def __init__(self):
        self.user = os.getlogin()
        self.advanced = AdvancedCommandExecutor()
    
    def execute(self, command: str) -> str:
        """Execute command - COMPLETE LAPTOP CONTROL"""
        cmd = command.lower().strip()
        print(f"⚡ Executing: {cmd}")
        
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
                # Try to extract number
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
        elif "battery" in cmd or "power" in cmd:
            return self.advanced.get_battery_status()
        
        # ========== WIFI CONTROL ==========
        elif "wifi" in cmd or "wi-fi" in cmd:
            if "status" in cmd or "check" in cmd:
                return self.advanced.get_wifi_status()
            elif "on" in cmd or "enable" in cmd or "connect" in cmd:
                return self.advanced.toggle_wifi(True)
            elif "off" in cmd or "disable" in cmd or "disconnect" in cmd:
                return self.advanced.toggle_wifi(False)
            else:
                return self.advanced.get_wifi_status()
        
        # ========== SYSTEM STATS ==========
        elif "system stats" in cmd or "performance" in cmd or "cpu" in cmd or "ram" in cmd:
            return self.advanced.get_system_stats()
        
        elif "disk space" in cmd or "storage" in cmd or "space" in cmd:
            return self.advanced.get_disk_space()
        
        # ========== FILE & FOLDER OPERATIONS ==========
        elif "create file" in cmd:
            filename = cmd.replace("create file", "").strip()
            if not filename:
                filename = f"newfile_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            return self.advanced.create_file(filename)
        
        elif "create folder" in cmd or "new folder" in cmd:
            foldername = cmd.replace("create folder", "").replace("new folder", "").strip()
            if not foldername:
                foldername = f"NewFolder_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            return self.advanced.create_folder(foldername)
        
        elif "empty recycle bin" in cmd or "clear recycle" in cmd:
            return self.advanced.empty_recycle_bin()
        
        # ========== OPEN FILE ==========
        elif "open file" in cmd:
            filename = cmd.replace("open file", "").strip()
            if filename:
                return self.advanced.open_file(filename)
            return "Please specify a file name"
        
        # ========== TELEGRAM ==========
        elif "telegram" in cmd or "open telegram" in cmd:
            if "chat" in cmd or "message" in cmd or "person" in cmd:
                # Extract person name after removing keywords
                person = cmd.replace("telegram", "").replace("open", "").replace("chat", "").replace("message", "").replace("person", "").replace("with", "").strip()
                return self.advanced.open_telegram(person if person else None)
            return self.advanced.open_telegram()
        
        # ========== WHATSAPP ==========
        elif "whatsapp" in cmd or "open whatsapp" in cmd:
            if "chat" in cmd or "message" in cmd or "person" in cmd:
                person = cmd.replace("whatsapp", "").replace("open", "").replace("chat", "").replace("message", "").replace("person", "").replace("with", "").strip()
                return self.advanced.open_whatsapp(person if person else None)
            return self.advanced.open_whatsapp()
            if not filename:
                filename = f"newfile_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            return self.advanced.create_file(filename)
        
        elif "create folder" in cmd or "new folder" in cmd:
            foldername = cmd.replace("create folder", "").replace("new folder", "").strip()
            if not foldername:
                foldername = f"NewFolder_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            return self.advanced.create_folder(foldername)
        
        elif "empty recycle bin" in cmd or "clear recycle" in cmd:
            return self.advanced.empty_recycle_bin()
        
        # ========== SCREENSHOT ==========
        elif "screenshot" in cmd or "screen shot" in cmd or "capture screen" in cmd:
            return self.advanced.take_screenshot()
        
        # ========== APPLICATION MANAGEMENT ==========
        elif "close" in cmd and ("chrome" in cmd or "firefox" in cmd or "notepad" in cmd or "calculator" in cmd):
            if "chrome" in cmd:
                return self.advanced.close_application("chrome")
            elif "firefox" in cmd:
                return self.advanced.close_application("firefox")
            elif "notepad" in cmd:
                return self.advanced.close_application("notepad")
            elif "calculator" in cmd:
                return self.advanced.close_application("calculator")
        
        elif "list apps" in cmd or "running apps" in cmd:
            return self.advanced.list_running_apps()
        
        # ========== WEBSITE OPENING ==========
        elif "open website" in cmd or "visit" in cmd or "go to" in cmd:
            url = cmd.replace("open website", "").replace("visit", "").replace("go to", "").strip()
            if url:
                return self.advanced.open_website(url)
            return "Please specify a website"
        
        # ========== FOLDER COMMANDS ==========
        if "open folder" in cmd:
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
            
            else:
                try:
                    os.startfile(folder)
                    return f"Opened {folder}"
                except:
                    return f"Could not open {folder}"
        
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
        
        elif "open cmd" in cmd or "open command" in cmd:
            os.system("start cmd")
            return "Opening Command Prompt"
        
        elif "open chrome" in cmd:
            os.system("start chrome")
            return "Opening Chrome"
        
        elif "open firefox" in cmd:
            os.system("start firefox")
            return "Opening Firefox"
        
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
        
        elif "sleep" in cmd:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "Going to sleep..."
        
        # ========== WEB BROWSING ==========
        elif "open youtube" in cmd:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube"
        
        elif "open google" in cmd:
            webbrowser.open("https://google.com")
            return "Opening Google"
        
        elif "open facebook" in cmd:
            webbrowser.open("https://facebook.com")
            return "Opening Facebook"
        
        elif "open instagram" in cmd:
            webbrowser.open("https://instagram.com")
            return "Opening Instagram"
        
        # ========== VIDEO SEARCH ==========
        elif "find video" in cmd or "search video" in cmd or "video" in cmd:
            if "find video" in cmd:
                query = cmd.replace("find video", "").strip()
            elif "search video" in cmd:
                query = cmd.replace("search video", "").strip()
            else:
                query = cmd.replace("video", "").strip()
            
            if query:
                search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                return f"Searching YouTube for: {query}"
            else:
                webbrowser.open("https://youtube.com")
                return "Opening YouTube"
        
        elif cmd.startswith("search "):
            query = cmd[7:].strip()
            webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
            return f"Searching: {query}"
        
        elif cmd.startswith("play "):
            query = cmd[5:].strip()
            webbrowser.open(f"https://youtube.com/results?search_query={query.replace(' ', '+')}")
            return f"Playing: {query}"
        
        # ========== CONTROL PANEL ==========
        elif "control panel" in cmd:
            os.system("control")
            return "Opening Control Panel"
        
        elif "task manager" in cmd:
            os.system("taskmgr")
            return "Opening Task Manager"
        
        # ========== FILE EXPLORER ==========
        elif "open computer" in cmd or "open file explorer" in cmd:
            os.system("explorer")
            return "Opening File Explorer"
        
        elif "recycle bin" in cmd or "open bin" in cmd:
            os.system("explorer shell:RecycleBinFolder")
            return "Opening Recycle Bin"
        
        # ========== TIME & DATE ==========
        elif "time" in cmd or "what time" in cmd:
            current = datetime.datetime.now().strftime("%I:%M %p")
            return f"The time is {current}"
        
        elif "date" in cmd or "today's date" in cmd:
            current = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current}"
        
        # ========== SYSTEM INFO ==========
        elif "system info" in cmd or "computer info" in cmd:
            info = f"""
            User: {self.user}
            Time: {datetime.datetime.now().strftime('%I:%M:%S %p')}
            Date: {datetime.datetime.now().strftime('%B %d, %Y')}
            Current Directory: {os.getcwd()}
            OS: {sys.platform}
            """
            return info.strip()
        
        # ========== JOKES ==========
        elif "joke" in cmd or "tell joke" in cmd:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the computer go to the doctor? Because it had a virus!",
                "What do you call a fake noodle? An impasta!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "What's a computer's favorite snack? Microchips!",
            ]
            return random.choice(jokes)
        
        # ========== HELP ==========
        elif "help" in cmd or "what can you do" in cmd:
            help_text = """I can control your entire laptop! Here's what I can do:

🔊 VOLUME CONTROL:
• Volume up/down/mute/50/100
• Set volume [number]

💡 BRIGHTNESS:
• Brightness up/down/50/100
• Set brightness [number]

🔋 POWER & BATTERY:
• Battery status
• WiFi on/off/status
• System stats
• Disk space

📁 FILE & FOLDER OPERATIONS:
• Create file [name]
• Create folder [name]
• Open folder desktop/documents/downloads
• Empty recycle bin
• Open file explorer

📸 SCREEN:
• Take screenshot
• Screen brightness controls

🖥️ APPLICATIONS:
• Open notepad/calculator/paint/cmd
• Open chrome/firefox
• Close [app name]
• List running apps
• Task manager

🌐 WEB BROWSING:
• Open youtube/google/facebook/instagram
• Open website [url]
• Search [query]
• Find video [query]
• Play [song/video name]

⚙️ SYSTEM CONTROL:
• Shutdown/restart/lock/sleep
• Control panel
• Task manager

📅 INFORMATION:
• Time/date
• System info
• Performance stats
• Tell jokes

No wake word needed - just speak your command!"""

            return help_text
        
        # ========== GREETINGS ==========
        elif any(word in cmd for word in ["hello", "hi", "hey"]):
            greetings = [f"Hello {self.user}!", f"Hi {self.user}!", f"Hey {self.user}!"]
            return random.choice(greetings)
        
        elif "how are you" in cmd:
            responses = ["I'm working perfectly! Ready to help.", "All systems operational!", "Feeling great! What can I do for you?"]
            return random.choice(responses)
        
        elif "thank you" in cmd or "thanks" in cmd:
            return "You're welcome!"
        
        elif "your name" in cmd:
            return "I am MSI, your advanced AI voice assistant!"
        
        # ========== DEFAULT ==========
        else:
            return f"I heard '{cmd}'. Try saying 'help' to see what I can do."

# ==================== MAIN MSI ====================
class MSI:
    """Advanced AI Voice Assistant with Complete Laptop Control"""
    
    def __init__(self):
        print("="*60)
        print("🤖 MSI - ADVANCED AI VOICE ASSISTANT")
        print("="*60)
        print("✅ Complete Laptop Control System Active!")
        print("="*60)
        
        self.voice = VoiceSystem()
        self.commands = CommandExecutor()
        self.running = True
        
        self.start()
    
    def start(self):
        """Start MSI"""
        self.voice.speak("Initialization complete. Hello! I am MSI, your advanced AI voice assistant. Just speak naturally, I will understand your commands!")
        
        print("\n" + "="*60)
        print("✅ MSI IS ACTIVE - Just speak your commands:")
        print("\n💡 EXAMPLES (No wake word needed!):")
        print("• 'volume 50' or 'set volume to 50'")
        print("• 'brightness high' or 'increase brightness'")
        print("• 'battery status' or 'check battery'")
        print("• 'take screenshot' or 'screenshot'")
        print("• 'open notepad' or 'launch notepad'")
        print("• 'wifi status' or 'check wifi'")
        print("• 'system stats' or 'performance'")
        print("• 'help' - See all commands")
        print("\n🛑 Say 'exit' or 'quit' to stop")
        print("="*60 + "\n")
        
        self.main_loop()
    
    def main_loop(self):
        """Main loop"""
        while self.running:
            try:
                # Listen for command
                text = self.voice.listen()
                
                if text:
                    # Check for exit command
                    if "exit" in text or "quit" in text or "stop" in text:
                        self.voice.speak("Goodbye! Shutting down MSI.")
                        self.running = False
                        break
                    
                    # Process all voice input directly as commands
                    command = text.lower().strip()
                    
                    # Remove optional "msi" prefix if user still says it
                    if command.startswith("msi "):
                        command = command[4:].strip()
                    
                    if command:
                        print(f"\n🔧 COMMAND RECEIVED: {command}")
                        response = self.commands.execute(command)
                        self.voice.speak(response)
                    else:
                        print("⚠️ No command detected, please speak again")
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n🛑 Manual stop detected")
                self.voice.speak("Goodbye!")
                break
            except Exception as e:
                print(f"⚠️ Unexpected error: {e}")
                time.sleep(1)

# ==================== QUICK TEST FUNCTION ====================
def quick_test():
    """Quick test without voice"""
    print("\n🧪 Running quick test...")
    
    executor = CommandExecutor()
    
    test_commands = [
        "open notepad",
        "time",
        "open youtube",
        "find video python tutorial",
        "help",
        "joke",
    ]
    
    for cmd in test_commands:
        print(f"\n🔧 Testing: '{cmd}'")
        result = executor.execute(cmd)
        print(f"✅ Result: {result}")
        time.sleep(0.5)
    
    print("\n✅ All tests completed!")

# ==================== RUN MSI ====================
if __name__ == "__main__":
    print("🚀 Starting MSI AI Voice Assistant...")
    
    # Ask if user wants to run quick test
    choice = input("\nRun quick test first? (y/n): ").lower()
    if choice == 'y':
        quick_test()
    
    # Start main MSI
    try:
        print("\n" + "="*60)
        print("🤖 LAUNCHING MSI...")
        print("="*60)
        msi = MSI()
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Run as Administrator for full system control")
        print("2. Check microphone is connected and working")
        print("3. Install required packages:")
        print("   pip install pyttsx3 speechrecognition pyaudio psutil")
        print("   pip install pycaw comtypes screen-brightness-control")
        print("   pip install pyautogui winshell")
        input("\nPress Enter to exit...")