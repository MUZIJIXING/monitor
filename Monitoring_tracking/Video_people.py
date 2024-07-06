# 在独立的线程中处理视频流，并通过信号槽机制将视频帧和检测到的车辆数据传递给主线程
from PyQt5.QtCore import QThread
import cv2 as cv
from PyQt5.QtCore import pyqtSignal
from api.people import people_detect


class Video_people(QThread):
    # 使用信号与槽槽函数向外传递数据
    #    发送者   Video
    #    信号类型  自定义信号类型(参数信号所能传递的数据)
    #    接收者   （线程所在的Dialog）
    #    槽函数   （接收者类：功能方法）

    # 定义一个名为send的自定义信号，该信号可以传递6个参数：高度，宽度，通道数，图像字节数据，线程ID，人数量，特殊人员数量
    send = pyqtSignal(int, int, int, bytes,int,int,int) #emit
    def __init__(self,video_id,people_information):
        super().__init__()
        # 准备工作
        self.people_information = people_information
        self.th_id = 1
        # 从指定的视频文件中捕获视频帧
        self.dev = cv.VideoCapture(video_id)
        # 打开视频文件
        self.dev.open(video_id)

    def run(self):
        # 耗时操作
        # 重写QThread的run方法,这是线程执行的内容
        while True:
            # 从视频捕获设备读取一帧图像,ret表示是否成功读取,frame是读取的图像
            ret, frame = self.dev.read()
            # 调用vehicle_detect函数检测车辆,并返回标记后的图像和检测到的车辆数量
            frame, num, found = people_detect(frame,self.people_information)
            if not ret:
                print('no')
            # car
            h, w, c = frame.shape
            # 将图像转换为字节数据
            img_bytes = frame.tobytes()
            # send信号发送图像的高度、宽度、通道数、字节数据、线程ID、车流数量
            self.send.emit(h, w, c, img_bytes,self.th_id,num,found)
            # 休眠10毫秒，usleep以微秒为单位
            QThread.usleep(10000)



