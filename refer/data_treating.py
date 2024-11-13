import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.font_manager import FontProperties

# 设置字体为 SimHei 显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 真实值和两种方法的预测值
true_data  = [[47, 80, 164, 196, 331]
             ,[52, 74, 129, 188, 326]
             ,[46, 75, 132, 178, 386]
             ,[49, 68, 138, 195, 370]
             ,[53, 62, 142, 177, 393]]

old_method = [[45, 76, 153, 171, 290] 
             ,[50, 73, 123, 171, 297]
             ,[46, 73, 123, 161, 331]
             ,[49, 60, 132, 180, 317]
             ,[52, 60, 131, 167, 328]]

new_method = [[47, 81, 163, 194, 329] 
             ,[52, 75, 128, 188, 325]
             ,[47, 75, 132, 179, 381]
             ,[49, 67, 138, 193, 366]
             ,[53, 62, 142, 178, 388]]

# 使用 zip 函数逐元素地组合向量，然后计算每个维度的总和
true_data_sum = [sum(values) for values in zip(*true_data)]
old_method_sum = [sum(values) for values in zip(*old_method)]
new_method_sum = [sum(values) for values in zip(*new_method)]

x_labels = ['15.5', '28.0', '44.4', '83.5', '110.6']

# 计算相对误差
def calculate_relative_error(true_values, predicted_values):
    return [abs(t - p) / t * 100 for t, p in zip(true_values, predicted_values)]

# 计算平均相对误差（MRE）
def calculate_mre(relative_errors):
    return sum(relative_errors) / len(relative_errors)

# 计算所有维度的相对误差
new_method_relative_errors = calculate_relative_error(true_data_sum, new_method_sum)
old_method_relative_errors = calculate_relative_error(true_data_sum, old_method_sum)

# 计算所有维度的MRE
new_method_mre = calculate_mre(new_method_relative_errors)
old_method_mre = calculate_mre(old_method_relative_errors)

# 打印MRE
print(f"New Method MRE: {new_method_mre:.2f}%")
print(f"Old Method MRE: {old_method_mre:.2f}%")

# 绘制相对误差图
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制新方法的相对误差
ax.plot(new_method_relative_errors, label='New Method Relative Error', marker='o', linestyle='-')
for j, error in enumerate(new_method_relative_errors):
    ax.text(j, error, f'{error:.2f}%', ha='center', va='bottom')

# 绘制旧方法的相对误差
ax.plot(old_method_relative_errors, label='Old Method Relative Error', marker='x', linestyle='--')
for j, error in enumerate(old_method_relative_errors):
    ax.text(j, error, f'{error:.2f}%', ha='center', va='bottom')

# 设置纵坐标为百分比
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0f}%'))

# 设置横坐标标签
plt.xticks(range(len(x_labels)), x_labels)
plt.xlabel('浓度梯度')
plt.ylabel('相对误差 (%)')
plt.title('相对误差对比')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()