
import cv2 as cv
import numpy as np
import time

def main(address):
    
    # 预设一个窗口
    cv.namedWindow("Threshold Setting")

    # 空函数
    def nothing(x):
        pass
    
    # 预设滑块
    cv.createTrackbar("H_min", "Threshold Setting", 30, 255, nothing)
    cv.createTrackbar("H_max", "Threshold Setting", 60, 255, nothing)
    cv.createTrackbar("S_min", "Threshold Setting", 50, 255, nothing)
    cv.createTrackbar("S_max", "Threshold Setting", 255, 255, nothing)
    cv.createTrackbar("V_min", "Threshold Setting", 50, 255, nothing)
    cv.createTrackbar("V_max", "Threshold Setting", 255, 255, nothing)
    
    while True:

        # 读取图片
        img = cv.imread(address)

        # 调整图像，防畸变
        img = cv.resize(img, (0,0), fx=0.2, fy=0.2)

        # 将RGB模型转换为HSV模型
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # 生成滑块
        H_min = cv.getTrackbarPos('H_min', 'Threshold Setting')
        H_max = cv.getTrackbarPos('H_max', 'Threshold Setting')
        S_min = cv.getTrackbarPos('S_min', 'Threshold Setting')
        S_max = cv.getTrackbarPos('S_max', 'Threshold Setting')
        V_min = cv.getTrackbarPos('V_min', 'Threshold Setting')
        V_max = cv.getTrackbarPos('V_max', 'Threshold Setting')

        # 转换为numpy数组
        lower_hsv1 = np.array([H_min, S_min, V_min])
        upper_hsv1 = np.array([H_max, S_max, V_max])

        # 基于阈值生成二值图
        Mask = cv.inRange(hsv, lowerb=lower_hsv1, upperb=upper_hsv1)  # hsv 掩码
        ret, mask = cv.threshold(Mask, 40, 255, cv.THRESH_BINARY)  # 二值化处理

        # 图像学腐蚀(terations,程度)
        mask = cv.erode(mask, None, iterations=2)

        # 图像学膨胀(terations,程度)
        mask = cv.dilate(mask, None, iterations=1)

        # 高斯模糊
        # mask = cv.GaussianBlur(mask, (3, 3), 0)

        # 获取图像结构化元素（形态学处理前置操作）
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))

        # 图像闭操作
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

        # 获取二值化圖轮廓点集(坐标)
        contours1, heriachy1 = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  

        # 在原图上绘制轮廓
        cv.drawContours(img, contours1, -1, (0, 0, 255), 2)

        # 显示图像
        cv.imshow("Mask", mask)
        cv.imshow("Image", img)

        # 等待键盘指令
        key = cv.waitKey(1)

        # 退出程序
        if(key == 27):
            cv.destroyAllWindows()
            break

        # 输出参数
        elif key & 0xFF == ord('v'):
            print ([H_min,H_max,S_min,S_max,V_min,V_max])   
            #print(contours1)         

        # C键截图保存
        elif key & 0xFF == ord('c'):
            
            # 获取当前时间
            t = time.localtime()

            # 生成当前日期字符串
            Capture_Day = str(t.tm_year)+"."+str(t.tm_mon)+"."+str(t.tm_mday)
            # 生成当前时间字符串
            Capture_Time = str(t.tm_hour)+"."+str(t.tm_min)+"."+str(t.tm_sec)

            # 设置截取图片名称
            Picture_Name = Capture_Day+"_"+Capture_Time

            # 设置截取图片所在路径
            Capture_Path = "./results/"+Picture_Name+".jpg"
            
            # 保存截图
            cv.imwrite(Capture_Path, img)

            print("截图已保存:%s" % Capture_Path)

    # 摧毁所有窗口
    cv.destroyAllWindows()

adress = "./samples/img(1).png"
main(adress)




