#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QPoint
import sys
import logic


TUTOR = "Страна считывается пока зелёная точка не совпадёт с красной. Клик по синим точкам не считается. "\
            "Отрезки не должны пересекаться. Страны не должны накладывать друг на друга и пересекаться"

class Window(QWidget):
    def __init__(self):
        self.black = QColor(0, 0, 0)
        self.colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0 ,0, 255),\
                       QColor(128, 0, 128), QColor(128, 128, 0)]
        super().__init__()
        self.setGeometry(100, 100, 900,500)
        self.setFixedSize(1000, 500)
        self.flag_rects = True
        self.pen = False
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        self.b_stop_entering = QPushButton("Закончить ввод", self)
        self.b_stop_entering.clicked[bool].connect(self.stop_entering)
        hbox.addWidget(self.b_stop_entering)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle("Map")
        self.qp = QPainter()
        self.vertexes = []
        self.edges = []
        self.previous_point = QPoint()
        self.countries = []
        self.points_for_country = []

    def stop_entering(self):
        """Обработчик кнопки"""
        if len(self.points_for_country):
            QMessageBox.question(self, "Misstake", "Закончите вводить страну",
                                     QMessageBox.Ok, QMessageBox.Ok)
            self.b_stop_entering.setText("Закончить ввод")
            return
        self.flag_rects = not self.flag_rects
        if not self.flag_rects:
            self.b_stop_entering.setText("Продолжить ввод")
            if logic.is_there_intersection(self.edges):
                QMessageBox.question(self, "Misstake", "Отрезки не должны пересекаться",
                                     QMessageBox.Ok, QMessageBox.Ok)
                self.countries.clear()
                self.edges.clear()
                self.points_for_country.clear()
                self.vertexes.clear()
                self.flag_rects = True
                self.pen = False
                self.update()
                self.b_stop_entering.setText("Закончить ввод")
                return
            for country1 in self.countries:
                for country2 in self.countries:
                    if country1 == country2:
                        continue
                    else:
                        intersect = country1.intersected(country2)
                    if intersect:
                        QMessageBox.question(self, "Misstake", "Страны не должны накладываться друг на друга",
                                             QMessageBox.Ok, QMessageBox.Ok)
                        self.countries.clear()
                        self.edges.clear()
                        self.points_for_country.clear()
                        self.vertexes.clear()
                        self.flag_rects = True
                        self.pen = False
                        self.update()
                        self.b_stop_entering.setText("Закончить ввод")
                        return
            logic.get_neighbours(self.countries)
            logic.paint_graph(self.countries)
        else:
            self.b_stop_entering.setText("Закончить ввод")
            for country in self.countries:
                country.num_of_color = -1
                country.neighbours = []
                country.variants_of_color = [0, 1, 2, 3]
        self.update()

    def mousePressEvent(self, event):
        """Обработчик кликов"""
        if self.flag_rects:
            x = event.x()
            y = event.y()
            flag = True
            for vertex in self.vertexes:
                if vertex.x()-10<x<vertex.x()+10 and vertex.y()-10<y<vertex.y()+10:
                    x = vertex.x()
                    y = vertex.y()
                    flag = False
                    break
            point = QPoint(x, y)
            if len(self.points_for_country)>2:
                if point == self.points_for_country[0]:
                    self.edges.append(((self.previous_point.x(), self.previous_point.y()), (x, y)))
                    self.countries.append(logic.Country(self.points_for_country))
                    self.points_for_country.clear()
                    self.pen = False
                    self.update()
                    return
            if point in self.points_for_country:
                return
            if flag:
                self.vertexes.append(point)
            if not self.pen:
                self.points_for_country.append(point)
                self.previous_point = point
                self.update()
                self.pen = True
                return
            else:
                self.edges.append(((self.previous_point.x(), self.previous_point.y()),(x, y)))
                self.points_for_country.append(point)
                self.previous_point = point
            self.update()

    def paintEvent(self, event):
        """Рисовальщик"""
        self.qp.begin(self)
        self.qp.setPen(QColor(0, 0, 0))
        if self.flag_rects:
            for point in self.vertexes:
                if point in self.points_for_country:
                    if point in self.points_for_country:
                        self.qp.setPen(QColor(0, 0, 255))
                    if point == self.points_for_country[0]:
                        self.qp.setPen(QColor(255, 0, 0))
                    if point == self.points_for_country[-1]:
                        self.qp.setPen(QColor(0, 255, 0))
                self.qp.drawRect(point.x()-10, point.y()-10, 20, 20)
                self.qp.setPen(QColor(0, 0, 0))
        else:
            self.qp.setRenderHint(QPainter.Antialiasing)
            for country in self.countries:
                self.qp.setBrush(self.colors[country.num_of_color])
                self.qp.drawPolygon(country)
        for edge in self.edges:
            self.qp.drawLine(edge[0][0], edge[0][1], edge[1][0], edge[1][1])
        self.qp.end()


if __name__ == '__main__':
    print(TUTOR)
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())