# 🎨 MSI AI Voice Assistant - UI Version

**Beautiful Dark-Themed Interface with Complete Laptop Control**

## 🌟 New Features

### 📱 Messaging Apps Control
- **Telegram**: Open and chat with specific people
  - "open telegram"
  - "telegram chat john"
  - "message person sarah on telegram"
  
- **WhatsApp**: Quick WhatsApp Web access
  - "open whatsapp"
  - "whatsapp chat mom"

### 📂 Advanced File Operations
- **Open Files by Name**
  - "open file report.pdf"
  - "open file presentation"
  - Searches Desktop, Documents, Downloads automatically

### 🎨 Beautiful UI Features
- **Dark Theme** with cyberpunk aesthetics
- **Real-time System Monitoring**
  - Live CPU usage
  - RAM usage
  - Disk usage
  - Battery status
- **Weather Widget** (requires API key)
- **Quick Action Buttons**
  - One-click screenshot
  - Quick volume/brightness control
- **Console Log** with timestamps
- **Voice/Text Input** - Use microphone or type

## 🚀 Quick Start

### Installation
```bash
# Install all required packages
pip install customtkinter pyttsx3 speechrecognition pyaudio psutil
pip install pycaw comtypes screen-brightness-control pyautogui requests
```

### Run the UI Version
```bash
python msi_ui.py
```
Or double-click: `run_msi_ui.bat`

## 🎤 How to Use

### Two Ways to Command:
1. **🎤 Voice Mode**: Click "ACTIVATE VOICE" button and speak
2. **⌨️ Text Mode**: Type command in input box and press Enter

### No Wake Word Required!
Just say or type your command directly:
- ✅ "volume 50"
- ✅ "open notepad"
- ✅ "screenshot"

(Optional: You can still say "MSI" before commands if you prefer)

## 📝 New Commands

### 📱 Messaging
```
• open telegram
• telegram chat [username]
• message person [name] on telegram
• open whatsapp
• whatsapp chat [name]
```

### 📂 File Operations
```
• open file [filename]
• open file report.pdf
• open file presentation
```

### All Previous Commands Still Work!
```
• volume 50
• brightness high
• battery status
• screenshot
• open notepad
• system stats
• open youtube
• search [query]
• time / date
• shutdown / restart / lock
```

## 🎨 UI Components

### Left Sidebar (Widgets):
- **System Stats**: Real-time CPU, RAM, Disk monitoring
- **Battery Status**: Current battery percentage
- **Weather**: Live weather data (requires API key)
- **Quick Actions**: One-click buttons for common tasks

### Main Console:
- Command history with timestamps
- MSI responses
- System diagnostics
- Color-coded messages

### Control Panel:
- Text input field
- Voice activation button
- Clear log button

## ⚙️ Configuration

### Weather API (Optional):
1. Get free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Edit `msi_ui.py`:
```python
WEATHER_API_KEY = "your_api_key_here"
CITY = "Your City"
```

## 🎯 Examples

### Using Voice:
1. Click "🎤 ACTIVATE VOICE"
2. Speak: "volume 75"
3. MSI responds and executes

### Using Text:
1. Type in input box: "open telegram"
2. Press Enter
3. Telegram opens

### Quick Actions:
- Click "📸 Screenshot" button
- Instant screenshot saved to Desktop

### File Opening:
- Say: "open file project"
- MSI searches and opens matching file

### Messaging:
- Say: "telegram chat johnsmith"
- Opens Telegram and navigates to chat

## 🎨 UI Customization

The UI uses CustomTkinter with dark theme:
- **Primary Color**: Electric Blue (#00d4ff)
- **Background**: Deep Black (#0a0a0a)
- **Console**: Matrix Green (#00ff00)
- **Alerts**: Amber (#ffcc00)

To change theme, edit in `msi_ui.py`:
```python
ctk.set_appearance_mode("dark")  # or "light"
ctk.set_default_color_theme("blue")  # or "green", "dark-blue"
```

## 🔧 Troubleshooting

### UI Not Opening
```bash
pip install customtkinter
```

### Microphone Not Working
- Check Windows Privacy Settings
- Allow microphone access for Python
- Test with built-in Voice Recorder app

### Commands Not Executing
- Run as Administrator for system commands
- Check console log for error messages

### Weather Not Showing
- Add valid OpenWeatherMap API key
- Check internet connection

## 💡 Tips

1. **Voice Mode**: Click "STOP LISTENING" when done to save CPU
2. **Clear Log**: Click "CLEAR LOG" button to clean console
3. **Quick Actions**: Use sidebar buttons for instant commands
4. **File Opening**: Be specific with file names for better results
5. **System Monitor**: Watch real-time stats in left sidebar

## 🆚 Versions

### Console Version (`main.py`):
- Lightweight
- No UI dependencies
- Perfect for low-resource systems

### UI Version (`msi_ui.py`):
- Beautiful interface
- Real-time monitoring
- Quick action buttons
- Better user experience

## 📦 Dependencies

- **customtkinter**: Modern UI framework
- **pyttsx3**: Text-to-speech
- **speech_recognition**: Voice recognition
- **psutil**: System monitoring
- **pycaw**: Volume control
- **pyautogui**: Screenshots
- **requests**: Weather API (optional)

## 🎮 Keyboard Shortcuts

- **Enter**: Submit text command
- **ESC**: (Future) Quick voice activation
- **Ctrl+C**: Exit program

## 🔮 Future Features

- [ ] Custom wake word configuration
- [ ] Command history dropdown
- [ ] Saved command favorites
- [ ] Multi-language support
- [ ] Theme customization in UI
- [ ] News widget
- [ ] Calendar integration
- [ ] Email notifications

## 📊 System Requirements

- **OS**: Windows 10/11
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Microphone**: Required for voice commands
- **Internet**: Optional (for weather, web commands)

## 🎓 Learning Resources

- CustomTkinter Docs: https://customtkinter.tomschimansky.com/
- Speech Recognition: https://pypi.org/project/SpeechRecognition/
- OpenWeather API: https://openweathermap.org/api

---

**Enjoy your beautiful MSI AI Voice Assistant! 🚀**

*Control your laptop with style!*
