"""Окно игры"""

import sys
import logic
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QMessageBox, QInputDialog # pylint: disable-msg=E0611
from PyQt5.QtGui import QColor # pylint: disable-msg=E0611
import os

SIZE = 20
LIST_I = []
LIST_J = []

class Game(QMainWindow):
    """Само окно"""
    def __init__(self, window, width, height, colors):
        super().__init__(window)
        self.setWindowTitle("Кубики")
        self.colors = {0: QColor(255, 255, 255), 1: QColor(255, 0, 0), 2: QColor(0, 255, 0),\
                       3: QColor(0, 0, 255), 4: QColor(255, 255, 0), \
                       5: QColor(255, 0, 255), 6: QColor(0, 255, 255),\
                       7: QColor(128, 0, 128), 8: QColor(0, 128, 128)}
        self.result = 0
        self.height = height
        self.width = width
        self.res_lab = QLabel("Счёт: "+str(self.result), self)
        self.res_lab.setGeometry(0, height*SIZE, 700, 20)
        self.num_colors = colors
        self.setFixedSize(width*SIZE, height*SIZE+20)
        self.table = logic.get_table(height, width, self.num_colors)
        self.field = self.get_field()
        restart = QPushButton("Сначала", self)
        restart.clicked.connect(self.again)
        restart.setGeometry(width*SIZE - 70, height*SIZE, 70, 20)

    def get_field(self):
        """Поле клеток"""
        field = []
        for i in range(self.height):
            lst = []
            for j in range(self.width):
                lst.append(Cell(self, i, j, self.colors[self.table[i][j]]))
            field.append(lst)
        return field

    def again(self):
        """Перезапуск приложения"""
        executable = sys.executable
        args = sys.argv
        args.insert(0, sys.executable)
        os.execvp(executable, args)

    def mouseReleaseEvent(self, event):
        """События отжатия мыши"""
        global LIST_I, LIST_J
        i = event.y()//SIZE
        j = event.x()//SIZE
        if i > self.height - 1 or j > self.width - 1:
            return
        logic.burst(i, j, self.table, LIST_I, LIST_J)
        logic.shift_down(self.table)
        logic.shift_left(self.table, LIST_J)
        self.result = logic.recount_result(self.table)
        self.res_lab.setText("Счёт: "+str(self.result))
        self.change_colors()
        if not logic.is_there_cell_to_burst(self.table):
            self.return_results()
        LIST_I.clear()
        LIST_J.clear()

    def return_results(self):
        "Вывод результата"
        if not os.path.exists("Scores"):
            os.mkdir("Scores")
        file = os.path.join("Scores", "".join([str(self.height), ",",\
                                    str(self.width), ",", str(self.num_colors), ".txt"]))
        lst = []
        res_lst = [str(self.result)]
        try:
            with open(file) as output:
                for line in output:
                    if line != "":
                        lst.append(line.split())
            if len(lst) == 10:
                if int(lst[-1][-1]) >= self.result:
                    reply = QMessageBox.question(self, "Message",\
                                    """Вы не вошли в 10 лучших в это режиме игры \n
                                    Выйти?""", QMessageBox.Yes | \
                                    QMessageBox.No, QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        exit(0)
                    else:
                        self.again()
                else:
                    with open(file, "w") as output:
                        text, okey = QInputDialog.getText(self, "Результат", "Ваш результат: "\
                                            + str(self.result) + "\nВведите ваше имя:")
                        if okey:
                            res_lst.insert(0, text)
                            for i in range(len(lst)):
                                if int(lst[i][-1]) < self.result:
                                    lst.insert(i, res_lst)
                            for i in range(10):
                                output.write(" ".join(lst[i])+"\n")
                        else:
                            return
                    self.show_scores(lst)
            else:
                with open(file, "w") as output:
                    text, okey = QInputDialog.getText(self, "Результат", "Ваш результат: " + \
                                    str(self.result) + "\nВведите ваше имя:")
                    if okey:
                        flag = True
                        res_lst.insert(0, text)
                        for i in range(len(lst)):
                            if int(lst[i][-1]) < self.result:
                                lst.insert(i, res_lst)
                                flag = False
                                break
                        if flag:
                            lst.append(res_lst)
                        for element in lst:
                            output.write(" ".join(element)+"\n")
                self.show_scores(lst)
        except FileNotFoundError:
            with open(file, "w") as output:
                text, okey = QInputDialog.getText(self, "Результат", "Ваш результат: " + \
                                    str(self.result) + "\nВведите ваше имя:")
                if okey:
                    res_lst.insert(0, text)
                    output.write(" ".join(res_lst) + "\n")
            self.show_scores(res_lst)

    def show_scores(self, lst):
        "Показ доски рекордов"
        res = ""
        for element in lst:
            res = "".join([res, " ".join(element) + "\n"])
        reply = QMessageBox.question(self, "Message", res + "\nВыйти?", \
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            exit(0)
        else:
            self.again()

    def change_colors(self):
        """Смена цвета у клетки"""
        for i in LIST_I:
            for j in LIST_J:
                if self.table[i][j] == 0 and self.field[i][j].color == self.colors[0]:
                    continue
                self.field[i][j].set_color(self.colors[self.table[i][j]])


class Cell(QLabel):
    """Кубик"""
    def __init__(self, window, i, j, color):
        super().__init__(window)
        self.color = color
        self.setGeometry(SIZE*j, SIZE*i, SIZE, SIZE)
        self.set_color(color)

    def set_color(self, color):
        """Устанавливаем цвет"""
        self.setStyleSheet("QLabel { background-color: %s }" % color.name())


def play(window, width, height, colors):
    """Запуск приложения"""
    game = Game(window, width, height, colors)
    game.show()
