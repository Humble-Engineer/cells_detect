import argparse

# 创建ArgumentParser对象
parser = argparse.ArgumentParser(description='荧光图像检测脚本')
# 添加参数，并指定默认值
parser.add_argument('--path', default='./samples/img(1).png', help='需要检测的图片路径')
# 解析命令行参数
args = parser.parse_args()

if __name__ == "__main__":
    print(parser)
