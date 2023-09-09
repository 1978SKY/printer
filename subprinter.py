import datetime
import os
import sys

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from ui.printer import Ui_Form
from utils import pictureUtil, configUtil

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class Sub_Ui_Form(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle("选择文件")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            start_time = self.__time_start()

            # 前置工作，清除上张图片的所有计算内容
            self.__pre_clean()

            file_path = dialog.selectedFiles()[0]
            self.textBrowser_10.setText(file_path)
            self.__display_image(file_path)

            if self.checkBox.isChecked():  # 计算覆盖率
                self.calculate_matrix()
            if self.checkBox_2.isChecked():  # 计算价格
                self.calculate_price()

            self.__time_end(start_time)

    # 更换皮肤
    def select_theme(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle("选择文件")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = dialog.selectedFiles()[0]
            self.__switch_theme(file_path)

    # 计算点阵个数
    def picture_dot_matrix(self):
        file_path = self.textBrowser_10.toPlainText()
        if os.path.exists(file_path):
            start_time = self.__time_start()

            total_count, black_count, color_count = self.__get_matrix(file_path)

            self.textBrowser_12.setText('{:.2f}w'.format(total_count / 10000))

            end_time = datetime.datetime.now()
            self.textBrowser_8.setText(end_time.strftime("%H:%M:%S"))

            self.__time_end(start_time)
        else:
            Sub_Ui_Form.__common_tips("图片不存在")

    # 计算覆盖率
    def calculate_matrix(self):
        file_path = self.textBrowser_10.toPlainText()
        if not os.path.exists(file_path):
            Sub_Ui_Form.__common_tips('文件不存在')
        else:
            start_time = self.__time_start()
            total_count, black_count, color_count = self.__get_matrix(file_path)

            total_coverage = (black_count + color_count) / total_count
            self.textBrowser_4.setText('{:.2f}%'.format(total_coverage * 100))

            black_coverage = black_count / total_count
            self.textBrowser_5.setText('{:.2f}%'.format(black_coverage * 100))

            color_coverage = color_count / total_count
            self.textBrowser_6.setText('{:.2f}%'.format(color_coverage * 100))

            end_time = datetime.datetime.now()
            self.textBrowser_8.setText(end_time.strftime("%H:%M:%S"))

            self.__time_end(start_time)

    # 计算价格
    def calculate_price(self):
        file_path = self.textBrowser_10.toPlainText()
        if not os.path.exists(file_path):
            Sub_Ui_Form.__common_tips("图片不存在")
        else:
            start_time = self.__time_start()

            total_amount = 0
            total_count, black_count, color_count = self.__get_matrix(file_path)
            # 未勾选彩印只按彩色价系算钱，需要算黑色价格
            if not self.checkBox_3.isChecked():
                black_base_price = float(self.textEdit.toPlainText())
                black_increment_price = float(self.textEdit_2.toPlainText())

                black_amount = pictureUtil.calculate_price(black_count / 100000.0, black_base_price,
                                                           black_increment_price)
                self.textBrowser.setText('{}元'.format(str(round(black_amount, 2))))
                total_amount += black_amount
            else:
                self.textBrowser.clear()
            # 计算彩色价格
            color_base_price = float(self.textEdit_3.toPlainText())
            color_increment_price = float(self.textEdit_4.toPlainText())
            color_amount = pictureUtil.calculate_price(color_count / 100000.0, color_base_price,
                                                       color_increment_price)
            total_amount += color_amount
            self.textBrowser_2.setText('{}元'.format(str(round(color_amount, 2))))
            self.textBrowser_3.setText('{}元'.format(str(round(total_amount, 2))))

            self.__time_end(start_time)

    # 保存配置文件
    def save_config(self):
        file_path = os.path.join(BASE_DIR, 'resource/config.json')
        config = configUtil.read_config_file(file_path)
        config['textEdit'] = self.textEdit.toPlainText()
        config['textEdit_2'] = self.textEdit_2.toPlainText()
        config['textEdit_3'] = self.textEdit_3.toPlainText()
        config['textEdit_4'] = self.textEdit_4.toPlainText()
        config['label_19'] = self.label_19.property('theme_path')
        configUtil.write_config_file(file_path, config)

    # 本地加载配置文件
    def load_config(self):
        file_path = os.path.join(BASE_DIR, 'resource/config.json')
        config = configUtil.read_config_file(file_path)
        if 'textEdit' in config:
            self.textEdit.setPlainText(config['textEdit'])
        if 'textEdit_2' in config:
            self.textEdit_2.setPlainText(config['textEdit_2'])
        if 'textEdit_3' in config:
            self.textEdit_3.setPlainText(config['textEdit_3'])
        if 'textEdit_4' in config:
            self.textEdit_4.setPlainText(config['textEdit_4'])
        if 'label_19' in config:
            self.__switch_theme(config['label_19'])

    # 前置清除工作
    def __pre_clean(self):
        self.textBrowser_4.clear()
        self.textBrowser_5.clear()
        self.textBrowser_6.clear()
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.textBrowser_12.clear()

        self.total_count = 0

    # 切换主题
    def __switch_theme(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(self.label_19.size(),
                               aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio,
                               transformMode=Qt.TransformationMode.SmoothTransformation)
        self.label_19.setProperty("theme_path", file_path)
        self.label_19.setPixmap(pixmap)

    # 图片地址展示
    def __display_image(self, file_path):
        pixmap = QPixmap(file_path)
        self.label_17.setPixmap(pixmap.scaled(301, 500, aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.__size_of_picture(pixmap)

    # 计算图片尺寸
    def __size_of_picture(self, pixmap):
        width = pixmap.width()
        height = pixmap.height()
        self.textBrowser_11.setText('长：{},宽：{}'.format(height, width))

    # 获取点阵
    def __get_matrix(self, file_path):
        if hasattr(self.textBrowser_4, 'total_count'):
            total_count = self.textBrowser_4.property('total_count')
            black_count = self.textBrowser_4.property('black_count')
            color_count = self.textBrowser_4.property('color_count')
        else:
            total_count, black_count, color_count = pictureUtil.calculate_dot_matrix(file_path)
        self.textBrowser_4.setProperty('total_count', total_count)
        self.textBrowser_5.setProperty('black_count', black_count)
        self.textBrowser_6.setProperty('color_count', color_count)
        return total_count, black_count, color_count

    # 公共提示
    @staticmethod
    def __common_tips(msg):
        if len(msg) < 1:
            msg = "错误操作"
        msg_box = QMessageBox()
        msg_box.setText(msg)
        # msg_box.setWindowTitle("提示")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        # 显示信息框
        msg_box.exec()

    def __time_start(self):
        start_time = datetime.datetime.now()
        self.textBrowser_7.setText(start_time.strftime("%H:%M:%S"))
        return start_time

    def __time_end(self, start_time):
        end_time = datetime.datetime.now()
        self.textBrowser_8.setText(end_time.strftime("%H:%M:%S"))

        time_difference = end_time - start_time
        dif = time_difference.microseconds / 1000
        self.textBrowser_9.setText("{}毫秒".format(round(dif, 3)))
