# 命令行输入参数测试

# filename.py
import sys

# 获取命令行参数
args = sys.argv

# 打印整个参数列表
print("命令行参数:", args)

# 打印脚本名称
print("脚本名称:", args[0])

# 打印传递给脚本的其他参数
if len(args) > 1:
    print("其他参数:", args[1])
