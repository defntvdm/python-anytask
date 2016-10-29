#!/usr/bin/env python3

"""Окно выбора количества цветов и размера поля, запуск"""

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QMessageBox # pylint: disable-msg=E0611
import sys
import argparse
import os
import game


class MainWindow(QWidget):
    """Сама форма выбора"""
    def __init__(self, width, altitude, colors):
        super().__init__()

        self.setWindowTitle("Размеры")

        lab_width = QLabel("Ширина", self)
        lab_height = QLabel("Высота", self)
        lab_colors = QLabel("Количество цветов", self)

        self.width = QLineEdit(str(width), self)
        self.height = QLineEdit(str(altitude), self)
        self.colors = QLineEdit(str(colors), self)

        start = QPushButton("Старт", self)
        start.clicked.connect(self.start)
        start.setShortcut("ctrl+s")

        scores = QPushButton("Рекорды", self)
        scores.clicked.connect(self.scores)

        grid = QGridLayout(self)

        grid.addWidget(lab_width, 0, 0)
        grid.addWidget(self.width, 0, 1)

        grid.addWidget(lab_height, 1, 0)
        grid.addWidget(self.height, 1, 1)

        grid.addWidget(lab_colors, 2, 0)
        grid.addWidget(self.colors, 2, 1)

        grid.addWidget(start, 3, 0)
        grid.addWidget(scores, 3, 1)

    def start(self):
        """"Функция старта с заданными параметрами"""
        width = int(self.width.text())
        height = int(self.height.text())
        colors = int(self.colors.text())
        if colors > 8 or colors < 1:
            reply = QMessageBox.question(self, "Message", "Количество цветов от 1 до 8"\
                    + "\nВыйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                exit(0)
            else:
                return
        if width*height > 1000 and colors == 1:
            reply = QMessageBox.question(self, "Message",\
                    "Плохое соотношение размера поля и количества цветов"\
                    + "\nВыйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                exit(0)
            else:
                return
        if (width < 2 or height < 2) and colors != 1:
            reply = QMessageBox.question(self, "Message", \
                    "Наврятли вы выиграете с такими настройками"\
                    + "\nВыйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                exit(0)
            else:
                return
        if width == 1 and colors == 1 and height == 1:
            reply = QMessageBox.question(self, "Message", "Нет ходов"\
                    + "\nВыйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                exit(0)
            else:
                return
        if width > 100 and height > 100:
            reply = QMessageBox.question(self, "Message", "Большое поле"\
                    + "\nВыйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                exit(0)
            else:
                return
        game.play(self, width, height, colors)
        self.setVisible(False)

    def scores(self):
        "Показ доски рекордов"
        file = os.path.join("Scores", "".join([self.height.text(), ",",\
                        self.width.text(), ",", self.colors.text(), ".txt"]))
        if os.path.exists(file):
            with open(file) as output:
                lst = []
                for line in output:
                    lst.append(line.split())
            res = ""
            for element in lst:
                res = "".join([res, " ".join(element) + "\n"])
            reply = QMessageBox.question(self, "Message", res + "\nВыйти?", QMessageBox.Yes |\
                                                               QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                exit(0)
            else:
                return
        else:
            reply = QMessageBox.question(self, "Message", "В этом режиме нет рекордов"\
                            + "\nВыйти?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                exit(0)
            else:
                return

def get_args():
    """Парсим аргументы командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--altitude", type=int, default=14, help="Высота(по умолчанию 14)")
    parser.add_argument("-w", "--width", type=int, default=14, help="Ширина(по умолчанию 14)")
    parser.add_argument("-c", "--colors", type=int, default=5, \
                        help="Количество цветов, не больше 8(по умолчанию 5)")
    args = parser.parse_args()
    if args.colors > 8 or args.colors < 1:
        print("Количество цветов от 1 до 8")
        exit(0)
    if args.width*args.altitude > 1000 and args.colors == 1:
        print("Плохое соотношение размера и количества цветов")
        exit(0)
    if args.altitude < 2 or args.width < 2:
        if args.color != 1:
            print("Врят ли Вы выиграете на таком поле")
            exit(0)
    if args.altitude>800 and args.width>600 or args.altitude > 400 or args.width > 400:
        print("Большое поле")
    return args

def main():
    """Начало"""
    app = QApplication(sys.argv)
    args = get_args()
    window = MainWindow(args.width, args.altitude, args.colors)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
