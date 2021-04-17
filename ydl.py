from PyQt5.QtWidgets import QErrorMessage, QFormLayout, QMainWindow, QLineEdit, QMessageBox, QProgressBar, QPushButton, QWidget, QLabel
from download_thread import TrackDownloader

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.url_box = QLineEdit()
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_button_clicked)
        self.progress_label = QLabel()
        self.progress_bar = QProgressBar()

        self.layout = QFormLayout()
        self.layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.layout.addRow("YouTube URL", self.url_box)
        self.layout.addRow("", self.download_button)
        self.layout.addRow(self.progress_label, self.progress_bar)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.setMinimumSize(400, 150)

    def download_button_clicked(self):
        self.url_box.setEnabled(False)
        self.download_button.setEnabled(False)


        url = self.url_box.text()
        download_thread = TrackDownloader(self, url)
        download_thread.progress_updated.connect(self.progress_updated)
        download_thread.error_encountered.connect(self.error_encountered)
        download_thread.start()

    def progress_updated(self, progress):
        status = progress["status"]

        if status == "downloading":
            downloaded_bytes = progress["downloaded_bytes"]
            total_bytes_est = progress["total_bytes_estimate"] if "total_bytes_estimate" in progress else 0
            total_bytes = progress["total_bytes"] if "total_bytes" in progress else total_bytes_est

            self.progress_bar.setRange(0, total_bytes)
            self.progress_bar.setValue(downloaded_bytes)

            if total_bytes != 0:
                self.progress_label.setText(f"{int((downloaded_bytes / total_bytes) * 100)}%")
            else:
                self.progress_label.setText("Downloading")

        elif status == "error":
            self.url_box.setEnabled(True)
            self.download_button.setEnabled(True)
            self.progress_label.setText("Error")
            self.progress_bar.setValue(0)

        elif status == "finished":
            self.url_box.setEnabled(True)
            self.download_button.setEnabled(True)
            self.progress_label.setText("Downloaded")


    def error_encountered(self, exception: str):
        print(exception)
        error_msg = QMessageBox()
        error_msg.setWindowTitle("Error")
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setText("Error while downloading song.")
        error_msg.setInformativeText("Make sure the URL is valid.")
        error_msg.resize(600,400)
        error_msg.setDetailedText(exception)
        error_msg.exec_()


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    exit(app.exec_())