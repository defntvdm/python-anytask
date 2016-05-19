"""
Растровый редактор Николаев Вадим КБ-201
Опции:
1 - Перо
2 - Линия
3 - Прямоугольник
4 - Эллипс
5 - Заливка
"""

from PyQt5.QtWidgets import QApplication, QWidget, QColorDialog, QPushButton, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.Qt import Qt, QRect
import sys
import logic
import copy
from PIL import Image, ImageDraw


class Button(QPushButton):
    def __init__(self, text, option, window):
        super().__init__(window)
        self.setText(text)
        self.option = option


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.size_h = 600
        self.size_w = 1000
        self.setGeometry(200, 200, self.size_w, self.size_h)
        self.setFixedSize(self.size_w, self.size_h)
        self.setWindowTitle("Растровый редактор")
        self.points = []
        self.preview = {}
        for _ in range(self.size_w):
            self.points.append([0 for _ in range(self.size_h)])
        self.qp = QPainter()
        self.width = 0
        self.left_x = 0
        self.top_y = 0
        self.height = 0
        self.last_x = 0
        self.last_y = 0
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        v_layout = QVBoxLayout()
        v_layout.addStretch(1)
        self.option = 1
        self.thickness = 1
        self.color = QColor(0, 0, 0)
        self.color_changer = QPushButton(self)
        self.color_changer.setFixedSize(30, 30)
        self.color_changer.setStyleSheet("background: black")
        self.color_changer.clicked[bool].connect(self.change_color)
        self.thick_changer = QSlider(Qt.Horizontal, self)
        self.thick_changer.setRange(1, 9)
        self.thick_changer.setFixedSize(50, 10)
        self.thick_changer.valueChanged[int].connect(self.change_thickness)
        self.thick_lab = QLabel("W: 1", self)
        pen = Button("Перо", 1, self)
        pen.clicked[bool].connect(self.change_option)
        line = Button("Линия", 2, self)
        line.clicked[bool].connect(self.change_option)
        rect = Button("Прямоугольник", 3, self)
        rect.clicked[bool].connect(self.change_option)
        ellipse = Button("Эллипс", 4, self)
        ellipse.clicked[bool].connect(self.change_option)
        fill = Button("Заливка", 5, self)
        fill.clicked[bool].connect(self.change_option)
        clean = QPushButton("Очистить", self)
        clean.clicked[bool].connect(self.clean)
        save = QPushButton("Сохранить", self)
        save.clicked[bool].connect(self.save)
        load = QPushButton("Загрузить", self)
        load.clicked[bool].connect(self.load)
        h_layout.addWidget(save)
        h_layout.addWidget(load)
        h_layout.addWidget(self.thick_lab)
        h_layout.addWidget(self.thick_changer)
        h_layout.addWidget(pen)
        h_layout.addWidget(line)
        h_layout.addWidget(rect)
        h_layout.addWidget(ellipse)
        h_layout.addWidget(fill)
        h_layout.addWidget(clean)
        h_layout.addWidget(self.color_changer)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
        self.figure_x1 = 0
        self.figure_y1 = 0

    def clean(self):
        for i in range(self.size_w):
            for j in range(self.size_h):
                self.points[i][j] = 0
        self.left_x = 0
        self.top_y = 0
        self.width = self.size_w
        self.height = self.size_h
        self.repaint()

    def change_color(self):
        self.color = QColorDialog.getColor()
        self.color_changer.setStyleSheet("background: %s" % self.color.name())
        self.top_y = 0
        self.left_x = 0
        self.width = self.size_w
        self.height = self.size_h
        self.repaint(self.left_x, self.top_y, self.width, self.height)

    def change_option(self):
        sender = self.sender()
        self.option = sender.option

    def change_thickness(self):
        self.thickness = self.thick_changer.value()
        self.thick_lab.setText("W: "+str(self.thickness))

    def save(self):
        image = Image.new('RGB', (self.size_w, self.size_h), (0, 0, 0, 0))
        drawer = ImageDraw.Draw(image)
        for i in range(self.size_w):
            for j in range(self.size_h):
                if self.points[i][j]:
                    drawer.point((i, j), (self.points[i][j].red(),\
                                          self.points[i][j].green(),\
                                          self.points[i][j].blue()))
                else:
                    drawer.point((i, j), tuple([255, 255, 255]))
        name = QFileDialog.getSaveFileName(self, filter="Images (*.png)")[0]
        if name:
            image.save(name, 'PNG')
        self.left_x = 0
        self.top_y = 0
        self.width = self.size_w
        self.height = self.size_h
        self.repaint()

    def load(self):
        picture_name = QFileDialog.getOpenFileName(self)[0]
        if picture_name.split('.')[-1] != 'png' or not picture_name:
            return
        image = Image.open(picture_name)
        data = image.load()
        size_y = min(image.size[1], self.size_h)
        size_x = min(image.size[0], self.size_w)
        for x in range(size_x):
            for y in range(size_y):
                x_y = data[x, y]
                self.points[x][y] = QColor(x_y[0], x_y[1], x_y[2])
        self.left_x = 0
        self.top_y = 0
        self.width = self.size_w
        self.height = self.size_h
        self.repaint()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        if self.option == 1:
            logic.add_thickness_point(self.points, x, y, self.color, self.thickness)
        elif self.option == 2:
            self.figure_x1 = x
            self.figure_y1 = y
        elif self.option == 3:
            self.figure_x1 = x
            self.figure_y1 = y
        elif self.option == 4:
            self.figure_x1 = x
            self.figure_y1 = y
        else:
            logic.brush(x, y, self.points, self.color, self.size_w, self.size_h)
            self.left_x = 0
            self.top_y = 0
            self.width = self.size_w
            self.height = self.size_h
            self.repaint()
            return
        self.last_x = x
        self.last_y = y
        self.left_x = x-self.thickness
        self.width = 2*self.thickness
        self.top_y = y-self.thickness
        self.height = 2*self.thickness
        self.repaint(self.left_x, self.top_y, self.width, self.height)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        if  -1 < x < self.size_w-self.thickness and -1 < y < self.size_h-self.thickness:
                self.left_x = int(min(x, self.last_x)) - self.thickness
                self.top_y = int(min(y, self.last_y)) - self.thickness
                self.width = int(abs(self.left_x-max(x, self.last_x)))+self.thickness
                self.height = int(abs(self.top_y-max(y, self.last_y)))+self.thickness
        else:
            return
        if self.option == 1:
                logic.draw_line(x, y, self.last_x, self.last_y, self.points, self.color, self.thickness)
                self.last_x = x
                self.last_y = y
        elif self.option == 2:
            self.preview.clear()
            logic.draw_line(x, y, self.figure_x1, self.figure_y1, self.preview, self.color, self.thickness)
        elif self.option == 3:
            self.preview.clear()
            logic.draw_rect(x, y, self.figure_x1, self.figure_y1, self.preview, self.color, self.thickness)
        elif self.option == 4:
            self.preview.clear()
            logic.draw_ellipse(x, y, self.figure_x1, self.figure_y1, self.preview, self.color, self.thickness,\
                               self.size_w, self.size_h)
        self.repaint(self.left_x, self.top_y, self.width, self.height)

    def mouseReleaseEvent(self, event):
        if 1 < self.option < 5:
            self.figure_x1 = 0
            self.figure_y1 = 0
            for point, color in self.preview.items():
                self.points[point[0]][point[1]] = color
            self.preview.clear()
            self.top_y = 0
            self.left_x = 0
            self.width = self.size_w
            self.height = self.size_h
            self.repaint(0, 0, self.size_w, self.size_h)

    def paintEvent(self, QPaintEvent):
        self.qp.begin(self)
        for i in range(self.left_x, self.left_x+self.width):
            for j in range(self.top_y, self.top_y+self.height):
                if self.points[i][j]:
                    self.qp.setPen(self.points[i][j])
                    self.qp.drawPoint(i, j)
        for point, color in self.preview.items():
            self.qp.setPen(color)
            self.qp.drawPoint(point[0], point[1])
        self.qp.end()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
