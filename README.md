
# 🎙️ AI Voice Assistant for Laptop (MSI UI)

An AI-powered **voice assistant for laptops** built using Python that allows users to control system functions through **voice commands**.
This project features an **MSI-style graphical interface** and **enhanced microphone recognition** for accurate and reliable speech input.

---

## 🚀 Features

* 🎤 Voice-controlled system commands
* 🖥️ MSI-style graphical user interface
* 🔊 Volume control via voice
* 📂 Open applications using speech
* 🔋 Battery status detection
* 📸 Screenshot capture
* 🧠 Improved speech recognition with noise handling

=======
# 🤖 MSI - Advanced AI Voice Assistant for Laptop

## Complete Documentation & User Guide

**Version:** 2.5  
**Last Updated:** February 3, 2026  
**Status:** ✅ Fully Operational

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Features Overview](#features-overview)
3. [Installation](#installation)
4. [How to Use](#how-to-use)
5. [Complete Command List](#complete-command-list)
6. [Chat History System](#chat-history-system)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Technical Details](#technical-details)

---

## 🚀 Quick Start

### Running the Application

**UI Version (Recommended):**
```bash
python msi_usi.py
```
Or double-click: `run MSI.bat`

**Console Version:**
```bash
python main.py
```
Or double-click: `run_msi.bat`

### First Time Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python msi_integrated.py
   ```

3. Wait for mic test (stay quiet for 2 seconds)

4. Click **"🎤 ACTIVATE VOICE"** and start speaking!

---

## ✨ Features Overview

### Core Features

✅ **Voice Control** - Hands-free laptop operation  
✅ **Text Input** - Type commands directly  
✅ **Chat History** - All conversations saved automatically  
✅ **Smart App Opening** - Web vs installed app detection  
✅ **Music Control** - Spotify integration  
✅ **System Management** - Volume, brightness, battery, etc.  
✅ **File Operations** - Create, open, search files  
✅ **Web Integration** - Open websites, apps, social media  

### New Features (v2.5)

🆕 **Chat History Sidebar** - Like ChatGPT interface  
🆕 **Spotify Playback** - Play songs by name  
🆕 **Smart Messaging** - WhatsApp & Telegram (web/installed)  
🆕 **Fixed Screenshots** - Reliable capture with verification  
🆕 **Session Management** - View and load previous chats  

>>>>>>> d607771 (Add Updated files and all)
---

## 🛠️ Installation & Setup

Follow these steps carefully to run the project successfully.

---

### 🔹 1️⃣ Prerequisites

Make sure the following are installed on your system:

* **Windows OS**
* **Python 3.8 or above**
* **Working Microphone**
* **Internet connection** (for speech recognition)

Check Python installation:

```bash
python --version
```

---

### 🔹 2️⃣ Clone the Repository

```bash
git clone https://github.com/Praneethvarma80022/AI_VOICE_ASSISTANT_FOR_LAPTOP.git
cd AI_VOICE_ASSISTANT_FOR_LAPTOP
```

---

### 🔹 3️⃣ Install Required Libraries
=======
### Prerequisites

- **Python 3.7+**
- **Windows OS**
- **Microphone** (for voice commands)
- **Internet Connection** (for speech recognition)
>>>>>>> d607771 (Add Updated files and all)

### Install Dependencies

**Option 1: Using requirements.txt**
```bash
pip install -r requirements.txt
```


⚠️ If `pip` is not recognized:

```bash
python -m pip install -r requirements.txt
```

---

### 🔹 4️⃣ Install Microphone Dependencies (IMPORTANT)

Speech recognition requires **PyAudio**.

#### ✔ Option A: Using prebuilt wheel (Recommended)

Download the correct `.whl` file from:

> [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

Then install:

```bash
pip install PyAudio-*.whl
```

#### ✔ Option B: Using install.bat

```bash
install.bat
=======
**Option 2: Manual Installation**
```bash
pip install customtkinter
pip install pyttsx3
pip install speechrecognition
pip install pyaudio
pip install psutil
pip install requests
pip install pycaw
pip install comtypes
pip install screen-brightness-control
pip install pyautogui
```

### Optional Dependencies

For Spotify (if installed):
```bash
# Already works with installed Spotify Desktop
```

For WhatsApp/Telegram (desktop apps):
```bash
# Install from official websites if not already installed
```

---

## 💡 How to Use

### Voice Commands

1. Click **"🎤 ACTIVATE VOICE"** button
2. Wait for "🎤 Listening..." message
3. Speak your command clearly
4. Wait for response
5. Command executes automatically

### Text Commands

1. Type command in the input box
2. Press **Enter**
3. Command executes immediately

### Chat History Sidebar

1. View previous chats on the right sidebar
2. Click any **"📝 Chat N"** to load that conversation
3. Click **"📜 TOGGLE HISTORY"** to hide/show sidebar

---

## 📖 Complete Command List

### 🔊 Volume Control

| Command | Action |
|---------|--------|
| `volume up` | Set to 100% |
| `volume down` | Set to 20% |
| `volume mute` | Set to 0% |
| `volume 50` | Set to 50% |
| `volume [0-100]` | Set to specific level |

### 💡 Brightness Control

| Command | Action |
|---------|--------|
| `brightness up` | Set to 100% |
| `brightness down` | Set to 30% |
| `brightness 50` | Set to 50% |
| `brightness [0-100]` | Set to specific level |

### 🔋 System Information

| Command | Action |
|---------|--------|
| `battery` | Show battery status & time remaining |
| `system stats` | Display CPU, RAM, Disk usage |
| `cpu` | Show CPU usage |
| `ram usage` | Show RAM usage |
| `disk space` | Show disk space info |

### 📸 Screenshot

| Command | Action |
|---------|--------|
| `screenshot` | Capture screen to Desktop |
| `screen shot` | Capture screen |
| `capture screen` | Capture screen |

**Output:** `screenshot_YYYYMMDD_HHMMSS.png` saved to Desktop

### 🎵 Spotify Integration

| Command | Action |
|---------|--------|
| `open spotify` | Launch Spotify |
| `open spotify and play [song name]` | Open & play song |
| `spotify play [song name]` | Play specific song |
| `play [song name] on spotify` | Play song |

**Examples:**
- `"open spotify and play Shape of You"`
- `"spotify play Bohemian Rhapsody by Queen"`
- `"play Levitating"`

### 💬 WhatsApp

| Command | Action |
|---------|--------|
| `open whatsapp` | Open web version |
| `open installed whatsapp` | Open desktop app |
| `whatsapp chat [name]` | Open web + search contact |
| `installed whatsapp message [name]` | Open app + search |

**Examples:**
- `"open whatsapp"` → Web version
- `"open installed whatsapp"` → Desktop app
- `"whatsapp chat mom"` → Web + search

### 💬 Telegram

| Command | Action |
|---------|--------|
| `open telegram` | Open web version |
| `open installed telegram` | Open desktop app |
| `telegram chat [username]` | Open web + search user |
| `installed telegram message [name]` | Open app + jump to chat |

**Examples:**
- `"open telegram"` → Web version
- `"open installed telegram"` → Desktop app
- `"telegram chat johnsmith"` → Web + search

### 🌐 Web Browsing

| Command | Action |
|---------|--------|
| `open youtube` | Open YouTube |
| `open google` | Open Google |
| `open facebook` | Open Facebook |
| `open twitter` | Open Twitter |
| `open instagram` | Open Instagram |
| `open github` | Open GitHub |
| `open stackoverflow` | Open Stack Overflow |
| `open linkedin` | Open LinkedIn |
| `open website [url]` | Open any website |
| `search [query]` | Google search |

### 📂 File & Folder Operations

| Command | Action |
|---------|--------|
| `open file [name]` | Search and open file |
| `open folder desktop` | Open Desktop folder |
| `open folder documents` | Open Documents |
| `open folder downloads` | Open Downloads |
| `create file [name]` | Create new file |
| `create folder [name]` | Create new folder |
| `empty recycle bin` | Clear recycle bin |

### 🖥️ Applications

| Command | Action |
|---------|--------|
| `open notepad` | Launch Notepad |
| `open calculator` | Launch Calculator |
| `open paint` | Launch Paint |
| `open chrome` | Launch Chrome |
| `task manager` | Open Task Manager |
| `close chrome` | Close Chrome |
| `close notepad` | Close Notepad |
| `list apps` | Show running apps |

### 🔌 System Control

| Command | Action |
|---------|--------|
| `shutdown` | Shutdown in 5 seconds |
| `restart` | Restart in 5 seconds |
| `lock` | Lock computer |
| `wifi status` | Check WiFi connection |
| `wifi on` | Enable WiFi |
| `wifi off` | Disable WiFi |

### ⏰ Time & Date

| Command | Action |
|---------|--------|
| `time` | Show current time |
| `date` | Show current date |
| `today's date` | Show full date |

### 🎭 Entertainment

| Command | Action |
|---------|--------|
| `joke` | Tell a random joke |
| `tell joke` | Tell a joke |

### 👋 Greetings

| Command | Action |
|---------|--------|
| `hello` / `hi` / `hey` | Greeting response |
| `how are you` | Status check |
| `your name` | Introduction |

---

## 💾 Chat History System

### How It Works

**Automatic Saving:**
- Every message is saved automatically
- No manual action required
- Stored in `.msi_history` folder

**Storage Location:**
```
C:\Users\[YourName]\.msi_history\
├── session_20260202_143052.json
├── session_20260202_093015.json
└── session_20260201_180045.json
```

**JSON Format:**
```json
[
  {
    "timestamp": "14:30:52",
    "sender": "USER",
    "message": "YOU: open spotify"
  },
  {
    "timestamp": "14:30:53",
    "sender": "MSI",
    "message": "MSI: Opening Spotify Desktop"
  }
]
```

### Using the Sidebar

**View Chats:**
- Right sidebar shows all previous sessions
- Listed as "Chat 1", "Chat 2", etc. (newest first)
- Each shows preview of first message

**Load Chat:**
- Click any "📝 Chat N" button
- Conversation loads into main console
- Continue from where you left off

**Toggle Visibility:**
- Click "📜 TOGGLE HISTORY" button
- Hide sidebar for more screen space
- Show again anytime

**UI Layout:**
```
┌─────────────┬──────────────────┬──────────────┐
│   SYSTEM    │   MAIN CONSOLE   │    CHAT      │
│   WIDGETS   │                  │   HISTORY    │
│             │                  │              │
│  CPU: 45%   │  [Console Area]  │  📝 Chat 1   │
│  RAM: 60%   │                  │   "open..."  │
│  Battery    │                  │              │
│  Weather    │                  │  📝 Chat 2   │
│             │                  │   "screen..."│
│  [Quick     │                  │              │
│  Actions]   │                  │  📝 Chat 3   │
│             │                  │   "whats..." │
└─────────────┴──────────────────┴──────────────┘
    280px           840px            300px
```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────┐
│        LOGIN SCREEN (msi_ui.py)         │
│  Database: Verify username + password   │
│  Hash: SHA-256 for security              │
└──────────────┬──────────────────────────┘
               │ ✓ Authentication Success
               ▼
┌─────────────────────────────────────────┐
│     MSI INTEGRATED DASHBOARD (1420x750) │
│                                         │
│  ┌──────────┬──────────┬──────────────┐ │
│  │LEFT      │ CENTER   │ RIGHT        │ │
│  │SIDEBAR   │ CONSOLE  │ SIDEBAR      │ │
│  │280px     │ Flexible │ 300px        │ │
│  │          │          │              │ │
│  │Stats ────┼─ Input ─┼─ Chat        │ │
│  │Weather   │ Output   │ History      │ │
│  │Battery   │ Status   │ Refresh      │ │
│  │CPU/RAM   │ Buttons  │              │ │
│  │Disk      │ Voice/   │ Auto-save    │ │
│  │Actions   │ Text     │              │ │
│  └──────────┴──────────┴──────────────┘ │
│                                         │
│  Background Threads:                    │
│  ✓ Stats update (5s loop)               │
│  ✓ Weather fetch (startup + manual)     │
│  ✓ Voice recognition (when active)      │
│  ✓ Chat auto-save                       │
│  ✓ Command execution                    │
└─────────────────────────────────────────┘
               │
               ▼
        ┌──────────────────┐
        │  COMMAND EXECUTE │
        │                  │
        │ • Process text   │
        │ • Process voice  │
        │ • 90+ commands   │
        │ • System control │
        │ • Apps control   │
        │ • Web browsing   │
        │ • Messaging      │
        └──────────────────┘
               │
               ▼
        ┌──────────────────┐
        │  SAVE TO DATABASE│
        │                  │
        │ • User: john     │
        │ • Command: open  │
        │ • Response: OK   │
        │ • Timestamp      │
        │ • Chat history   │
        └──────────────────┘
               │
               ▼
        ┌──────────────────┐
        │  AUTO REFRESH    │
        │  RIGHT SIDEBAR   │
        │                  │
        │ New chat entry   │
        │ appears in list  │
        └──────────────────┘
```

---
## 🎯 Advanced Features

### Smart App Detection

**WhatsApp & Telegram:**
- Default: Opens web version
- With "installed" keyword: Opens desktop app
- Auto-fallback if app not found

**Spotify:**
- Checks for desktop app first
- Falls back to web version
- Deep linking for direct song playback

### Path Detection

**Spotify Paths:**
```
%APPDATA%\Spotify\Spotify.exe
C:\Program Files\Spotify\Spotify.exe
C:\Program Files (x86)\Spotify\Spotify.exe
```

**WhatsApp Paths:**
```
%APPDATA%\WhatsApp\WhatsApp.exe
C:\Program Files\WhatsApp\WhatsApp.exe
C:\Program Files (x86)\WhatsApp\WhatsApp.exe
```

**Telegram Paths:**
```
%APPDATA%\Telegram Desktop\Telegram.exe
C:\Program Files\Telegram Desktop\Telegram.exe
C:\Program Files (x86)\Telegram Desktop\Telegram.exe
```

### Protocol Support

**Spotify URI:**
```
spotify:search:[song_name]
```

**Telegram Deep Link:**
```
tg://resolve?domain=[username]
```

---

## 🔧 Troubleshooting

### Microphone Not Working

**Issue:** "Could not understand audio"

**Solutions:**
1. Check microphone is connected
2. Speak clearly and close to mic
3. Reduce background noise
4. Adjust for ambient noise during startup
5. Check microphone permissions in Windows

**Check Energy Threshold:**
```
MSI: Energy threshold: [value]
```
- Too high? Application won't detect voice
- Too low? Picks up background noise
- Optimal: 300-500

### Screenshot Not Saving

**Issue:** "Screenshot capture failed"

**Solutions:**
1. Install PyAutoGUI:
   ```bash
   pip install pyautogui
   ```
2. Check Desktop folder exists
3. Run as administrator if needed
4. Check disk space

### App Not Opening

**Issue:** "Could not open [app]"

**Solutions:**
1. **For Desktop Apps:**
   - Verify app is installed
   - Check installation path matches
   - Try "installed [app]" command

2. **For Web Apps:**
   - Check internet connection
   - Ensure browser is installed
   - Clear browser cache

3. **For Spotify:**
   - Open Spotify manually once to register URI protocol
   - Login to Spotify account
   - Check if Premium (better for auto-play)

### Speech Recognition Issues

**Issue:** Commands not recognized

**Solutions:**
1. Check internet connection (Google API required)
2. Speak clearly with pauses
3. Use exact command phrases
4. Check microphone volume in Windows
5. Try text input instead

### Chat History Not Saving

**Issue:** No previous sessions showing

**Solutions:**
1. Check `.msi_history` folder exists:
   ```
   C:\Users\[YourName]\.msi_history\
   ```
2. Ensure write permissions
3. Look for JSON files in folder
4. Restart application

---

## 🛠️ Technical Details

### System Requirements

- **OS:** Windows 10/11
- **Python:** 3.7 or higher
- **RAM:** 4GB minimum, 8GB recommended
- **Disk Space:** 500MB for dependencies
- **Internet:** Required for speech recognition

### Dependencies

**Core Libraries:**
- `customtkinter` - Modern UI framework
- `pyttsx3` - Text-to-speech engine
- `speechrecognition` - Voice input processing
- `pyaudio` - Audio handling

**System Control:**
- `psutil` - System stats (CPU, RAM, disk)
- `pycaw` - Volume control
- `comtypes` - Windows COM interfaces
- `screen-brightness-control` - Display brightness

**Additional:**
- `pyautogui` - Screenshot capture
- `requests` - API calls (weather)
- Standard library: `os`, `sys`, `datetime`, `subprocess`, `webbrowser`

### Architecture

**Main Components:**
1. **VoiceSystem** - Speech recognition & TTS
2. **AdvancedCommandExecutor** - System operations
3. **CommandExecutor** - Command routing
4. **ChatHistoryManager** - Session storage
5. **MSIApp** - UI management

**File Structure:**
```
Ai_Voice/
├── msi_integrated.py          ← Main app (login + 3-column UI)
├── msi_ui.py                  ← Alternative UI (no login)
├── main.py                    ← Console version
├── login.py                   ← Authentication module
├── .msi_history/              # Chat storage
│   ├── session_*.json
├── requirements.txt           ← Dependencies
├── README.md                  ← Basic info
├── DOCUMENTATION.md           ← Comprehensive guide

```
### Performance

**Startup Time:** 3-5 seconds  
**Response Time:** <1 second for commands  
**Speech Recognition:** 1-2 seconds  
**Memory Usage:** 100-200MB  
**CPU Usage:** 5-10% idle, 20-30% active  

---

## 📝 Version History

### v2.5 (February 2, 2026)
- ✅ Added chat history sidebar (ChatGPT-like)
- ✅ Spotify music playback integration
- ✅ Smart WhatsApp & Telegram opening
- ✅ Fixed screenshot capture
- ✅ Session management system
- ✅ Improved UI layout (1400x750)

### v2.0 (February 2, 2026)
- ✅ Chat history storage system
- ✅ JSON-based conversation logs
- ✅ Previous session loading
- ✅ Enhanced error handling

### v1.0 (Initial Release)
- ✅ Voice control system
- ✅ Basic commands
- ✅ System management
- ✅ Web integration

---

## 🎓 Usage Tips

### Best Practices

1. **Clear Speech:** Speak clearly at normal pace
2. **Exact Commands:** Use command list for accuracy
3. **Wait for Response:** Let MSI finish before next command
4. **Check Sidebar:** Review previous chats for reference
5. **Save Important Sessions:** Backup `.msi_history` folder

### Power User Tips

1. **Quick Toggle:** Use "📜 TOGGLE HISTORY" for more space
2. **Load Old Chats:** Review what worked in past sessions
3. **Combine Commands:** Chain operations logically
4. **Voice Shortcuts:** Create custom batch files
5. **Backup History:** Export JSON files regularly

### Common Workflows

**Music Session:**
```
"open spotify and play chill music"
"volume 50"
"brightness down"
```

**Work Setup:**
```
"open chrome"
"open notepad"
"brightness up"
"volume mute"
```

**Social Media Check:**
```
"open whatsapp"
"open instagram"
"open twitter"
>>>>>>> d607771 (Add Updated files and all)
```

---

### 🔹 5️⃣ Verify Microphone Access

1. Open **Windows Settings**
2. Go to **Privacy & Security → Microphone**
3. Enable:

   * ✅ Allow apps to access microphone
   * ✅ Allow desktop apps to access microphone

---

## ▶️ Running the Application

### 🔹 Run MSI UI Version

```bash
python msi_ui.py
```

OR

```bash
run_msi_ui.bat
```

---

## 🎤 Microphone Improvements (Latest Update)

The microphone issue was fixed by optimizing the speech recognition configuration.

### ✅ Fixes Applied

* Energy threshold reduced to **300**
* Dynamic energy threshold enabled
* Ambient noise calibration (2 seconds)
* Listening timeout increased to **5 seconds**
* Phrase time limit increased to **10 seconds**
* Clear console feedback and error messages

---

## 🎯 How to Use Voice Commands

1. Start the application
2. Wait 2 seconds for noise calibration
3. Click **🎤 ACTIVATE VOICE**
4. Speak after seeing **Listening…**

### 🗣️ Sample Commands

* `"volume 50"`
* `"open notepad"`
* `"screenshot"`
* `"battery status"`

---

## 💡 Microphone Usage Tips

### ✅ DO

* Speak clearly and normally
* Wait for listening message
* Keep background noise low

### ❌ DON’T

* Speak too fast
* Talk while processing
* Use in noisy environments

---

## 🔍 Console Feedback

* `🎤 Listening...` → Ready for input
* `✅ YOU: <command>` → Voice recognized
* `MSI: <response>` → Action executed

---

## 🛠️ Troubleshooting

### ❌ Microphone Not Working?

* Check **Windows Microphone Permissions**
* Test mic using **Voice Recorder**
* Ensure energy threshold shows **300–500**
* Restart the application

---

## 📂 Project Structure

```
AI_VOICE_ASSISTANT_FOR_LAPTOP/
├── main.py
├── msi_ui.py
├── requirements.txt
├── install.bat
├── run_msi.bat
├── run_msi_ui.bat
├── COMMAND_LIST.md
├── FILE_STRUCTURE.txt
├── QUICK_START.txt
├── UPDATE_SUMMARY.md
└── README.md
```

---

## 🧪 Technologies Used

* Python
* SpeechRecognition
* PyAudio
* Tkinter
* Windows APIs

---

## 📌 Use Cases

* Hands-free laptop control
* Accessibility support
* Smart system automation
* Academic capstone project

=======
## 🆘 Support & Help

### Getting Help

1. **Read This Documentation** - Comprehensive guide
2. **Check Troubleshooting Section** - Common issues
3. **Review Command List** - Exact syntax
4. **Check Chat History** - What worked before

### Common Questions

**Q: Can I use this offline?**  
A: Partially. Voice recognition requires internet (Google API), but text commands work offline.

**Q: Does this work on Mac/Linux?**  
A: Currently Windows only. System commands are OS-specific.

**Q: Can I add custom commands?**  
A: Yes! Edit `CommandExecutor.execute()` method in the code.

**Q: Is my chat history private?**  
A: Yes. All data stored locally in `.msi_history` folder.

**Q: How do I backup my chats?**  
A: Copy the `.msi_history` folder to external storage.

---

## 🔐 Privacy & Security

- **No Data Collection:** Nothing sent to external servers (except Google Speech API)
- **Local Storage:** All chat history stored on your machine
- **No Tracking:** No analytics or telemetry
- **Open Source:** Code is fully visible and auditable

---

## 📜 License

This project is provided as-is for educational and personal use.

---

## 👨‍💻 Developer

**Repository:** [AI_VOICE_ASSISTANT_FOR_LAPTOP](https://github.com/Praneethvarma80022/AI_VOICE_ASSISTANT_FOR_LAPTOP)  
**Owner:** Praneethvarma80022  
**Branch:** main

---

## 🎉 Credits

**Speech Recognition:** Google Speech API  
**UI Framework:** CustomTkinter  
**TTS Engine:** pyttsx3  
**System Integration:** Various Python libraries

---

**Thank you for using MSI Voice Assistant!** 🚀

For updates and improvements, check the repository regularly.

**Current Status:** ✅ Fully Operational | All Features Working
>>>>>>> d607771 (Add Updated files and all)

