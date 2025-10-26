import cv2
import numpy as np

def detect_cells_watershed(image_path):
    """
    使用分水岭算法检测明场图像中的细胞（小黑点）
    
    Args:
        image_path (str): 图像文件路径
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 使用高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 使用阈值分割，将暗色细胞从明亮背景中分离出来
    # 使用自适应阈值可以更好地处理不均匀照明
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # 形态学操作，去除噪声并连接相邻细胞
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # 创建确定的前景区域（只有足够黑的区域）
    # 通过降低阈值获取确定的前景
    _, sure_fg = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 距离变换获取确定的背景区域
    dist_transform = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    _, sure_bg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    
    # 转换sure_bg为uint8类型
    sure_bg = np.uint8(sure_bg)
    
    # 未知区域
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # 标记连通分量
    _, markers = cv2.connectedComponents(sure_fg)
    
    # 为所有标记加1，确保背景不是0
    markers = markers + 1
    
    # 标记未知区域为0
    markers[unknown == 255] = 0
    
    # 应用分水岭算法
    markers = cv2.watershed(image, markers)
    
    # 创建结果图像
    result_image = image.copy()
    result_image[markers == -1] = [0, 0, 255]  # 用红色标记分水岭边界
    
    # 计算细胞数量
    cell_count = len(np.unique(markers)) - 2  # 减去背景和边界标记
    
    # 在原图上绘制检测到的细胞
    cell_count_filtered = 0
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # 计算轮廓面积，过滤掉太小或太大的区域
        area = cv2.contourArea(contour)
        if 10 < area < 500:  # 根据实际情况调整面积阈值
            # 获取轮廓的边界框
            x, y, w, h = cv2.boundingRect(contour)
            
            # 检查该区域是否足够暗（细胞）
            region = blurred[y:y+h, x:x+w]
            mean_intensity = np.mean(region)
            
            # 只有足够暗的区域才认为是细胞（阈值可根据需要调整）
            if mean_intensity < 100:  # 暗区域阈值
                # 计算等效圆的半径
                radius = np.sqrt(area / np.pi)
                
                # 绘制圆形标记细胞
                cv2.circle(result_image, (x + w//2, y + h//2), int(radius), (0, 255, 0), 2)
                cell_count_filtered += 1
    
    # 显示结果
    print(f"分水岭算法检测到 {cell_count} 个区域")
    print(f"经过亮度过滤后检测到 {cell_count_filtered} 个细胞")
    
    # 显示图像
    cv2.imshow("Original", image)
    cv2.imshow("Binary", binary)
    cv2.imshow("Distance Transform", dist_transform)
    cv2.imshow("Sure FG", sure_fg)
    cv2.imshow("Sure BG", sure_bg)
    cv2.imshow("Markers", np.uint8(markers * 50))  # 放大标记值以便可视化
    cv2.imshow("Watershed Result", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return cell_count_filtered

def detect_cells_simple_dark_filter(image_path):
    """
    简化版本：只使用暗区域过滤检测细胞
    
    Args:
        image_path (str): 图像文件路径
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return
    
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 使用高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 使用阈值分割，将暗色细胞从明亮背景中分离出来
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    
    # 形态学操作
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # 查找轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 在原图上绘制检测到的细胞
    result_image = image.copy()
    cell_count = 0
    
    for contour in contours:
        # 计算轮廓面积，过滤掉太小或太大的区域
        area = cv2.contourArea(contour)
        if 15 < area < 500:  # 根据实际情况调整面积阈值
            # 获取轮廓的边界框
            x, y, w, h = cv2.boundingRect(contour)
            
            # 检查该区域是否足够暗（细胞）
            region = blurred[y:y+h, x:x+w]
            mean_intensity = np.mean(region)
            
            # 只有足够暗的区域才认为是细胞（阈值可根据需要调整）
            if mean_intensity < 120:  # 暗区域阈值
                # 计算等效圆的半径
                radius = np.sqrt(area / np.pi)
                
                # 绘制圆形标记细胞
                cv2.circle(result_image, (x + w//2, y + h//2), int(radius), (0, 0, 255), 2)
                cell_count += 1
    
    # 显示结果
    print(f"检测到 {cell_count} 个细胞（仅考虑足够暗的区域）")
    
    # 显示图像
    cv2.imshow("Original", image)
    cv2.imshow("Binary", binary)
    cv2.imshow("Result", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return cell_count

# 使用示例
if __name__ == "__main__":
    # 替换为您的明场图像路径
    image_path = r"refer\light_cell\test1.jpg"
    
    print("使用暗区域过滤的简化检测方法:")
    detect_cells_simple_dark_filter(image_path)
    
    print("\n使用分水岭算法的检测方法:")
    detect_cells_watershed(image_path)