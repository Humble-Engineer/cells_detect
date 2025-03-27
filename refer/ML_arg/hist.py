import matplotlib.pyplot as plt

# 读取数据
with open(r'refer\ML_arg\img.txt', 'r') as file:
    data = [float(line.strip()) for line in file]

# 绘制直方图
plt.hist(data, bins=30, edgecolor='black')
plt.title('Data Distribution Histogram')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()