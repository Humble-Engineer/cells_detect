import cv2  
  
# 创建一个 VideoCapture 对象，参数为 0 表示读取默认摄像头  
cap = cv2.VideoCapture(0)  
  
# 检查摄像头是否成功打开  
if not cap.isOpened():  
    print("Error: 无法打开摄像头")  
    exit()  
  
while True:  
    # 逐帧读取摄像头  
    ret, frame = cap.read()  
  
    # 检查是否成功读取到帧  
    
    if not ret:  
        print("Error: 无法接收帧（可能摄像头已断开）")  
        break  
  
    # 显示帧  
    cv2.imshow('Camera Feed', frame)  
  
    # 如果按下 'q' 键，退出循环  
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break  
  
# 释放摄像头并关闭所有 OpenCV 窗口  
cap.release()  
cv2.destroyAllWindows()