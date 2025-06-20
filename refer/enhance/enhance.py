import cv2
import numpy as np
import os
import random
import glob

SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

class DataAugmenter:
    
    def __init__(self, input_dir, output_dir, img_suffix='.jpg'):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.img_suffix = img_suffix
        self.create_dirs()
        
    def create_dirs(self):
        """创建输出目录"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_images(self):
        """加载图像和对应的标注文件"""
        image_paths = []
        for ext in SUPPORTED_FORMATS:
            image_paths.extend(glob.glob(os.path.join(self.input_dir, f'*{ext}')))
        return image_paths
    
    def random_hsv(self, image, h_gain=0.3, s_gain=0.5, v_gain=0.5):
        """随机调整HSV颜色空间"""
        r = np.random.uniform(-1, 1, 3) * [h_gain, s_gain, v_gain] + 1

        # 转换为HSV并拆分通道，保留uint8格式用于索引
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hue, sat, val = cv2.split(hsv)

        # 创建查找表
        x = np.arange(0, 256, dtype="uint8")  # 确保是 uint8 类型
        lut_hue = ((x * r[0]) % 180).astype("uint8")
        lut_sat = np.clip(x * r[1], 0, 255).astype("uint8")
        lut_val = np.clip(x * r[2], 0, 255).astype("uint8")

        # 使用原始 uint8 的 hue/sat/val 作为索引
        hsv = cv2.merge((
            cv2.LUT(hue, lut_hue),
            cv2.LUT(sat, lut_sat),
            cv2.LUT(val, lut_val)
        ))

        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def random_flip(self, image, label=None, p=0.5):
        """随机水平翻转"""
        if random.random() < p:
            image = cv2.flip(image, 1)
            # 如果有标签文件需要同步翻转
            if label is not None:
                # 这里需要根据你的标注格式实现相应的坐标转换
                pass
        return image

    def random_rotation(self, image, label=None, max_angle=30):
        """随机旋转"""
        angle = random.uniform(-max_angle, max_angle)
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(image, M, (w, h))
        
        # 如果有标签文件需要同步旋转
        if label is not None:
            # 实现标注坐标的旋转转换
            pass
            
        return rotated_image

    def random_scale(self, image, label=None, scale_range=(0.8, 1.2)):
        """随机缩放"""
        scale = random.uniform(scale_range[0], scale_range[1])
        new_size = tuple(int(dim * scale) for dim in image.shape[1::-1])
        resized_image = cv2.resize(image, new_size)
        
        # 如果有标签文件需要同步缩放
        if label is not None:
            # 实现标注坐标的缩放转换
            pass
            
        return resized_image

    def random_crop(self, image, label=None, crop_size=None):
        """随机裁剪"""
        if crop_size is None:
            crop_size = (image.shape[1] // 2, image.shape[0] // 2)
            
        start_x = random.randint(0, image.shape[1] - crop_size[0])
        start_y = random.randint(0, image.shape[0] - crop_size[1])
        
        cropped_image = image[start_y:start_y+crop_size[1], start_x:start_x+crop_size[0]]
        
        # 如果有标签文件需要同步裁剪
        if label is not None:
            # 实现标注坐标的裁剪转换
            pass
            
        return cropped_image

    # 在 augment 方法中加入调试输出
    def augment(self, num_augmentations=5):
        image_paths = self.load_images()
        print(f"找到 {len(image_paths)} 张图像")

        for img_path in image_paths:
            image = cv2.imread(img_path)
            if image is None:
                print(f"[警告] 无法读取图像: {img_path}")
                continue

            base_name = os.path.splitext(os.path.basename(img_path))[0]
            print(f"正在处理: {img_path}")

            for i in range(num_augmentations):
                augmented_image = image.copy()

                # 随机选择增强操作
                if random.random() > 0.5:
                    augmented_image = self.random_hsv(augmented_image)

                if random.random() > 0.5:
                    augmented_image = self.random_flip(augmented_image)

                if random.random() > 0.5:
                    augmented_image = self.random_rotation(augmented_image)

                if random.random() > 0.5:
                    augmented_image = self.random_scale(augmented_image)

                if random.random() > 0.5:
                    augmented_image = self.random_crop(augmented_image)

                # 保存增强后的图像
                output_path = os.path.join(self.output_dir, f"{base_name}_aug_{i}{self.img_suffix}")
                success = cv2.imwrite(output_path, augmented_image)
                if not success:
                    print(f"[错误] 保存失败: {output_path}")

if __name__ == "__main__":
    augmenter = DataAugmenter(
        input_dir = r"refer\enhance\input",
        output_dir = r"refer\enhance\output"
    )
    augmenter.augment(num_augmentations=20)