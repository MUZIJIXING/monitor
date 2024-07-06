from PyQt5 import QtWidgets, QtGui, QtCore
from Monitoring_tracking.MonitorDialog_people import MonitorDialog_people
from Monitoring_tracking.MonitorDialog_car import MonitorDialog_car
from Monitoring_tracking.mainframe_button import Ui_Dialog
import data.resources


# 继承QMainWindow类
class MainDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建QLabel对象，将其设置为主窗口的子部件，中央部件
        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)
        # 将在资源文件的背景图片并创建对象QPixmap
        self.pixmap = QtGui.QPixmap(":/bg1.png")
        # 设置QLabel的尺寸为主窗口的宽度和高度
        self.label.resize(self.width(), self.height())
        # 设置QLabel自动缩放其内容以适应尺寸变化
        self.label.setScaledContents(True)
        # 将背景图片设置为QLabel的内容，保持纵横比并使用平滑转换
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))
        # 监听窗口大小变化事件
        self.resizeEvent = self.on_resize
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


    # 处理窗口大小变化的事件
    def on_resize(self, event):
        self.label.resize(self.width(), self.height())
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))
    def goin_people(self):
        self.MonitorDialog_people = MonitorDialog_people()
        self.MonitorDialog_people.show()
        self.close()

    def goin_car(self):
        self.MonitorDialog_car = MonitorDialog_car()
        self.MonitorDialog_car.show()
        self.close()

