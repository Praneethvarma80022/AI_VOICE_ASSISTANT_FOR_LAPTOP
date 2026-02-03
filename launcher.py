"""
MSI AI Voice Assistant - Main Launcher
Starts with login, then launches MSI UI
"""

import os
import sys

def main():
    """Main launcher - Login then MSI UI"""
    print("="*60)
    print("    MSI AI VOICE ASSISTANT")
    print("    Complete Laptop Control System")
    print("="*60)
    print("\n🔐 Starting login system...\n")
    
    # Import login app
    from login import LoginApp, launch_msi_after_login
    import customtkinter as ctk
    
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run login
    def on_success(username):
        """Launch MSI after login"""
        launch_msi_after_login(username)
    
    app = LoginApp(callback=on_success)
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n📦 Make sure all packages are installed:")
        print("   pip install customtkinter pyttsx3 speechrecognition")
        print("   pip install pyaudio psutil pycaw comtypes")
        input("\nPress Enter to exit...")
