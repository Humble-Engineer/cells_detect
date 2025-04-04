import math
import matplotlib.pyplot as plt

def find_approximate_gcd(numbers):
    max_number = max(numbers)
    min_number = min(numbers)
    min_distance = float('inf')
    best_divisor = 0
    
    divisors = []
    distances = []

    for divisor in range(int(max_number * 2), int(min_number), -1):
        divisor = divisor / 2  # 0.5步长扫描
        total_distance = 0

        for num in numbers:
            quotient = num / divisor
            closest_int = round(quotient)
            distance = abs(quotient - closest_int)
            total_distance += distance

        divisors.append(divisor)
        distances.append(total_distance)

        if total_distance < min_distance:
            min_distance = total_distance
            best_divisor = divisor

    return best_divisor, divisors, distances

# 数据读取
with open(r'.\refer\ML_arg\real_img.txt', 'r', encoding='utf-8') as f:
    numbers = [float(line.strip()) for line in f]

# 计算最佳除数
best_gcd, all_divisors, all_distances = find_approximate_gcd(numbers)

# 可视化设置
plt.figure(figsize=(10, 6), dpi=300)

# 兼容性样式设置
try:
    # 尝试新版样式名称
    plt.style.use('seaborn-v0_8-whitegrid')
except OSError:
    try:
        # 回退到旧版seaborn样式
        plt.style.use('seaborn')
    except OSError:
        # 完全兼容模式
        plt.grid(True, linestyle='--', alpha=0.6, color='#e0e0e0')

# 主曲线
ax = plt.gca()
main_line = plt.plot(all_divisors, all_distances,
                    color='#2c5c8a',
                    linewidth=2.5,
                    alpha=0.9)
# 极值点检测
minima_indices = []
for i in range(1, len(all_distances)-1):
    if (all_distances[i] < all_distances[i-1] 
        and all_distances[i] < all_distances[i+1]):
        minima_indices.append(i)
        
minima_points = [(all_divisors[i], all_distances[i]) 
                    for i in minima_indices]

# 极值点标注
scatter = plt.scatter(*zip(*minima_points),
                     color='#ff6361',
                     s=80,
                     edgecolor='#444444',
                     linewidth=1.5,
                     zorder=5,
                     label=f'Local Minima ({len(minima_points)})')

# 坐标轴美化
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
[spine.set_color('#4d4d4d') for spine in ax.spines.values()]

# 标签设置
plt.title('Divisor Optimization Analysis', fontsize=18, 
         fontname='Times New Roman', pad=20)
plt.xlabel('Divisor', fontsize=14, 
          fontname='Times New Roman',labelpad=10)
plt.ylabel('Normalized Distance', fontsize=14, 
          fontname='Times New Roman', labelpad=10)

# 刻度设置
plt.tick_params(axis='both', which='major', labelsize=12,
               length=6, width=1.5)

# 最优解标注
plt.annotate(f'Optimal Divisor: {best_gcd:.1f}',
            xy=(best_gcd, min(all_distances)),
            xytext=(best_gcd+5, min(all_distances)+0.5),
            arrowprops=dict(arrowstyle='->', 
                          connectionstyle='arc3',
                          color='#58508d'),
            fontsize=12,
            fontname='Times New Roman')

# 背景设置
ax.set_facecolor('#f0f0f0')

# 兼容性网格设置（如果样式加载失败）
if not plt.style.available:  # 如果没有任何样式被加载
    ax.grid(True, 
           linestyle='--', 
           alpha=0.6, 
           color='gray',
           which='both')

# 保存输出
plt.tight_layout()
plt.savefig('optimized_plot.pdf', format='pdf', bbox_inches='tight')
plt.savefig('optimized_plot.png', dpi=600, bbox_inches='tight')
plt.show()