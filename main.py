import os
import tkinter as tk
import subprocess
import random
from pydub import AudioSegment

SONGS_DIR = "songs"
CLIP_DURATION = 10 * 1000  # 10 seconds in milliseconds

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Song Flashcards")
        self.root.geometry("400x250")

        # Load songs
        self.songs = [
            f for f in os.listdir(SONGS_DIR)
            if f.lower().endswith((".mp3", ".wav"))
        ]
        if not self.songs:
            raise RuntimeError("No audio files found in /songs")

        random.shuffle(self.songs)
        self.index = 0
        self.proc = None

        # Flashcard label
        self.card = tk.Label(
            root,
            text="???",
            font=("Helvetica", 20, "bold"),
            wraplength=350,
            pady=40
        )
        self.card.pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="▶ Play", width=10, command=self.play_song).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="👁 Reveal", width=10, command=self.reveal_song).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Next →", width=10, command=self.next_song).grid(row=0, column=2, padx=5)

    def play_song(self):
        # Stop previous playback
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()

        song_path = os.path.join(SONGS_DIR, self.songs[self.index])

        # Load song length with pydub
        audio = AudioSegment.from_file(song_path)
        max_start = max(0, len(audio) - CLIP_DURATION)
        start_ms = random.randint(0, max_start)

        # ffplay: -ss = start time (seconds), -t = duration (seconds)
        self.proc = subprocess.Popen(
            [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel", "quiet",
                "-ss", str(start_ms / 1000),
                "-t", str(CLIP_DURATION / 1000),
                song_path
            ]
        )

    def reveal_song(self):
        self.card.config(text=self.songs[self.index])

    def next_song(self):
        # Stop playback if any
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()

        self.index = (self.index + 1) % len(self.songs)
        self.card.config(text="???")


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

