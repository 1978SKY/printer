import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog, QApplication

from ui.printer import Ui_Form
from subprinter import Sub_Ui_Form


class MyDialog(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()

        # 创建 Ui_Dialog 对象并设置 UI
        self.ui = Sub_Ui_Form()
        self.ui.setupUi(self)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "打印机覆盖率计算软件"))

        # 槽函数
        self.ui.pushButton_6.clicked.connect(self.ui.open_file_dialog)  # 选择图片
        self.ui.pushButton_4.clicked.connect(self.ui.picture_dot_matrix)  # 点阵计算
        self.ui.pushButton_2.clicked.connect(self.ui.calculate_matrix)  # 覆盖率计算
        self.ui.pushButton_3.clicked.connect(self.ui.calculate_price)  # 计算价格

        self.ui.pushButton_5.clicked.connect(self.ui.select_theme)

    # 在窗口显示时执行的槽函数
    def showEvent(self, event):
        self.ui.load_config()  # 执行加载操作
        event.accept()

    # 在窗口关闭时执行的槽函数
    def closeEvent(self, event):
        self.ui.save_config()  # 执行保存操作
        event.accept()


def main():
    app = QApplication(sys.argv)

    dialog = MyDialog()
    dialog.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
