from PyQt5.QtCore import QThread, pyqtSignal
import cv2 as cv
from api.car import vehicle_detect

class Video_car(QThread):
    send = pyqtSignal(int, int, int, bytes, int, int, dict,int)

    def __init__(self, video_id, car_id):
        super().__init__()
        self.car_id = car_id
        self.th_id = 1
        self.dev = cv.VideoCapture(video_id)
        if not self.dev.isOpened():
            print(f"无法打开视频文件: {video_id}")
        self.running = True

    def run(self):
        while self.running and self.dev.isOpened():
            ret, frame = self.dev.read()
            if not ret:
                print("无法获取帧")
                break
            frame, num, car_num, found = vehicle_detect(frame, self.car_id)
            h, w, c = frame.shape
            img_bytes = frame.tobytes()
            self.send.emit(h, w, c, img_bytes, self.th_id, num, car_num, found)
            QThread.usleep(10000)

    def stop(self):
        self.running = False
        self.dev.release()
        self.quit()
        self.wait()

    def update_car_id(self, new_car_id):
        self.car_id = new_car_id
        print(f"Video_car 中的车牌号更新为: {self.car_id}")

