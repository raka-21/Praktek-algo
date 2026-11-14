import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.setGeometry(300, 300, 600, 450)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignCenter)

        self.welcome_label = QLabel("Welcome to the Main Application!")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 20px;")

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(93)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                background-color: #f0f0f0;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: green;
            }
        """)

        self.status_label = QLabel("Loading data...")

        layout.addStretch()
        layout.addWidget(self.welcome_label)
        layout.addSpacing(40)
        layout.addWidget(self.progress)
        layout.addSpacing(40)
        layout.addWidget(self.status_label)
        layout.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Buat Splash Screen
    pixmap = QPixmap(450, 250)
    pixmap.fill(QColor("#2c3e50"))
    splash = QSplashScreen(pixmap)
    splash.show()

    # Simulasi loading
    steps = ["Memuat modul...", "Menyiapkan antarmuka...", "Loading data...", "Selesai..."]
    for i, step in enumerate(steps):
        splash.showMessage(f"\n\n   {step} ({(i + 1) * 25}%)", Qt.AlignBottom | Qt.AlignLeft, Qt.white)
        app.processEvents()
        time.sleep(0.7)

    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())