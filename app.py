import sounddevice as sd
import numpy as np
import keyboard
import tkinter as tk
from tkinter import ttk
import threading
import time

# === Core Settings ===
running = False
last_trigger_time = 0
COOLDOWN = 0.3  # seconds

# Default threshold
sensitivity_threshold = 0.25

def audio_callback(indata, frames, time_info, status):
    global last_trigger_time
    global running
    global sensitivity_threshold

    if not running:
        return

    volume_norm = np.linalg.norm(indata) * 10
    now = time.time()

    if volume_norm > sensitivity_threshold and (now - last_trigger_time > COOLDOWN):
        print(f"🎵 Beat! Volume: {volume_norm:.2f}")
        keyboard.press_and_release('f5')
        last_trigger_time = now

def start_stream():
    global running
    if not running:
        running = True
        print("🔊 Started listening for beats...")

def stop_stream():
    global running
    running = False
    print("⏹️ Stopped.")

def update_threshold(val):
    global sensitivity_threshold
    sensitivity_threshold = float(val)
    threshold_label.config(text=f"Sensitivity: {sensitivity_threshold:.2f}")

def audio_thread():
    with sd.InputStream(callback=audio_callback):
        while True:
            time.sleep(0.1)

# === GUI Setup ===
app = tk.Tk()
app.title("🎧 BeatSync RGB Controller")
app.geometry("400x220")
app.resizable(False, False)

title = ttk.Label(app, text="🎵 BeatSync RGB Controller", font=("Segoe UI", 16))
title.pack(pady=10)

# Start/Stop buttons
frame = ttk.Frame(app)
frame.pack()

start_btn = ttk.Button(frame, text="Start Listening", command=start_stream)
start_btn.grid(row=0, column=0, padx=10, pady=10)

stop_btn = ttk.Button(frame, text="Stop", command=stop_stream)
stop_btn.grid(row=0, column=1, padx=10, pady=10)

# Sensitivity slider
threshold_label = ttk.Label(app, text=f"Sensitivity: {sensitivity_threshold:.2f}")
threshold_label.pack()

sensitivity_slider = ttk.Scale(app, from_=0.05, to=1.0, value=sensitivity_threshold, command=update_threshold, length=300)
sensitivity_slider.pack(pady=5)

# Run audio listener in background
threading.Thread(target=audio_thread, daemon=True).start()

app.mainloop()
