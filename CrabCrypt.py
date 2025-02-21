import tkinter as tk
from tkinter import filedialog, messagebox
import os
import webbrowser
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives import hashes, padding
import base64
import secrets

version = "1.0.2"

# Cyberpunk Color Theme
BG_COLOR = "#0D0D0D"  # Dark Background
FG_COLOR = "#00FF41"  # Neon Green Text
BTN_COLOR = "#1F1B24"  # Dark Purple Buttons
BTN_HOVER = "#4E3F5A"  # Hover Color
blue = "#5865F2"
red = "#9c0b2a"
green = "#1a3619"

FONT = ("Courier", 12, "bold")

class CrabCryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CrabCrypt🦀🔐")
        self.root.geometry("600x650")
        self.root.configure(bg=BG_COLOR)

        self.file_path = ""

        # Title Banner
        title_label = tk.Label(root, text="CrabCrypt🦀🔐", fg=FG_COLOR, bg=BG_COLOR,
                               font=("Courier", 16, "bold"))
        title_label.pack(pady=10)

        self.password_label = tk.Label(root, text="Enter Password:", fg=blue, bg=BG_COLOR, font=FONT)
        self.password_label.pack()

        self.password_entry = tk.Entry(root, show="*", font=FONT, bg=BTN_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
        self.password_entry.pack(pady=5)

        # File Selection Area
        self.drop_frame = tk.Frame(root, width=400, height=100, bg=BTN_COLOR, relief="solid", borderwidth=2)
        self.drop_frame.pack(pady=10)
        self.drop_frame.pack_propagate(False)

        self.drop_label = tk.Label(self.drop_frame, text="Click to Select File", fg="#FFFFFF", bg=BTN_COLOR, font=FONT,
                                   width=50, height=5)
        self.drop_label.pack(expand=True)
        self.drop_label.bind("<Button-1>", self.select_file)

        self.status_label = tk.Label(root, text="", fg="#FFD700", bg=BG_COLOR, font=FONT)
        self.status_label.pack(pady=5)

        button_width = 20
        button_height = 2
        button_padding = 5

        self.encrypt_button = tk.Button(root, text="Encrypt File", bg=BG_COLOR, fg=red, font=FONT,
                                        width=button_width, height=button_height, command=self.encrypt_file)
        self.encrypt_button.pack(pady=button_padding)
        self.encrypt_button.bind("<Enter>", lambda e: self.encrypt_button.config(bg=BTN_HOVER))
        self.encrypt_button.bind("<Leave>", lambda e: self.encrypt_button.config(bg=BTN_COLOR))

        self.decrypt_button = tk.Button(root, text="Decrypt File", bg=BG_COLOR, fg=FG_COLOR, font=FONT,
                                        width=button_width, height=button_height, command=self.decrypt_file)
        self.decrypt_button.pack(pady=button_padding)
        self.decrypt_button.bind("<Enter>", lambda e: self.decrypt_button.config(bg=BTN_HOVER))
        self.decrypt_button.bind("<Leave>", lambda e: self.decrypt_button.config(bg=BTN_COLOR))

        self.github_button = tk.Button(root, text="GitHub", bg=BG_COLOR, fg="#FFFFFF", font=FONT,
                                       width=button_width, height=button_height, command=self.open_github)
        self.github_button.pack(pady=button_padding)

        self.discord_button = tk.Button(root, text="Discord", bg=BG_COLOR, fg="#FFFFFF", font=FONT,
                                        width=button_width, height=button_height, command=self.open_discord)
        self.discord_button.pack(pady=button_padding)

        self.exit_button = tk.Button(root, text="Exit", bg=BTN_COLOR, fg="#FFFFFF", font=FONT,
                                     width=button_width, height=button_height, command=root.quit)
        self.exit_button.pack(pady=button_padding)

        self.footer_label = tk.Label(root, text=f"V{version}"
            "\nMade by Spyboy\n", fg=blue, bg=BG_COLOR,
                                     font=("Courier", 10, "bold"))
        self.footer_label.pack(side="bottom", pady=5)

    def select_file(self, event):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.drop_label.config(text=f"Selected File: {os.path.basename(self.file_path)}")

    def open_github(self):
        webbrowser.open("https://github.com/spyboy-productions/CrabCrypt")

    def open_discord(self):
        webbrowser.open("https://discord.gg/ZChEmMwE8d")

    def encrypt_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        salt = secrets.token_bytes(16)
        iv = secrets.token_bytes(12)  # 12 bytes for AES-GCM
        key = PBKDF2HMAC(algorithm=hashes.SHA256(), iterations=600000, salt=salt, length=32).derive(password.encode())

        with open(self.file_path, "rb") as f:
            plaintext = f.read()

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        encrypted_path = self.file_path + ".crabcrypt"
        with open(encrypted_path, "wb") as f:
            f.write(salt + iv + encryptor.tag + ciphertext)

        self.status_label.config(text=f"Encrypted: {encrypted_path}", fg="#00FF41")
        messagebox.showinfo("Success", f"File Encrypted Successfully!\nSaved at: {encrypted_path}")

    def decrypt_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        with open(self.file_path, "rb") as f:
            data = f.read()

        salt, iv, tag, ciphertext = data[:16], data[16:28], data[28:44], data[44:]
        key = PBKDF2HMAC(algorithm=hashes.SHA256(), iterations=600000, salt=salt, length=32).derive(password.encode())

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()

        new_file_path = filedialog.asksaveasfilename()
        if not new_file_path:
            return

        with open(new_file_path, "wb") as f:
            f.write(decrypted)

        self.status_label.config(text=f"Decrypted: {new_file_path}", fg="#FFD700")
        messagebox.showinfo("Success", f"File Decrypted Successfully!\nSaved at: {new_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrabCryptApp(root)
    root.mainloop()
