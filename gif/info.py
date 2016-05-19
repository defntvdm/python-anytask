from PyQt5.QtWidgets import QMainWindow, QLabel, QMessageBox, QDialog, QGridLayout
import logic

class Information(QDialog):
    def __init__(self, parent, file_name):
        super().__init__(parent)
        self.setWindowTitle("Инфо")
        grid = QGridLayout()
        bytes = logic.get_bytes(file_name)
        version = logic.get_version(bytes)
        lab_version = QLabel("Версия GIF: "+version, self)
        grid.addWidget(lab_version, 0, 0)
        global_width = logic.get_w(bytes)
        lab_global_width = QLabel("Глобальная ширина: "+str(global_width), self)
        grid.addWidget(lab_global_width, 1, 0)
        global_height = logic.get_h(bytes)
        lab_global_height = QLabel("Глобальная высота: "+str(global_height), self)
        grid.addWidget(lab_global_height, 2, 0)
        byte10 = logic.get_str_byte(bytes)
        existing_colors = logic.get_exsisting_colors(byte10)
        lab_exsisting_colors = QLabel("Глобальная палитра: "+existing_colors , self)
        grid.addWidget(lab_exsisting_colors, 3, 0)
        num_colors = logic.get_num_colors(byte10)
        lab_num_colors = QLabel("Число цветов: "+str(num_colors), self)
        grid.addWidget(lab_num_colors, 4, 0)
        #num = logic.miss_numbers(bytes)
        #print(bytes[num:num+4], num)
        self.setLayout(grid)