import pyaudio
import wave
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import time

class VoiceRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.root.geometry("500x500")
        self.root.resizable(True, True)
        self.root.configure(bg='#2C3E50')

        self.recording = False
        self.paused = False
        self.frames = []
        self.start_time = None
        self.pause_start_time = None
        self.total_paused_time = 0

        self.create_widgets()

    def create_widgets(self):
        # Style configuration
        style = ttk.Style()
        style.configure("TFrame", background="#2C3E50")
        style.configure("TLabelFrame", background="#2C3E50", foreground="black")
        style.configure("TButton", background="#1ABC9C", foreground="black")
        style.configure("TLabel", background="#2C3E50", foreground="white")

        self.status_label = ttk.Label(self.root, text="Press Record to start", font=("Helvetica", 14))
        self.status_label.pack(pady=10)

        self.timer_label = ttk.Label(self.root, text="00:00", font=("Helvetica", 14))
        self.timer_label.pack(pady=10)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.record_button = ttk.Button(button_frame, text="Record", command=self.start_recording)
        self.record_button.grid(row=0, column=0, padx=10)
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10)
        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_recording, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=2, padx=10)

        # Save button below other buttons and making it circular
        save_button_frame = ttk.Frame(self.root)
        save_button_frame.pack(pady=10)
        self.save_button = tk.Button(save_button_frame, text="Save", command=self.save_recording, state=tk.DISABLED, bg="#1ABC9C", fg="black", font=("Helvetica", 12))
        self.save_button.config(height=2, width=10, borderwidth=0, highlightthickness=0)
        self.save_button.pack()

    def start_recording(self):
        self.recording = True
        self.paused = False
        self.frames = []
        self.start_time = time.time()
        self.total_paused_time = 0
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL, text="Pause")
        self.status_label.config(text="Recording...")
        self.stream = self.get_stream()
        self.update_timer()
        self.record()

    def stop_recording(self):
        self.recording = False
        self.paused = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.status_label.config(text="Recording Stopped")
        self.stream.stop_stream()
        self.stream.close()

    def save_recording(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Wave files", "*.wav")])
        if filepath:
            self.save_wave_file(filepath)
            messagebox.showinfo("Voice Recorder", "Recording saved successfully!")
            self.status_label.config(text="Press Record to start")
            self.timer_label.config(text="00:00")

    def pause_recording(self):
        if not self.paused:
            self.paused = True
            self.pause_start_time = time.time()
            self.status_label.config(text="Recording Paused")
            self.pause_button.config(text="Resume")
        else:
            self.paused = False
            self.total_paused_time += time.time() - self.pause_start_time
            self.status_label.config(text="Recording...")
            self.pause_button.config(text="Pause")
            self.record()

    def get_stream(self):
        p = pyaudio.PyAudio()
        return p.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=44100,
                      input=True,
                      frames_per_buffer=1024)

    def record(self):
        if self.recording and not self.paused:
            data = self.stream.read(1024)
            self.frames.append(data)
            self.root.after(1, self.record)

    def update_timer(self):
        if self.recording:
            if not self.paused:
                elapsed_time = time.time() - self.start_time - self.total_paused_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def save_wave_file(self, filepath):
        p = pyaudio.PyAudio()
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorder(root)
    root.mainloop()
