import sys
from Monitoring_tracking.Monitoring_trackingAPP import MonitorApp
if __name__ == '__main__':
    # 创建类的实例
    app = MonitorApp()
    # app.exec()执行某些操作并返回状态码
    # sys.exit()用于退出python程序，将app.exec()的返回值作为退出状态码
    sys.exit(app.exec())