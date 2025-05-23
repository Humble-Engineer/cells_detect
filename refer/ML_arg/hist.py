import matplotlib.pyplot as plt

# 必须先设置样式再绘图
try:
    plt.style.use('seaborn-v0_8')  # 新版兼容写法
except:
    plt.style.use('classic')  # 回退到经典样式

# 读取数据
with open(r'refer\ML_arg\low_power_lens.txt', 'r') as file:
    data = [float(line.strip()) for line in file]

# 绘制直方图
plt.hist(data, bins=30, edgecolor='black')
plt.title('Data Distribution Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(False)

# 坐标轴美化
ax = plt.gca()
ax.set_facecolor('#f5f5f5')  # 设置浅灰色背景
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()