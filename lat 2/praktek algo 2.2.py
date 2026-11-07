
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import (
    QMediaPlayer,
    QMediaContent,
    QMediaPlaylist
)


class SimpleMediaPlayer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Media Player")
        self.setGeometry(300, 300, 600, 250)

        # Media Player
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        # Main Layout
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        # Buttons
        btn_layout = QHBoxLayout()

        self.play_btn = QPushButton("▶ Play")
        self.pause_btn = QPushButton("⏸ Pause")
        self.stop_btn = QPushButton("⏹ Stop")
        self.add_btn = QPushButton("+ Add File")

        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.add_btn)

        # Playlist display
        self.song_list = QListWidget()

        # Progress slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)

        # Label
        self.current_label = QLabel("Belum ada lagu")
        self.current_label.setAlignment(Qt.AlignCenter)

        # Add widgets
        layout.addLayout(btn_layout)
        layout.addWidget(QLabel("Daftar Lagu:"))
        layout.addWidget(self.song_list)
        layout.addWidget(self.slider)
        layout.addWidget(self.current_label)

        # Signals
        self.play_btn.clicked.connect(self.player.play)
        self.pause_btn.clicked.connect(self.player.pause)
        self.stop_btn.clicked.connect(self.player.stop)
        self.add_btn.clicked.connect(self.add_file)

        self.slider.sliderMoved.connect(
            self.player.setPosition
        )

        self.player.positionChanged.connect(
            self.slider.setValue
        )

        self.player.durationChanged.connect(
            self.slider.setRange
        )

        self.song_list.currentRowChanged.connect(
            self.playlist.setCurrentIndex
        )

        self.playlist.currentIndexChanged.connect(
            self.song_list.setCurrentRow
        )

    def add_file(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Pilih File Audio",
            "",
            "Audio Files (*.mp3 *.wav)"
        )

        for file in files:

            name = file.replace("\\", "/").split("/")[-1]

            self.playlist.addMedia(
                QMediaContent(
                    QUrl.fromLocalFile(file)
                )
            )

            self.song_list.addItem(name)

        if files:
            self.current_label.setText(
                "File audio berhasil ditambahkan"
            )

    def closeEvent(self, event):
        self.player.stop()
        event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SimpleMediaPlayer()
    window.show()

    sys.exit(app.exec_())
