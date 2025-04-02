

import cv2 as cv
import threading

class Camera:

    def __init__(self, main_window):

        self.main_window = main_window

        self.thread_running = False  # 控制线程是否运行的标志
        self.worker_thread = None  # 存储线程实例

        # 首先尝试使用内置摄像头
        self.cap = cv.VideoCapture(0)

        # 检查内置摄像头是否成功打开
        if not self.cap.isOpened():
            # 如果内置摄像头失败，则尝试外接摄像头
            self.cap = cv.VideoCapture(1)
            if not self.cap.isOpened():
                print("未检测到任何摄像头!")
                return
            else:   
                print("成功读取外接摄像头...")
        else :
            print("成功读取内置摄像头...")

    def toggle_thread(self):
        if not self.thread_running:
            self.start_thread()
        else:
            self.stop_thread()
    
    def start_thread(self):
        self.thread_running = True
        self.main_window.ui.capture_button.setText("stop capture")
        self.worker_thread = threading.Thread(target=self.thread_worker, daemon=True)
        self.worker_thread.start()

    def stop_thread(self):
        self.thread_running = False
        self.main_window.ui.capture_button.setText("start capture")
        if self.worker_thread is not None:
            self.worker_thread.join()
        self.worker_thread = None

    def thread_worker(self):

        while self.thread_running:

            ret, self.main_window.origin_img = self.cap.read()
            if not ret:
                print("无法获取帧，请检查摄像头是否正常工作。")
                break
            else:
                self.main_window.algorithm.count()
                pass
