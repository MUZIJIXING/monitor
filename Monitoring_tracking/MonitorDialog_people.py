from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog
from Monitoring_tracking.UIpeople import Ui_People
from Monitoring_tracking.Video_people import Video_people


# 定义MonitorDialog类,继承QDialog
class MonitorDialog_people(QDialog):
    def __init__(self):
        super().__init__()
        # 创建Ui_Dialog类实例
        self.ui = Ui_People()
        # 调用setupUi方法设置用户界面
        self.ui.setupUi(self)
        # people_information初始化
        self.people_information = {}
        self.update_people_information()

        # 绑定QComboBox的currentIndexChanged信号到槽函数
        self.ui.gender.currentIndexChanged.connect(self.update_people_information)
        self.ui.age.currentIndexChanged.connect(self.update_people_information)
        self.ui.upper_wear.currentIndexChanged.connect(self.update_people_information)
        self.ui.lower_wear.currentIndexChanged.connect(self.update_people_information)

        self.video = Video_people('data/vd1.mp4', self.people_information)
        # 绑定信号与槽函数
        self.video.send.connect(self.showimg)
        # 启动视频处理线程
        self.video.start()

    # 定义一个名为update_people_information的槽函数，用于更新people_information字典
    def update_people_information(self):
        self.people_information['gender'] = self.ui.gender.currentText()
        self.people_information['age'] = self.ui.age.currentText()
        self.people_information['upper_wear'] = self.ui.upper_wear.currentText()
        self.people_information['lower_wear'] = self.ui.lower_wear.currentText()
        print("people_information 更新:", self.people_information)  # 调试信息

    # 定义一个名为showing的槽函数，用于显示图像
    def showimg(self, h, w, c, b, th_id, num, found):
        # 使用图像数据b创建一个QImage对象，指定宽度w，高度h和每行字节数w*c，图像格式为QImage.Format_BGR888
        image = QImage(b, w, h, w * c, QImage.Format_BGR888)
        # 将QImage图像转化为QPixmap图像
        pix = QPixmap.fromImage(image)
        if th_id == 1:
            # 自动缩放
            width = self.ui.video_people.width()
            height = self.ui.video_people.height()
            # 将QPixmap对象缩放到video1标签的宽度和高度，保持纵横比
            scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
            self.ui.video_people.setPixmap(scale_pix)
            # str(num) 类型转换
            self.ui.perplenumber.setText(str(num))
            if found>0:
                self.ui.alarm.setStyleSheet("background-color: red;")



