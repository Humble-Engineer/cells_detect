import os

# 导入参数输入模块
from modules import parameter
# 导入图像处理模块
from modules import process

if __name__ == "__main__":

    # 如果输入的路径图像不存在
    if (os.path.exists(parameter.args.path) == 0):
        # 终端报错提示
        print(f"检测文件{parameter.args.path}不存在!")
        # 采用默认图片路径
        parameter.args.path='./samples/img(5).png'

    # 检测输入路径的图像
    process.detect(parameter.args.path)
    
    






