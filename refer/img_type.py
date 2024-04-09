import cv2

def check_if_image_is_rgb(image_path):
    """
    检查给定路径下的图像是否为三通道（RGB）图像。

    参数:
        image_path (str): 待检查图像的文件路径。

    返回:
        bool: 如果图像为三通道，则返回True；否则返回False。
    """
    # 读取图像
    img = cv2.imread(image_path)

    # 检查图像是否成功读取
    if img is None:
        print(f"未能成功读取图像 {image_path}")
        return False

    # 获取图像通道数（最后一个维度的大小）
    num_channels = img.shape[-1]

    # 判断是否为三通道图像（RGB）
    is_rgb = num_channels == 3

    return is_rgb

if __name__ == "__main__":
    """
    用于测试的示例代码。
    """
    # 示例图像路径
    image_to_check = "samples\origin.png"
    
    print("正在检查图像是否为三通道（RGB）图像...")
    is_rgb_image = check_if_image_is_rgb(image_to_check)
    print(f"图像 '{image_to_check}' 是否为三通道：{is_rgb_image}")