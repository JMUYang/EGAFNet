import cv2
import numpy as np
from PIL import Image
import os


def generate_edge_labels(label_folder, output_folder):
    """
    从分割标签生成边缘标签

    Args:
        label_folder: 分割标签文件夹（1.tif, 2.tif, ...）
        output_folder: 边缘标签输出文件夹
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    label_files = sorted([f for f in os.listdir(label_folder) if f.endswith('.tif')])

    for label_file in label_files:
        # 读取标签
        label_path = os.path.join(label_folder, label_file)
        label = cv2.imread(label_path, cv2.IMREAD_GRAYSCALE)

        # 二值化（假设建筑物为白色/255，背景为黑色/0）
        _, binary = cv2.threshold(label, 127, 255, cv2.THRESH_BINARY)

        # 使用Canny边缘检测
        edges = cv2.Canny(binary, 100, 200)

        # 膨胀边缘使其更明显（可选）
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

        # 保存边缘标签
        output_path = os.path.join(output_folder, label_file)
        cv2.imwrite(output_path, edges)

        print(f"生成边缘: {label_file}")

    print(f"✅ 完成！共生成 {len(label_files)} 个边缘标签")


# 使用示例
label_folder = r"D:\WHU Building\test\label"
edge_folder = r"D:\WHU Building\test\edge"
generate_edge_labels(label_folder, edge_folder)