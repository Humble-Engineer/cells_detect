import os
import datetime

def generate_filename(base_name):
    """
    生成带有当前日期的文件名
    :param base_name: 文件名的基础部分
    :return: 带有当前日期的文件名
    """
    # 获取当前日期和时间
    now = datetime.datetime.now()
    # 将日期格式化为 "年月日" 格式
    date_str = now.strftime("%Y%m%d%H%M%S")
    # 拼接文件名
    return f"{base_name}_{date_str}.txt"

def write_to_file(filename, content, mode='w'):
    """
    在当前目录下创建文件并写入内容
    :param filename: 文件名
    :param content: 要写入的内容
    :param mode: 文件打开模式，默认为 'w'（写入模式）
    """
    # 获取当前工作目录
    current_dir = os.getcwd()
    # 定义文件的完整路径
    file_path = os.path.join(current_dir, filename)
    
    # 打开文件，如果文件不存在则创建
    with open(file_path, mode, encoding='utf-8') as file:
        # 写入内容
        file.write(content)
    
    print(f"文件已创建并写入内容：{file_path}")

# 调用函数，指定文件名基础部分和内容
file_name = generate_filename('data')

write_to_file(file_name, 'hello world!\n', mode='a')