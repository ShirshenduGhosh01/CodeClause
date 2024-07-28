import os
import pygame
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x500")
        self.root.resizable(True, True)
        self.root.configure(bg='#2C3E50')

        self.is_paused = False
        self.current_song_index = 0
        self.playlist = []

        pygame.mixer.init()

        style = ttk.Style()
        style.configure("TFrame", background="#2C3E50")
        style.configure("TLabelFrame", background="#2C3E50", foreground="white")
        style.configure("TButton", background="#1ABC9C", foreground="black")
        style.configure("TLabel", background="#2C3E50", foreground="white")

        playlist_frame = ttk.LabelFrame(self.root, text="Playlist")
        playlist_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.playlist_box = tk.Listbox(playlist_frame, selectmode=tk.SINGLE, bg='#34495E', fg='white', selectbackground='#1ABC9C')
        self.playlist_box.pack(padx=10, pady=10, fill="both", expand=True)

        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack()

        self.play_button = ttk.Button(control_frame, text="Play", command=self.play_music)
        self.play_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = ttk.Button(control_frame, text="Pause", command=self.pause_music)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_music)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)

        volume_frame = ttk.Frame(self.root, padding=10)
        volume_frame.pack()

        ttk.Label(volume_frame, text="Volume:").pack(side=tk.LEFT)
        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side=tk.LEFT, padx=10)

        self.select_folder_button = ttk.Button(self.root, text="Select Folder", command=self.load_folder)
        self.select_folder_button.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, orient='horizontal', mode='determinate', length=380)
        self.progress.pack(pady=10)

    def load_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.playlist = [os.path.join(folder_selected, file) for file in os.listdir(folder_selected) if file.endswith(('.mp3', '.wav'))]
            if self.playlist:
                self.playlist_box.delete(0, tk.END)
                for file in self.playlist:
                    self.playlist_box.insert(tk.END, os.path.basename(file))
                messagebox.showinfo("Folder Loaded", f"Loaded {len(self.playlist)} songs.")
            else:
                messagebox.showwarning("No Songs Found", "No mp3 or wav files found in the selected folder.")

    def play_music(self):
        if not self.playlist:
            messagebox.showwarning("No Folder Selected", "Please select a folder with music files.")
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            selected_song_index = self.playlist_box.curselection()
            if selected_song_index:
                self.current_song_index = selected_song_index[0]
            self.play_song()

    def play_song(self):
        if self.current_song_index >= len(self.playlist):
            self.current_song_index = 0

        song = self.playlist[self.current_song_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.update_progress_bar()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.root.after(1000, self.check_song_end)

    def check_song_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.current_song_index += 1
                self.play_song()

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_paused = False
        self.progress.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_progress_bar(self):
        song_length = pygame.mixer.Sound(self.playlist[self.current_song_index]).get_length()
        self.progress.config(maximum=song_length)
        self.update_progress()

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000
            self.progress['value'] = current_time
            self.root.after(1000, self.update_progress)
        else:
            self.progress.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
