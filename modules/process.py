import cv2 as cv
import numpy as np
import time

def trackbar_init():

     # 预设一个窗口
    cv.namedWindow("Threshold Setting",0)

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

def hsv_update():

    # 生成滑块
    H_min = cv.getTrackbarPos('H_min', 'Threshold Setting')
    H_max = cv.getTrackbarPos('H_max', 'Threshold Setting')
    S_min = cv.getTrackbarPos('S_min', 'Threshold Setting')
    S_max = cv.getTrackbarPos('S_max', 'Threshold Setting')
    V_min = cv.getTrackbarPos('V_min', 'Threshold Setting')
    V_max = cv.getTrackbarPos('V_max', 'Threshold Setting')

    # 转换为numpy数组
    lower_hsv = np.array([H_min, S_min, V_min])
    upper_hsv = np.array([H_max, S_max, V_max])

    return lower_hsv,upper_hsv

def draw_contours(img,contours):

    # 查看轮廓个数
    num_contours = len(contours)

    # 设置要绘制的文字和字体属性
    text = "Cells (clusters) found:" + str(num_contours)
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 1
    font_color = (255, 255, 255)  # 白色

    # 计算文字的位置
    text_x = int(img.shape[0]*0.1)
    text_y = int(img.shape[0]*0.95)

    # 在图像上绘制文字
    cv.putText(img, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

    # 在原图上绘制轮廓
    for index in range (0,num_contours):

        # 单独绘制轮廓
        cv.drawContours(img, contours, index, (255, 0, 0), thickness=1)

        # 假设 contours 是你通过 cv.findContours 得到的轮廓列表
        # 选择要获取最小外接圆的轮廓，例如第一个轮廓
        selected_contour = contours[index]

        # 找到最小外接圆
        center, radius = cv.minEnclosingCircle(selected_contour)

        # 将浮点坐标转换为整数
        center = tuple(map(int, center))
        radius = int(radius)

        # 在图像上绘制最小外接圆
        # cv.circle(img, center, radius, (255, 255, 255), 2)

        # 设置要绘制的文字和字体属性
        text = str(index+1)
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        font_color = (0, 0, 255)  # 白色

        # 计算文字的位置
        text_x = (center[0] - radius)
        text_y = (center[1] - radius) 

        # 在图像上绘制文字
        cv.putText(img, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

def waitkey():
    pass

# 检测主程序
def detect(address):

    # 滑块初始化
    trackbar_init()
    
    while True:

        # 更新滑块HSV设置
        lower_hsv, upper_hsv = hsv_update()

        # 读取图片
        img = cv.imread(address)
        # 调整图像，防畸变
        img = cv.resize(img, (0,0), fx=0.3, fy=0.3)
        # 将RGB模型转换为HSV模型
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # 基于阈值生成二值图
        Mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)  # hsv 掩码
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
        contours, heriachy1 = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        # 绘制找到的轮廓
        draw_contours(img,contours)
        
        # 显示图像
        # cv.imshow("Mask", mask)
        cv.imshow("Image", img)

        # 等待键盘指令
        key = cv.waitKey(1)
        # 退出程序
        if(key == 27):
            # 摧毁所有窗口
            cv.destroyAllWindows()
            break

        # 输出参数
        elif key & 0xFF == ord('v'):
            print (lower_hsv, upper_hsv)          

        # s键保存结果
        elif key & 0xFF == ord('s'):
            
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



if __name__ == "__main__":
    # 尝试检测一下
    detect("./samples/img(10).png")