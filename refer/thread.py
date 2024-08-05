import threading
from time import sleep

# 线程任务
def thread_worker():
    print('Working', end='', flush=True)
    while True:
        print('.', end='', flush=True)  # 使用flush=True确保立即输出
        sleep(1)

if __name__ == '__main__':
    print('Main thread')
    work_1 = threading.Thread(target=thread_worker, daemon=True)  # 设置为守护线程
    work_1.start()  # 启动线程
    input("Press Enter to exit.")  # 等待用户输入
