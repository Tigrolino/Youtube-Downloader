# YouTube Downloader

Simple Python script to download YouTube videos as MP4 or MP3 at the best available quality.

Paste a link, pick MP4 or MP3, hit enter. That's it.

## Requirements

- Python 3.8+
- yt-dlp (`pip install yt-dlp`)
- ffmpeg installed and on your PATH (needed for MP3 extraction and merging MP4 video/audio)
- tkinter - usually comes with Python, on Linux you might need `sudo apt install python3-tk`

## Usage

```bash
python youtube_downloader.py
```

Paste a URL, choose MP4 or MP3, and press Enter or click DOWNLOAD. Files go to `D:\Videos\Youtube Downloads\Videos` (or `...\Audio` for mp3) by default, or click "Change Folder" to pick your own.

## License

MIT
