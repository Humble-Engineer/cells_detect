import os
import datetime

class DataHandler:

    def __init__(self, main_window=None):
        """
        初始化 DataHandler 实例
        :param main_window: 主窗口对象，可选参数，默认为 None
        """
        self.main_window = main_window
        self.data_dir = 'data'
        self.ensure_data_directory()
        self.generate_filename()
    
    def ensure_data_directory(self):
        """
        确保 data 子文件夹存在
        """
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def generate_filename(self):
        """
        生成带有当前日期的文件名
        :return: 带有当前日期的文件名
        """
        # 获取当前日期和时间
        now = datetime.datetime.now()
        # 将日期格式化为 "年月日时分秒" 格式
        date_str = now.strftime("%Y%m%d%H%M%S")
        # 拼接文件名
        filename = f"{date_str}.txt"
        # 定义文件的完整路径
        self.file_path = os.path.join(self.data_dir, filename)
    
    def write_to_file(self, content, mode='w'):
        """
        在当前目录下的 data 子文件夹中创建文件并写入内容
        :param content: 要写入的内容
        :param mode: 文件打开模式，默认为 'w'（写入模式）
        """
        # 打开文件，如果文件不存在则创建
        with open(self.file_path, mode, encoding='utf-8') as file:
            # 写入内容
            file.write(content)
        
        # print(f"文件已创建并写入内容：{self.file_path}")

if __name__ == '__main__':
    
    # 创建 DataHandler 实例
    handler = DataHandler()
    # 使用实例方法生成文件名并写入内容
    handler.write_to_file('hello world!\n', mode='a')