import cv2
import numpy as np
from matplotlib import pyplot as plt

def detect_contours_by_gradient(image_path, threshold=50, blur_kernel=(5, 5), morph_kernel=(3, 3)):
    """
    基于像素梯度变化的轮廓检测方法
    
    Args:
        image_path (str): 图像文件路径
        threshold (int): 梯度阈值，用于二值化梯度图像
        blur_kernel (tuple): 高斯模糊核大小
        morph_kernel (tuple): 形态学操作核大小
        
    Returns:
        tuple: 原始图像、梯度幅值图像、轮廓图像、所有轮廓列表
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, blur_kernel, 0)
    
    # 计算梯度 (使用Sobel算子)
    grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    
    # 计算梯度幅值
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    
    # 转换为8位图像
    gradient_magnitude = np.uint8(gradient_magnitude)
    
    # 应用阈值获取二值图像
    _, binary = cv2.threshold(gradient_magnitude, threshold, 255, cv2.THRESH_BINARY)
    
    # 形态学操作优化二值图像
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 在原始图像上绘制所有轮廓
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)  # 绿色表示所有检测到的轮廓
    
    return image, gradient_magnitude, contour_image, contours

def calculate_circularity(contour):
    """
    计算轮廓的圆形度
    
    圆形度 = 4π * 面积 / 周长²
    完美圆形的圆形度为1，其他形状的圆形度小于1
    
    Args:
        contour: 轮廓点集
        
    Returns:
        float: 圆形度值 (0-1之间)
    """
    area = cv2.contourArea(contour)
    if area == 0:
        return 0
    
    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0:
        return 0
    
    circularity = 4 * np.pi * area / (perimeter * perimeter)
    return circularity

def draw_contours_with_alpha(image, contours, color, thickness=2, alpha=0.15):
    """
    在图像上绘制指定透明度的轮廓
    
    Args:
        image: 输入图像
        contours: 轮廓列表
        color: 颜色 (B, G, R)
        thickness: 线条粗细
        alpha: 轮廓透明度 (0-1, 0为完全透明, 1为完全不透明)
        
    Returns:
        绘制了指定透明度轮廓的图像
    """
    # 创建一个与原图像相同大小的覆盖层
    overlay = image.copy()
    
    # 在覆盖层上绘制轮廓（使用纯色）
    cv2.drawContours(overlay, contours, -1, color, thickness)
    
    # 创建掩码来标识轮廓区域
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, contours, -1, 255, thickness)
    
    # 只对轮廓区域应用透明度混合
    for c in range(3):  # 对每个颜色通道处理
        image[:, :, c] = np.where(mask == 255, 
                                  (1 - alpha) * image[:, :, c] + alpha * overlay[:, :, c],
                                  image[:, :, c])
    
    return image

def detect_contours_by_gradient_colored_filtering(image_path, threshold=50, blur_kernel=(5, 5), 
                                                morph_kernel=(3, 3), top_percent=20, circularity_threshold=0.7,
                                                contour_alpha=0.15):
    """
    基于像素梯度变化的轮廓检测方法，使用不同颜色和透明度表示不同筛选阶段的轮廓
    
    颜色说明:
    - 绿色: 所有检测到的轮廓
    - 蓝色: 面积排名前top_percent%的轮廓
    - 红色: 面积排名前top_percent%且圆形度>=circularity_threshold的轮廓
    
    Args:
        image_path (str): 图像文件路径
        threshold (int): 梯度阈值，用于二值化梯度图像
        blur_kernel (tuple): 高斯模糊核大小
        morph_kernel (tuple): 形态学操作核大小
        top_percent (float): 保留的最大轮廓面积百分比 (例如20表示保留最大的20%)
        circularity_threshold (float): 圆形度阈值 (0-1之间，越接近1越像圆形)
        contour_alpha (float): 轮廓透明度 (0-1之间)
        
    Returns:
        tuple: 原始图像、梯度幅值图像、轮廓图像、筛选信息
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, blur_kernel, 0)
    
    # 计算梯度 (使用Sobel算子)
    grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    
    # 计算梯度幅值
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    
    # 转换为8位图像
    gradient_magnitude = np.uint8(gradient_magnitude)
    
    # 应用阈值获取二值图像
    _, binary = cv2.threshold(gradient_magnitude, threshold, 255, cv2.THRESH_BINARY)
    
    # 形态学操作优化二值图像
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, morph_kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 计算每个轮廓的面积和圆形度
    areas = [cv2.contourArea(cnt) for cnt in contours]
    circularities = [calculate_circularity(cnt) for cnt in contours]
    
    # 创建结果图像
    contour_image = image.copy()
    
    if len(areas) > 0:
        # 1. 绘制所有检测到的轮廓 (绿色) - 使用指定透明度
        draw_contours_with_alpha(contour_image, contours, (0, 255, 0), 2, contour_alpha)
        
        # 2. 计算要保留的轮廓数量
        num_to_keep = max(1, int(len(contours) * top_percent / 100))
        
        # 3. 根据面积大小对轮廓进行排序
        contour_area_circularity_triplets = list(zip(contours, areas, circularities))
        contour_area_circularity_triplets.sort(key=lambda x: x[1], reverse=True)  # 按面积降序排列
        
        # 4. 取前top_percent%的轮廓 (蓝色) - 使用指定透明度
        top_contours = contour_area_circularity_triplets[:num_to_keep]
        top_contours_only = [triplet[0] for triplet in top_contours]
        draw_contours_with_alpha(contour_image, top_contours_only, (255, 0, 0), 2, contour_alpha)
        
        # 5. 进一步筛选出圆形度满足要求的轮廓 (红色) - 使用指定透明度
        circular_contours = [triplet[0] for triplet in top_contours if triplet[2] >= circularity_threshold]
        draw_contours_with_alpha(contour_image, circular_contours, (0, 0, 255), 2, contour_alpha)
        
        # 输出统计信息
        print(f"原始轮廓数量: {len(contours)}")
        print(f"保留最大面积的 {top_percent}% 轮廓: {num_to_keep}个")
        print(f"其中圆形度 >= {circularity_threshold} 的轮廓数量: {len(circular_contours)}")
        print(f"平均圆形度: {np.mean(circularities):.3f}")
        
        # 准备返回的筛选信息
        filter_info = {
            'total_contours': len(contours),
            'top_percent': top_percent,
            'num_top_contours': num_to_keep,
            'circularity_threshold': circularity_threshold,
            'num_circular_contours': len(circular_contours),
            'mean_circularity': np.mean(circularities),
            'areas': areas,
            'circularities': circularities
        }
    else:
        print("未检测到轮廓")
        filter_info = {
            'total_contours': 0,
            'top_percent': top_percent,
            'num_top_contours': 0,
            'circularity_threshold': circularity_threshold,
            'num_circular_contours': 0,
            'mean_circularity': 0,
            'areas': [],
            'circularities': []
        }
    
    # 在图像上标注筛选条件信息
    if len(areas) > 0:
        info_text1 = f"Total: {len(contours)} (Green) | Top {top_percent}%: {num_to_keep} (Blue) | Circular: {len(circular_contours)} (Red)"
        cv2.putText(contour_image, info_text1, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        info_text2 = f"Circularity threshold: {circularity_threshold} | Contour Alpha: {contour_alpha}"
        cv2.putText(contour_image, info_text2, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return image, gradient_magnitude, contour_image, filter_info

def analyze_filtering_process(image_path, threshold=50, blur_kernel=(5, 5), morph_kernel=(3, 3), 
                            top_percent=20, circularity_threshold=0.7, contour_alpha=0.15):
    """
    分析筛选过程，显示不同阶段的轮廓
    
    Args:
        image_path (str): 图像文件路径
        threshold (int): 梯度阈值
        blur_kernel (tuple): 高斯模糊核大小
        morph_kernel (tuple): 形态学操作核大小
        top_percent (float): 面积排名百分比
        circularity_threshold (float): 圆形度阈值
        contour_alpha (float): 轮廓透明度
    """
    # 获取彩色筛选结果
    _, _, result_colored, filter_info = detect_contours_by_gradient_colored_filtering(
        image_path, threshold=threshold, blur_kernel=blur_kernel, morph_kernel=morph_kernel,
        top_percent=top_percent, circularity_threshold=circularity_threshold, contour_alpha=contour_alpha)
    
    # 显示结果
    plt.figure(figsize=(15, 5))
    
    # 原始图像
    orig = cv2.imread(image_path)
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    # 彩色筛选结果
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(result_colored, cv2.COLOR_BGR2RGB))
    plt.title('Colored Filtering Result (Low Alpha Contours)')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return result_colored, filter_info

def simple_gradient_contour_detection_colored(image_path, top_percent=20, circularity_threshold=0.7, contour_alpha=0.15):
    """
    简单的彩色轮廓检测函数，使用不同颜色和透明度表示不同筛选阶段
    
    Args:
        image_path (str): 图像文件路径
        top_percent (float): 保留的最大轮廓面积百分比
        circularity_threshold (float): 圆形度阈值
        contour_alpha (float): 轮廓透明度
    """
    orig, grad, result, filter_info = detect_contours_by_gradient_colored_filtering(
        image_path, top_percent=top_percent, circularity_threshold=circularity_threshold, contour_alpha=contour_alpha)
    
    # 显示结果
    cv2.imshow('Original', orig)
    cv2.imshow('Gradient', grad)
    cv2.imshow('Colored Filtering Result (Low Alpha)', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return result, filter_info

# 使用示例
if __name__ == "__main__":
    # 替换为您的明场图像路径
    image_path = r"refer\light_cell\light.png"

    # 设置顶部百分比阈值
    top_percent=20
    # 设置圆形度阈值，用于过滤形状接近圆形的轮廓
    circularity_threshold=0.5
    # 设置轮廓透明度，控制绘制轮廓时的透明程度
    contour_alpha=0.2
    
    # 分析筛选过程 (使用15%的轮廓透明度)
    print("使用彩色表示不同筛选阶段的轮廓 (轮廓部分透明表示):")
    result_image, filter_info = analyze_filtering_process(image_path, 
                                                          top_percent=top_percent, 
                                                          circularity_threshold=circularity_threshold, 
                                                          contour_alpha=contour_alpha)
    
    # 打印详细统计信息
    if filter_info['total_contours'] > 0:
        print(f"\n详细统计信息:")
        print(f"  总轮廓数: {filter_info['total_contours']}")
        print(f"  面积前{filter_info['top_percent']}%轮廓数: {filter_info['num_top_contours']}")
        print(f"  符合圆形度要求的轮廓数: {filter_info['num_circular_contours']}")
        print(f"  平均圆形度: {filter_info['mean_circularity']:.3f}")
        print(f"  筛选保留率: {filter_info['num_circular_contours']/filter_info['total_contours']*100:.1f}%")
    
    # 使用彩色筛选进行检测
    print("\n使用彩色筛选进行检测 (轮廓部分透明表示):")
    simple_gradient_contour_detection_colored(image_path, 
                                              top_percent=top_percent, 
                                              circularity_threshold=circularity_threshold, 
                                              contour_alpha=contour_alpha)