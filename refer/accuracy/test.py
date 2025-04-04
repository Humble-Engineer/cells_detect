import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error

import pandas as pd

def analyze_accuracy(true_counts, predicted_counts):
    """
    可视化分析算法计数精度
    参数：
        true_counts: 真实计数值列表
        predicted_counts: 算法预测值列表
    """
    # 计算评估指标
    r2 = r2_score(true_counts, predicted_counts)
    mae = mean_absolute_error(true_counts, predicted_counts)
    rmse = np.sqrt(np.mean((np.array(true_counts)
                             - np.array(predicted_counts))**2))
    
    # 创建画布
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # 散点图：真实值 vs 预测值
    axs[0,0].scatter(true_counts, predicted_counts, alpha=0.5)
    axs[0,0].plot([min(true_counts), max(true_counts)], 
                [min(true_counts), max(true_counts)], 'r--')
    axs[0,0].set_xlabel('True Count')
    axs[0,0].set_ylabel('Predicted Count')
    axs[0,0].set_title(f'R² = {r2:.2f}')
    
    # 误差分布直方图
    errors = np.array(predicted_counts) - np.array(true_counts)
    axs[0,1].hist(errors, bins=20, alpha=0.7)
    axs[0,1].axvline(0, color='r', linestyle='--')
    axs[0,1].set_xlabel('Prediction Error')
    axs[0,1].set_ylabel('Frequency')
    axs[0,1].set_title(f'MAE: {mae:.1f}, RMSE: {rmse:.1f}')
    
    # 残差图
    axs[1,0].scatter(true_counts, errors, alpha=0.5)
    axs[1,0].axhline(0, color='r', linestyle='--')
    axs[1,0].set_xlabel('True Count')
    axs[1,0].set_ylabel('Residuals')
    
    # 箱线图
    axs[1,1].boxplot([true_counts, predicted_counts], 
                   labels=['True', 'Predicted'])
    axs[1,1].set_ylabel('Cell Count')
    
    plt.tight_layout()
    plt.show()


# # 假设有以下测试数据
# true = [85, 120, 96, 143, 77, 132]
# predicted = [82, 115, 101, 138, 80, 128]


# 读取Excel文件（带异常处理）
try:
    df = pd.read_excel(r'F:\repos\Projects\cells_detect\refer\accuracy\data.xlsx', engine='openpyxl')
    
    # 检查必要列是否存在
    required_columns = ['True', 'Predicted']
    if not all(col in df.columns for col in required_columns):
        missing = [col for col in required_columns if col not in df.columns]
        raise ValueError(f"缺少必要列: {missing}")

    true = df['True'].tolist()
    predicted = df['Predicted'].tolist()

except FileNotFoundError:
    print("错误：文件未找到，请检查路径是否正确")
    exit()
except Exception as e:
    print(f"数据加载失败: {str(e)}")
    exit()

analyze_accuracy(true, predicted)