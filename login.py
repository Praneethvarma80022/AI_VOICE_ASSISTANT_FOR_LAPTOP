"""
MSI Login System with SQLite Database
Handles user authentication and registration
"""

import sqlite3
import hashlib
import customtkinter as ctk
from pathlib import Path
import os

# Database configuration
DB_PATH = Path.home() / ".msi_data" / "users.db"
DB_PATH.parent.mkdir(exist_ok=True)

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
            
            # Create users table
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
            
            # Check if username exists
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                return False, "Username already exists!"
            
            # Check if email exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                return False, "Email already registered!"
            
            # Hash password and insert
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
            
            # Get user
            cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False, "User not found!"
            
            # Verify password
            password_hash = self.hash_password(password)
            if result[1] == password_hash:
                return True, "Login successful!"
            else:
                return False, "Incorrect password!"
        
        except Exception as e:
            return False, f"Login error: {str(e)}"
    
    def get_user_id(self, username: str) -> int:
        """Get user ID by username"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except:
            return None


class LoginApp(ctk.CTk):
    """Login window for MSI application"""
    
    def __init__(self, callback=None):
        super().__init__()
        
        self.title("MSI - Login")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.db = DatabaseManager()
        self.callback = callback
        self.current_mode = "login"  # login or register
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup login UI"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            self.main_frame,
            text="🤖 MSI AI VOICE ASSISTANT",
            font=("Orbitron", 24, "bold"),
            text_color="#00d4ff"
        )
        header_label.grid(row=0, column=0, pady=30)
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="LOGIN",
            font=("Orbitron", 20, "bold"),
            text_color="#ffcc00"
        )
        self.title_label.grid(row=0, column=0, pady=20)
        
        # Username
        ctk.CTkLabel(
            self.content_frame,
            text="Username",
            font=("Consolas", 12),
            text_color="#00ff00"
        ).grid(row=1, column=0, sticky="w", pady=(10, 5))
        
        self.username_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter username",
            height=40,
            font=("Consolas", 12),
            border_color="#00d4ff",
            border_width=2
        )
        self.username_entry.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        # Password
        ctk.CTkLabel(
            self.content_frame,
            text="Password",
            font=("Consolas", 12),
            text_color="#00ff00"
        ).grid(row=3, column=0, sticky="w", pady=(10, 5))
        
        self.password_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter password",
            height=40,
            font=("Consolas", 12),
            border_color="#00d4ff",
            border_width=2,
            show="•"
        )
        self.password_entry.grid(row=4, column=0, sticky="ew", pady=(0, 15))
        
        # Email (for registration)
        ctk.CTkLabel(
            self.content_frame,
            text="Email",
            font=("Consolas", 12),
            text_color="#00ff00"
        ).grid(row=5, column=0, sticky="w", pady=(10, 5))
        
        self.email_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter email",
            height=40,
            font=("Consolas", 12),
            border_color="#00d4ff",
            border_width=2
        )
        self.email_entry.grid(row=6, column=0, sticky="ew", pady=(0, 15))
        self.email_entry.grid_remove()  # Hidden by default
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=("Consolas", 10),
            text_color="#ff6b6b"
        )
        self.status_label.grid(row=7, column=0, pady=10)
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.content_frame,
            text="LOGIN",
            height=40,
            font=("Orbitron", 14, "bold"),
            fg_color="#1f538d",
            hover_color="#2b6db8",
            command=self.handle_login
        )
        self.login_button.grid(row=8, column=0, sticky="ew", pady=10)
        
        # Register button
        self.register_button = ctk.CTkButton(
            self.content_frame,
            text="REGISTER",
            height=40,
            font=("Orbitron", 14, "bold"),
            fg_color="#1d5f1d",
            hover_color="#2a7f2a",
            command=self.show_register_mode
        )
        self.register_button.grid(row=9, column=0, sticky="ew", pady=5)
        
        # Toggle button (for switching modes)
        self.toggle_button = ctk.CTkButton(
            self.content_frame,
            text="Already have account? Login",
            height=35,
            font=("Consolas", 11),
            fg_color="#333333",
            hover_color="#444444",
            command=self.toggle_mode
        )
        self.toggle_button.grid(row=10, column=0, sticky="ew", pady=10)
        self.toggle_button.grid_remove()  # Hidden by default
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.status_label.configure(text="❌ Please enter username and password!", text_color="#ff6b6b")
            return
        
        success, message = self.db.authenticate_user(username, password)
        
        if success:
            self.status_label.configure(text="✅ " + message, text_color="#00ff00")
            self.after(1000, lambda: self.close_and_continue(username))
        else:
            self.status_label.configure(text="❌ " + message, text_color="#ff6b6b")
    
    def show_register_mode(self):
        """Switch to registration mode"""
        self.current_mode = "register"
        self.title_label.configure(text="CREATE ACCOUNT")
        self.login_button.configure(text="REGISTER")
        self.register_button.grid_remove()
        self.toggle_button.grid()
        self.email_entry.grid()
        self.status_label.configure(text="")
        self.login_button.configure(command=self.handle_register)
    
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
            self.status_label.configure(text="✅ " + message, text_color="#00ff00")
            self.after(1000, self.toggle_mode)
        else:
            self.status_label.configure(text="❌ " + message, text_color="#ff6b6b")
    
    def toggle_mode(self):
        """Toggle between login and register modes"""
        if self.current_mode == "register":
            self.current_mode = "login"
            self.title_label.configure(text="LOGIN")
            self.login_button.configure(text="LOGIN", command=self.handle_login)
            self.register_button.grid()
            self.toggle_button.grid_remove()
            self.email_entry.grid_remove()
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.status_label.configure(text="")
        else:
            self.show_register_mode()
    
    def close_and_continue(self, username):
        """Close login and continue to main app"""
        self.username = username
        if self.callback:
            self.callback(username)
        self.destroy()


def launch_msi_after_login(username):
    """Launch MSI UI after successful login"""
    try:
        print(f"✅ User '{username}' logged in successfully!")
        print("🚀 Launching MSI AI Voice Assistant...")
        
        # Import and launch MSI UI
        import subprocess
        import sys
        
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        msi_ui_path = os.path.join(current_dir, "msi_ui.py")
        
        # Launch msi_ui.py
        subprocess.Popen([sys.executable, msi_ui_path])
        
    except Exception as e:
        print(f"❌ Error launching MSI UI: {e}")
        print("Trying alternative method...")
        try:
            # Alternative: Direct import
            import msi_ui
        except Exception as e2:
            print(f"❌ Could not launch MSI UI: {e2}")


if __name__ == "__main__":
    def on_login_success(username):
        """Callback when login is successful"""
        launch_msi_after_login(username)
    
    app = LoginApp(callback=on_login_success)
    app.mainloop()
