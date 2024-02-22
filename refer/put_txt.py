import cv2 as cv
import numpy as np

# 创建一个空白图像
img = np.zeros((300, 500, 3), dtype=np.uint8)

# 设置要绘制的文字和字体属性
text = "Hello, OpenCV!"
font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 1.5
font_thickness = 2
font_color = (255, 255, 255)  # 白色

# 获取文字的大小信息
text_size = cv.getTextSize(text, font, font_scale, font_thickness)[0]

# 计算文字的位置（居中放置）
text_x = (img.shape[1] - text_size[0]) // 2
text_y = (img.shape[0] + text_size[1]) // 2

# 在图像上绘制文字
cv.putText(img, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

# 显示图像
cv.imshow("Image with Text", img)
cv.waitKey(0)
cv.destroyAllWindows()
