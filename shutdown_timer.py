import subprocess
import tkinter as tk
from tkinter import ttk, messagebox


class ShutdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Shutdown Timer")
        self.root.geometry("430x330")
        self.root.resizable(False, False)

        self.running = False
        self.remaining = 0

        style = ttk.Style()
        try:
            style.theme_use("vista")
        except tk.TclError:
            pass

        frame = ttk.Frame(root, padding=24)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="PC Shutdown Timer",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(0, 6))

        ttk.Label(
            frame,
            text="Schedule a Windows shutdown and cancel it whenever you need.",
            wraplength=360,
            justify="center"
        ).pack(pady=(0, 20))

        input_frame = ttk.Frame(frame)
        input_frame.pack()

        ttk.Label(input_frame, text="Hours").grid(row=0, column=0, padx=5)
        ttk.Label(input_frame, text="Minutes").grid(row=0, column=1, padx=5)
        ttk.Label(input_frame, text="Seconds").grid(row=0, column=2, padx=5)

        self.hours = tk.StringVar(value="0")
        self.minutes = tk.StringVar(value="30")
        self.seconds = tk.StringVar(value="0")

        ttk.Spinbox(input_frame, from_=0, to=168, width=8, textvariable=self.hours).grid(row=1, column=0, padx=5, pady=5)
        ttk.Spinbox(input_frame, from_=0, to=59, width=8, textvariable=self.minutes).grid(row=1, column=1, padx=5, pady=5)
        ttk.Spinbox(input_frame, from_=0, to=59, width=8, textvariable=self.seconds).grid(row=1, column=2, padx=5, pady=5)

        self.display = ttk.Label(
            frame,
            text="00:30:00",
            font=("Consolas", 28, "bold")
        )
        self.display.pack(pady=18)

        buttons = ttk.Frame(frame)
        buttons.pack()

        self.start_button = ttk.Button(buttons, text="Start Shutdown", command=self.start)
        self.start_button.grid(row=0, column=0, padx=6)

        self.cancel_button = ttk.Button(buttons, text="Cancel Shutdown", command=self.cancel, state="disabled")
        self.cancel_button.grid(row=0, column=1, padx=6)

        self.status = ttk.Label(frame, text="Ready", anchor="center")
        self.status.pack(pady=16)

        ttk.Label(
            frame,
            text="Tip: Cancel Shutdown immediately stops the scheduled Windows shutdown.",
            wraplength=360,
            justify="center"
        ).pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_seconds(self):
        try:
            h = int(self.hours.get())
            m = int(self.minutes.get())
            s = int(self.seconds.get())
        except ValueError:
            raise ValueError("Enter whole numbers only.")

        if h < 0 or not 0 <= m <= 59 or not 0 <= s <= 59:
            raise ValueError("Minutes and seconds must be between 0 and 59.")
        total = h * 3600 + m * 60 + s
        if total < 1:
            raise ValueError("Set a countdown of at least 1 second.")
        return total

    def start(self):
        if self.running:
            return

        try:
            self.remaining = self.get_seconds()
        except ValueError as e:
            messagebox.showerror("Invalid time", str(e))
            return

        # Windows built-in shutdown scheduler.
        result = subprocess.run(
            ["shutdown", "/s", "/t", str(self.remaining)],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if result.returncode != 0:
            messagebox.showerror(
                "Could not schedule shutdown",
                result.stderr.strip() or "Windows could not schedule the shutdown."
            )
            return

        self.running = True
        self.start_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.status.config(text="Shutdown scheduled")
        self.tick()

    def tick(self):
        if not self.running:
            return

        if self.remaining <= 0:
            self.display.config(text="00:00:00")
            self.running = False
            self.start_button.config(state="normal")
            self.cancel_button.config(state="disabled")
            self.status.config(text="Windows shutdown should now begin.")
            return

        h, rem = divmod(self.remaining, 3600)
        m, s = divmod(rem, 60)
        self.display.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        self.remaining -= 1
        self.root.after(1000, self.tick)

    def cancel(self):
        if not self.running:
            return

        result = subprocess.run(
            ["shutdown", "/a"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if result.returncode == 0:
            self.running = False
            self.remaining = 0
            self.display.config(text="00:00:00")
            self.start_button.config(state="normal")
            self.cancel_button.config(state="disabled")
            self.status.config(text="Shutdown cancelled")
        else:
            messagebox.showerror(
                "Cancel failed",
                "Windows could not cancel the scheduled shutdown. It may have already started."
            )

    def on_close(self):
        if self.running:
            if messagebox.askyesno(
                "Shutdown scheduled",
                "A shutdown is currently scheduled. Cancel it before closing?"
            ):
                self.cancel()
                self.root.destroy()
        else:
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    ShutdownTimer(root)
    root.mainloop()
