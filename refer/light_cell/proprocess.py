import cv2
import numpy as np
from matplotlib import pyplot as plt

def remove_background_morphological(image_path):
    """
    使用形态学操作消除背景噪声
    
    Args:
        image_path (str): 图像文件路径
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 创建结构元素（大尺寸用于背景估计）
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    
    # 使用形态学开运算估计背景
    background = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)
    
    # 从原图中减去背景
    result = cv2.subtract(blurred, background)
    
    # 调整对比度和亮度
    result = cv2.convertScaleAbs(result, alpha=1.5, beta=0)
    
    return blurred, background, result

def remove_background_top_hat(image_path):
    """
    使用顶帽变换消除背景噪声
    
    Args:
        image_path (str): 图像文件路径
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 创建结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    
    # 顶帽变换（原图减去开运算结果）
    tophat = cv2.morphologyEx(blurred, cv2.MORPH_TOPHAT, kernel)
    
    return blurred, tophat

def remove_background_rolling_ball(image_path, radius=20):
    """
    使用滚动球算法消除背景噪声（简化版）
    
    Args:
        image_path (str): 图像文件路径
        radius (int): 滚动球半径
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 创建球形结构元素
    kernel_size = 2 * radius + 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    
    # 使用形态学开运算估计背景
    background = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)
    
    # 从原图中减去背景
    result = cv2.subtract(blurred, background)
    
    # 调整对比度
    result = cv2.convertScaleAbs(result, alpha=2.0, beta=0)
    
    return blurred, background, result

def remove_background_frequency_domain(image_path):
    """
    使用频域滤波消除背景噪声
    
    Args:
        image_path (str): 图像文件路径
    """
    # 读取图像
    image = cv2.imread(image_path, 0)  # 直接读取为灰度图像
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    # 高斯模糊减少噪声
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    
    # 傅里叶变换
    f = np.fft.fft2(blurred)
    fshift = np.fft.fftshift(f)
    
    # 创建低通滤波器掩码（用于去除高频噪声）
    rows, cols = blurred.shape
    crow, ccol = rows // 2, cols // 2
    
    # 创建高通滤波器掩码（用于增强细胞边缘）
    mask = np.ones((rows, cols), np.uint8)
    r = 30  # 半径
    center = [crow, ccol]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= r*r
    mask[mask_area] = 0
    
    # 应用高通滤波器
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    # 转换为uint8
    result = np.uint8(img_back)
    
    return blurred, result

def remove_background_adaptive(image_path):
    """
    自适应背景消除方法
    
    Args:
        image_path (str): 图像文件路径
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 使用大尺寸中值滤波估计背景
    background = cv2.medianBlur(blurred, 51)
    
    # 从原图中减去背景
    result = cv2.subtract(blurred, background)
    
    # 调整对比度
    result = cv2.convertScaleAbs(result, alpha=2.0, beta=10)
    
    return blurred, background, result

def compare_background_removal_methods(image_path):
    """
    比较不同的背景消除方法
    
    Args:
        image_path (str): 图像文件路径
    """
    print("正在处理图像...")
    
    # 方法1: 形态学背景消除
    try:
        orig1, bg1, result1 = remove_background_morphological(image_path)
        print("形态学背景消除完成")
    except Exception as e:
        print(f"形态学背景消除失败: {e}")
        result1 = None
    
    # 方法2: 顶帽变换
    try:
        orig2, tophat_result = remove_background_top_hat(image_path)
        print("顶帽变换完成")
    except Exception as e:
        print(f"顶帽变换失败: {e}")
        tophat_result = None
    
    # 方法3: 滚动球算法
    try:
        orig3, bg3, result3 = remove_background_rolling_ball(image_path)
        print("滚动球算法完成")
    except Exception as e:
        print(f"滚动球算法失败: {e}")
        result3 = None
    
    # 方法4: 自适应背景消除
    try:
        orig4, bg4, result4 = remove_background_adaptive(image_path)
        print("自适应背景消除完成")
    except Exception as e:
        print(f"自适应背景消除失败: {e}")
        result4 = None
    
    # 显示结果
    plt.figure(figsize=(15, 12))
    
    # 原始图像
    plt.subplot(3, 4, 1)
    plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    # 形态学方法
    if result1 is not None:
        plt.subplot(3, 4, 2)
        plt.imshow(orig1, cmap='gray')
        plt.title('Morphological - Original')
        plt.axis('off')
        
        plt.subplot(3, 4, 3)
        plt.imshow(bg1, cmap='gray')
        plt.title('Morphological - Background')
        plt.axis('off')
        
        plt.subplot(3, 4, 4)
        plt.imshow(result1, cmap='gray')
        plt.title('Morphological - Result')
        plt.axis('off')
    
    # 顶帽变换
    if tophat_result is not None:
        plt.subplot(3, 4, 5)
        plt.imshow(orig2, cmap='gray')
        plt.title('Top-hat - Original')
        plt.axis('off')
        
        plt.subplot(3, 4, 6)
        plt.imshow(tophat_result, cmap='gray')
        plt.title('Top-hat - Result')
        plt.axis('off')
    
    # 滚动球算法
    if result3 is not None:
        plt.subplot(3, 4, 9)
        plt.imshow(orig3, cmap='gray')
        plt.title('Rolling Ball - Original')
        plt.axis('off')
        
        plt.subplot(3, 4, 10)
        plt.imshow(bg3, cmap='gray')
        plt.title('Rolling Ball - Background')
        plt.axis('off')
        
        plt.subplot(3, 4, 11)
        plt.imshow(result3, cmap='gray')
        plt.title('Rolling Ball - Result')
        plt.axis('off')
    
    # 自适应方法
    if result4 is not None:
        plt.subplot(3, 4, 12)
        plt.imshow(result4, cmap='gray')
        plt.title('Adaptive - Result')
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

def simple_background_removal(image_path, method='morphological'):
    """
    简单的背景消除函数
    
    Args:
        image_path (str): 图像文件路径
        method (str): 使用的方法 ('morphological', 'tophat', 'rollingball', 'adaptive')
    """
    if method == 'morphological':
        orig, _, result = remove_background_morphological(image_path)
    elif method == 'tophat':
        orig, result = remove_background_top_hat(image_path)
    elif method == 'rollingball':
        orig, _, result = remove_background_rolling_ball(image_path)
    elif method == 'adaptive':
        orig, _, result = remove_background_adaptive(image_path)
    else:
        raise ValueError("不支持的方法")
    
    # 显示结果
    cv2.imshow('Original', orig)
    cv2.imshow('Background Removed', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return result

# 使用示例
if __name__ == "__main__":
    # 替换为您的明场图像路径
    image_path = r"refer\light_cell\test1.jpg"
    
    print("比较不同的背景消除方法:")
    compare_background_removal_methods(image_path)
    
    print("\n使用单一方法处理:")
    # 可以选择以下任意一种方法:
    # simple_background_removal(image_path, 'morphological')
    # simple_background_removal(image_path, 'tophat')
    # simple_background_removal(image_path, 'rollingball')
    simple_background_removal(image_path, 'adaptive')