from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QByteArray, Qt
import sys
import info
import subprocess


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.pwd = subprocess.Popen('pwd', shell=True, stdout=subprocess.PIPE).stdout.read().decode()

        self.button_open = QPushButton("Открыть", self)
        self.button_open.clicked.connect(self.open)
        self.button_open.setShortcut("ctrl+o")

        self.button_info = QPushButton("Инфо", self)
        self.button_info.clicked.connect(self.info)
        self.button_info.setShortcut("ctrl+i")

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        self.setWindowTitle("GIF")

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.button_open, 1, 0)
        layout.addWidget(self.button_info, 2, 0)

        self.setLayout(layout)
        self.open()

    def open(self):
        self.file = QFileDialog.getOpenFileName(self, "Open File", self.pwd)[0]
        if self.file == "":
            return
        self.information = info.Information(self, self.file)
        movie = QMovie(self.file, QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setSpeed(100)
        self.label.setMovie(movie)
        movie.start()

    def info(self):
        self.information.show()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()