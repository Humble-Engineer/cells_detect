# 打包：pyinstaller -F camera.py

import cv2
import time

# 提示用户输入摄像头编号
camera_index = input("请输入摄像头编号（通常0为内置摄像头，1为外接摄像头）: ")

try:
    # 将输入转换为整数
    camera_index = int(camera_index)
except ValueError:
    print("错误：输入无效，请输入一个数字。")
    exit()

# 根据用户输入创建 VideoCapture 对象
cap = cv2.VideoCapture(camera_index)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: 无法打开摄像头")
    exit()

# 初始化帧计数器、前一帧的时间戳和 FPS 变量
frame_count = 0
start_time = time.time()
fps = 0  # Initialize fps here

while True:
    # 逐帧读取摄像头
    ret, frame = cap.read()
    
    # 检查是否成功读取到帧
    if not ret:
        print("Error: 无法接收帧（可能摄像头已断开）")
        break
    
    # 帧计数加1
    frame_count += 1
    
    # 计算已经过去的时间
    elapsed_time = time.time() - start_time
    
    # 如果已经过去了一秒，重新开始计时并计算FPS
    if elapsed_time >= 1.0:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()
    
    # 在左上角显示FPS
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # 显示帧
    cv2.imshow('Camera Feed', frame)
    
    # 如果按下 'ESC' 键，退出循环
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 释放摄像头并关闭所有 OpenCV 窗口
cap.release()
cv2.destroyAllWindows()