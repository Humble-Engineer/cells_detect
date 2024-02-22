# shell输入样式python filename.py --arg2 value2 --arg1 value1 --arg3 value3

# filename.py
import argparse

# 创建ArgumentParser对象
parser = argparse.ArgumentParser(description='描述你的脚本')

# 添加参数，并指定默认值
parser.add_argument('--arg1', default='default_value1', help='参数1的帮助信息')
parser.add_argument('--arg2', default='default_value2', help='参数2的帮助信息')
parser.add_argument('--arg3', default='default_value3', help='参数3的帮助信息')

# 解析命令行参数
args = parser.parse_args()

# 打印参数的值
print('参数1:', args.arg1)
print('参数2:', args.arg2)
print('参数3:', args.arg3)