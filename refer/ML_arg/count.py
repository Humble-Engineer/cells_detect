import math
import matplotlib.pyplot as plt

def find_approximate_gcd(numbers):

    max_number = max(numbers)
    min_number = min(numbers)
    min_distance = float('inf')
    best_divisor = 0
    
    # 新增记录数据容器
    divisors = []
    distances = []

    for divisor in range(int(max_number * 2), int(min_number), -1):
        divisor = divisor / 2  # 转换为0.5步长
        total_distance = 0

        for num in numbers:
            quotient = num / divisor
            closest_int = round(quotient)
            distance = abs(quotient - closest_int)
            total_distance += distance

        # 记录每个除数的数据
        divisors.append(divisor)
        distances.append(total_distance)

        if total_distance < min_distance:
            min_distance = total_distance
            best_divisor = divisor

    return best_divisor, divisors, distances  # 修改返回结构


with open(r'.\refer\ML_arg\img.txt', 
         'r', 
         encoding='utf-8') as f:  # 关键修改点
    numbers = [float(line.strip()) for line in f]

# 修改函数调用
best_gcd, all_divisors, all_distances = find_approximate_gcd(numbers)

# 绘制误差曲线（在原有代码基础上添加）
plt.figure(figsize=(12, 7))  # 稍微加大画布尺寸
plt.plot(all_divisors, all_distances, 'b-', linewidth=1, alpha=0.7)
plt.title('Total Distance vs Divisor')
plt.xlabel('Divisor')
plt.ylabel('Total Distance')
plt.grid(True, linestyle='--', alpha=0.5)

# 新增标注代码
minima_indices = []
for i in range(1, len(all_distances)-1):
    if all_distances[i] < all_distances[i-1] and all_distances[i] < all_distances[i+1]:
        minima_indices.append(i)

minima_points = [(all_divisors[i], all_distances[i]) for i in minima_indices]

# 绘制极小值点
plt.scatter(*zip(*minima_points), 
            color='r', 
            s=60, 
            edgecolor='black',
            zorder=5,
            label=f'Local Minima ({len(minima_points)} found)')

# 智能标注（防止重叠）
for idx, (x, y) in enumerate(minima_points):
    offset = (10 if idx % 2 == 0 else -15)  # 交替上下偏移
    plt.annotate(f'({x:.1f}, {y:.1f})',
                 (x, y),
                 textcoords="offset points",
                 xytext=(0, offset),
                 ha='center',
                 va='bottom' if offset > 0 else 'top',
                 fontsize=8,
                 arrowprops=dict(arrowstyle="->", 
                               connectionstyle="arc3",
                               color='orange'))

plt.legend()
plt.tight_layout()  # 自动调整布局
plt.show()



