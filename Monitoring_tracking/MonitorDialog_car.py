from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog
from Monitoring_tracking.UIcar import Ui_Car
from Monitoring_tracking.Video_car import Video_car

class MonitorDialog_car(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Car()
        self.ui.setupUi(self)

        self.car_num = {'car': 0, 'truck': 0, 'bus': 0}
        self.car_id = self.ui.car_id.text()
        self.found = 0

        # 连接QLineEdit的textChanged信号到update_car_id方法
        self.ui.car_id.textChanged.connect(self.update_car_id)

        print('初始化视频处理线程')
        self.video = Video_car('data/vd2.mp4', self.car_id)
        print('绑定信号与槽')
        self.video.send.connect(self.showimg)
        print('启动视频处理线程')
        self.video.start()
        print('视频处理线程已启动')

    def update_car_id(self, text):
        """实时更新车牌号"""
        self.car_id = text
        print(f'车牌号更新为: {self.car_id}')
        self.video.update_car_id(self.car_id)

    def showimg(self, h, w, c, b, th_id, num, car_num, found):
        print(f"showimg函数被调用，参数：h={h}, w={w}, c={c}, th_id={th_id}, num={num}, car_num={car_num}")
        try:
            image = QImage(b, w, h, w * c, QImage.Format_BGR888)
            pix = QPixmap.fromImage(image)
            if th_id == 1:
                width = self.ui.video_car.width()
                height = self.ui.video_car.height()
                scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
                self.ui.video_car.setPixmap(scale_pix)
                print('更新UI元素')
                self.ui.sum_number.setText(str(num))
                self.ui.car_number.setText(str(car_num['car']))
                self.ui.bus_number.setText(str(car_num['bus']))
                self.ui.truck_number.setText(str(car_num['truck']))
                if found > 0:
                    self.ui.alarm.setStyleSheet("background-color: red;")
                print('UI元素更新完成')
        except Exception as e:
            print(f"showimg函数出错：{e}")

