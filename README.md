# 🤖 MSI - Advanced AI Voice Assistant

**Complete Laptop Control System** - Control your entire laptop from A-Z using just your voice!

## 🌟 Features

MSI is an advanced AI voice assistant that provides complete control over your Windows laptop through voice commands. No need to touch keyboard or mouse - just speak!

### 🎯 Capabilities

- 🔊 **Volume Control** - Adjust, mute, or set specific volume levels
- 💡 **Brightness Control** - Control screen brightness with voice
- 🔋 **Battery & Power** - Check battery status and power information
- 📡 **WiFi Management** - Enable/disable WiFi and check connection status
- 📁 **File Operations** - Create files and folders with voice commands
- 🖥️ **System Monitoring** - Check CPU, RAM, disk usage in real-time
- 📸 **Screenshots** - Capture screen instantly
- 🌐 **Web Browsing** - Open any website or search the web
- ⚙️ **Application Control** - Open, close, and manage applications
- 💾 **Storage Management** - Check disk space, empty recycle bin
- 🎮 **And much more!**

## 📦 Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed on your system.

### Step 2: Install Required Packages
Run this command in your terminal (as Administrator):

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install pyttsx3 speechrecognition pyaudio psutil pycaw comtypes screen-brightness-control pyautogui winshell pillow pywin32
```

### Step 3: Run MSI
```bash
python main.py
```

**Important**: Run as Administrator for full system control capabilities!

## 🎤 How to Use

1. Start the program: `python main.py`
2. Wait for "MSI IS ACTIVE" message
3. Say commands starting with **"MSI"** keyword
4. Example: "MSI volume 50" or "MSI open notepad"

## 📝 Command List

### 🔊 Volume Control
- `MSI volume up` - Increase volume to maximum
- `MSI volume down` - Decrease volume
- `MSI volume mute` - Mute sound
- `MSI volume 50` - Set volume to 50%
- `MSI volume [0-100]` - Set specific volume level

### 💡 Brightness Control
- `MSI brightness up` - Maximum brightness
- `MSI brightness down` - Minimum brightness
- `MSI brightness 50` - Set to 50%
- `MSI brightness [0-100]` - Set specific brightness

### 🔋 Power & Battery
- `MSI battery` - Check battery status
- `MSI battery status` - Detailed battery info
- `MSI system stats` - CPU, RAM, disk usage
- `MSI performance` - System performance metrics

### 📡 WiFi Control
- `MSI wifi status` - Check WiFi connection
- `MSI wifi on` - Enable WiFi
- `MSI wifi off` - Disable WiFi

### 📁 File & Folder Operations
- `MSI create file [name]` - Create new file
- `MSI create folder [name]` - Create new folder
- `MSI open folder desktop` - Open Desktop folder
- `MSI open folder documents` - Open Documents
- `MSI open folder downloads` - Open Downloads
- `MSI empty recycle bin` - Empty recycle bin

### 📸 Screen Capture
- `MSI screenshot` - Take screenshot (saved to Desktop)
- `MSI capture screen` - Same as screenshot

### 🖥️ Applications
- `MSI open notepad` - Open Notepad
- `MSI open calculator` - Open Calculator
- `MSI open paint` - Open Paint
- `MSI open chrome` - Open Google Chrome
- `MSI open firefox` - Open Firefox
- `MSI open cmd` - Open Command Prompt
- `MSI task manager` - Open Task Manager
- `MSI control panel` - Open Control Panel
- `MSI close chrome` - Close Chrome
- `MSI list apps` - List running applications

### 🌐 Web Browsing
- `MSI open youtube` - Open YouTube
- `MSI open google` - Open Google
- `MSI open facebook` - Open Facebook
- `MSI open instagram` - Open Instagram
- `MSI open website [url]` - Open any website
- `MSI search [query]` - Google search
- `MSI find video [query]` - YouTube search
- `MSI play [song name]` - Play video on YouTube

### ⚙️ System Control
- `MSI shutdown` - Shutdown computer (5 sec warning)
- `MSI restart` - Restart computer
- `MSI lock` - Lock computer
- `MSI sleep` - Put computer to sleep

### 💾 Storage & System Info
- `MSI disk space` - Check available storage
- `MSI system info` - Computer information
- `MSI time` - Current time
- `MSI date` - Current date

### 🎭 Fun & Utility
- `MSI tell joke` - Hear a random joke
- `MSI help` - Show all commands
- `MSI what can you do` - List capabilities

### 🛑 Exit
- `exit` or `quit` or `stop` - Close MSI

## 🎯 Example Usage

```
You: "MSI volume 75"
MSI: "Volume set to 75%"

You: "MSI brightness high"
MSI: "Brightness set to 100%"

You: "MSI battery status"
MSI: "Battery: 85%. Plugged in. Time remaining: 2h 30m"

You: "MSI take screenshot"
MSI: "Screenshot saved to Desktop as screenshot_20260202_143052.png"

You: "MSI open chrome"
MSI: "Opening Chrome"

You: "MSI search artificial intelligence"
MSI: "Searching: artificial intelligence"
```

## 🔧 Troubleshooting

### Microphone Not Working
- Check if microphone is connected
- Go to Windows Settings > Privacy > Microphone
- Allow apps to access your microphone
- Test microphone in Sound settings

### Some Commands Not Working
- Run the program as Administrator
- Some system commands require elevated privileges

### Installation Errors
```bash
# If PyAudio fails to install:
pip install pipwin
pipwin install pyaudio

# Alternative PyAudio installation:
python -m pip install pyaudio
```

### Volume/Brightness Control Not Working
```bash
pip install pycaw comtypes
pip install screen-brightness-control
```

## 💡 Tips

1. **Speak Clearly**: Speak clearly and at normal pace
2. **Keyword First**: Always say "MSI" before your command
3. **Administrator**: Run as Administrator for full control
4. **Microphone**: Use a good quality microphone for best results
5. **Quiet Environment**: Use in a quiet environment for better recognition

## 🔐 Permissions

MSI requires certain permissions to control your laptop:
- Microphone access (for voice commands)
- Administrator rights (for system control)
- Internet access (for web browsing and searches)

## 🆘 Support

If you encounter any issues:
1. Make sure all packages are installed
2. Run as Administrator
3. Check microphone settings
4. Verify Python version (3.8+)

## 📜 License

This project is for educational and personal use.

## 🚀 Version

**MSI v2.0** - Complete Laptop Control System
- Advanced voice recognition
- Comprehensive system control
- Enhanced functionality from A to Z

---

**Made with ❤️ for complete hands-free laptop control!**
