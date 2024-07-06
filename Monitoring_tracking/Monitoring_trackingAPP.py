from PyQt5.QtWidgets import QApplication
from Monitoring_tracking.mainframe import MainDialog
import sys

# 类
class MonitorApp(QApplication):
    def __init__(self):
        super(MonitorApp, self).__init__(sys.argv)
        self.dialog = MainDialog()
        self.dialog.show()
