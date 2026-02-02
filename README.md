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


