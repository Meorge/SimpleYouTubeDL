from PyQt5.QtCore import QThread, pyqtSignal
import youtube_dl
import traceback

class TrackDownloader(QThread):
    progress_updated = pyqtSignal(object)
    error_encountered = pyqtSignal(object)

    def __init__(self, parent, url):
        super(TrackDownloader, self).__init__(parent)
        self.url = url

    def run(self):
        mp3_options = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320"
            }],
            "prefer_ffmpeg": True,
            "keepvideo": False,
            "quiet": True,
            "progress_hooks": [self.updateProgress]
        }

        try:
            with youtube_dl.YoutubeDL(mp3_options) as ydl:
                ydl.download([self.url])
        except Exception as e:
            self.progress_updated.emit({"status": "error"})
            self.error_encountered.emit(traceback.format_exc())


    def updateProgress(self, d):
        self.progress_updated.emit(d)