import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp

# Path to save downloaded videos and audio files
VIDEO_DIR = r"D:\Videos\Youtube Downloads\Videos"
AUDIO_DIR = r"D:\Videos\Youtube Downloads\Audio"


class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        root.title("YouTube Downloader")
        root.geometry("500x220")

        self.output_path = tk.StringVar(value=VIDEO_DIR)
        self.mode = tk.StringVar(value="mp4")
        self.status_var = tk.StringVar(value="Ready")
        self.busy = False

        tk.Label(root, text="Paste URL (Enter = Download)").pack(pady=(10, 0))

        self.url_entry = tk.Entry(root, width=60)
        self.url_entry.pack(pady=5)
        self.url_entry.focus()

        fmt = tk.Frame(root)
        fmt.pack()
        tk.Radiobutton(fmt, text="MP4", variable=self.mode, value="mp4", command=self.update_folder).pack(side="left", padx=10)
        tk.Radiobutton(fmt, text="MP3", variable=self.mode, value="mp3", command=self.update_folder).pack(side="left")

        tk.Button(root, text="DOWNLOAD", font=("Arial", 14, "bold"), bg="green", fg="white",
                  command=self.start_download).pack(fill="x", padx=10, pady=10)

        tk.Button(root, text="Change Folder", command=self.change_folder).pack()

        tk.Label(root, textvariable=self.status_var, fg="blue").pack(pady=5)

        root.bind("<Return>", self.start_download)

    def update_folder(self):
        self.output_path.set(AUDIO_DIR if self.mode.get() == "mp3" else VIDEO_DIR)

    def change_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def start_download(self, event=None):
        if self.busy:
            return

        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Paste a URL first")
            return

        self.url_entry.delete(0, tk.END)
        threading.Thread(target=self.download, args=(url,), daemon=True).start()

    def progress_hook(self, d):
        if d["status"] == "downloading":
            mb = d.get("downloaded_bytes", 0) / 1024 / 1024
            eta = d.get("eta")
            msg = f"{mb:.2f} MB"
            if eta:
                msg += f" | ETA: {eta}s"
            self.status_var.set(msg)
        elif d["status"] == "finished":
            # still needs merging/extracting at this point
            self.status_var.set("Processing...")

    def download(self, url):
        self.busy = True
        self.status_var.set("Starting...")

        out_dir = self.output_path.get()
        os.makedirs(out_dir, exist_ok=True)

        opts = {
            "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
            "progress_hooks": [self.progress_hook],
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }

        if self.mode.get() == "mp3":
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        else:
            opts["format"] = "bestvideo+bestaudio/best"
            opts["merge_output_format"] = "mp4"

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            self.status_var.set("Done")
        except Exception as e:
            self.status_var.set("Error")
            messagebox.showerror("Error", str(e))

        self.busy = False


if __name__ == "__main__":
    root = tk.Tk()
    YouTubeDownloader(root)
    root.mainloop()
