import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui as pg

class AutoTyperApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AutoTyper")
        self.geometry("380x370")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        pg.FAILSAFE = True

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        self.style.configure(".", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        self.style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4")
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground="#89b4fa")
        
        self.style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            background="#89b4fa",
            foreground="#11111b",
            borderwidth=0,
            padding=8
        )
        self.style.map("Primary.TButton", background=[("active", "#b4befe")])

    def _create_widgets(self):
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        # Header Frame: Title on the left, Info button on the right
        header_frame = tk.Frame(container, bg="#1e1e2e")
        header_frame.pack(fill="x", pady=(0, 15))

        title_label = ttk.Label(header_frame, text="Auto Message Sender", style="Header.TLabel")
        title_label.pack(side="left")

        # Info Icon Button
        info_btn = tk.Button(
            header_frame,
            text="ℹ",
            font=("Segoe UI", 11, "bold"),
            bg="#313244",
            fg="#89b4fa",
            activebackground="#45475a",
            activeforeground="#b4befe",
            relief="flat",
            bd=0,
            width=3,
            cursor="hand2",
            command=self.show_instructions
        )
        info_btn.pack(side="right")

        # Message Entry
        ttk.Label(container, text="Message to Send:").pack(anchor="w")
        self.msg_entry = tk.Entry(container, bg="#313244", fg="#cdd6f4", insertbackground="white", 
                                  relief="flat", font=("Segoe UI", 10))
        self.msg_entry.pack(fill="x", pady=(4, 12), ipady=5)

        # Count Entry
        ttk.Label(container, text="Repeat Count:").pack(anchor="w")
        self.count_entry = tk.Entry(container, bg="#313244", fg="#cdd6f4", insertbackground="white", 
                                    relief="flat", font=("Segoe UI", 10))
        self.count_entry.pack(fill="x", pady=(4, 20), ipady=5)

        # Start Button
        self.start_btn = ttk.Button(container, text="Start Automation", style="Primary.TButton", command=self.start_thread)
        self.start_btn.pack(fill="x")

    def show_instructions(self):
        instructions = (
            "How to use AutoTyper:\n\n"
            "1. Enter the message you want to type.\n"
            "2. Enter how many times it should repeat.\n"
            "3. Click 'Start Automation'. The app will hide automatically.\n"
            "4. You have 5 SECONDS to click on your target chat box/input field.\n"
            "5. The app will type the text and press Enter automatically.\n\n"
            "🚨 Emergency Abort:\n"
            "If something goes wrong, slam your mouse cursor into ANY corner of your screen to stop it instantly."
        )
        messagebox.showinfo("Instructions & Safety", instructions)

    def show_floating_hud(self):
        """Creates an always-on-top translucent countdown badge in the top-right."""
        self.hud = tk.Toplevel(self)
        self.hud.overrideredirect(True)
        self.hud.attributes("-topmost", True)
        self.hud.configure(bg="#11111b")

        screen_w = self.winfo_screenwidth()
        self.hud.geometry(f"340x95+{screen_w - 360}+30")

        frame = tk.Frame(self.hud, bg="#181825", padx=12, pady=10, highlightbackground="#89b4fa", highlightthickness=1)
        frame.pack(fill="both", expand=True)

        self.hud_warning = tk.Label(
            frame,
            text="⚠️ Click on the chat box / input area NOW!",
            font=("Segoe UI", 9, "bold"),
            bg="#181825",
            fg="#f38ba8"
        )
        self.hud_warning.pack(anchor="center")

        self.hud_timer = tk.Label(
            frame,
            text="Starting in 5...",
            font=("Segoe UI", 12, "bold"),
            bg="#181825",
            fg="#f9e2af"
        )
        self.hud_timer.pack(pady=(4, 0))

    def start_thread(self):
        message = self.msg_entry.get().strip()
        count_str = self.count_entry.get().strip()

        if not message:
            messagebox.showwarning("Missing Input", "Please enter a message to send.")
            return

        try:
            count = int(count_str)
            if count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Input", "Repeat count must be a positive integer.")
            return

        self.withdraw()
        self.show_floating_hud()
        threading.Thread(target=self.run_automation, args=(message, count), daemon=True).start()

    def run_automation(self, message, count):
        for i in range(5, 0, -1):
            self.hud_timer.config(text=f"Starting in {i}s...")
            time.sleep(1)

        self.hud_warning.config(text="🚀 Sending messages...", fg="#a6e3a1")
        self.hud_timer.config(text="Do not touch the keyboard/mouse", fg="#cdd6f4")

        try:
            for _ in range(count):
                pg.typewrite(message)
                pg.press("enter")
                time.sleep(0.05)
        except pg.FailSafeException:
            # Handles emergency mouse flick abort cleanly
            pass

        self.hud.destroy()
        self.deiconify()


if __name__ == "__main__":
    app = AutoTyperApp()
    app.mainloop()