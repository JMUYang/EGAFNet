import os


def batch_rename_simple(folder_path, extension='tif'):
    """
    批量重命名文件夹中的图片为简单的数字格式：1.tif, 2.tif, 3.tif...

    Args:
        folder_path: 文件夹路径
        extension: 文件扩展名（如 'tif', 'png', 'jpg'）
    """

    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 {folder_path} 不存在！")
        return

    # 确保扩展名格式正确
    if not extension.startswith('.'):
        extension = '.' + extension

    # 获取所有指定扩展名的文件
    all_files = os.listdir(folder_path)
    files = [f for f in all_files if f.lower().endswith(extension.lower())]

    # 排序文件
    files.sort()

    if not files:
        print(f"在文件夹 {folder_path} 中没有找到 {extension} 文件！")
        return

    print(f"\n📁 文件夹: {folder_path}")
    print(f"找到 {len(files)} 个 {extension} 文件")
    print("\n前10个文件（排序后）：")
    for i, f in enumerate(files[:10], 1):
        print(f"  {i}. {f}")
    if len(files) > 10:
        print(f"  ... 共 {len(files)} 个文件")

    # 确认操作
    response = input(f"\n是否开始重命名这 {len(files)} 个文件为 1{extension}, 2{extension}, ...？(y/n): ")
    if response.lower() != 'y':
        print("操作已取消")
        return

    # 重命名文件
    renamed_count = 0
    for i, filename in enumerate(files, 1):
        new_name = f"{i}{extension}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        # 如果新文件名已存在，添加后缀
        if os.path.exists(new_path) and old_path != new_path:
            new_name = f"{i}_new{extension}"
            new_path = os.path.join(folder_path, new_name)
            print(f"  警告：{i}{extension} 已存在，将使用 {new_name}")

        try:
            os.rename(old_path, new_path)
            print(f"  {filename} -> {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"  错误：无法重命名 {filename} - {e}")

    print(f"\n✅ 重命名完成！共处理 {renamed_count} 个文件")


def process_whu_dataset():
    """
    处理WHU数据集的train文件夹
    """
    # WHU数据集的路径
    whu_path = r"D:\WHU Building"

    # 要处理的三个子文件夹
    sub_folders = ['image', 'label', 'edge']

    print("=" * 50)
    print("开始处理WHU数据集")
    print("=" * 50)

    for sub_folder in sub_folders:
        folder_path = os.path.join(whu_path, 'train', sub_folder)

        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            print(f"\n⚠️ 警告：文件夹不存在，跳过：{folder_path}")
            continue

        print(f"\n处理 {sub_folder} 文件夹...")
        batch_rename_simple(folder_path, extension='tif')

    print("\n" + "=" * 50)
    print("✅ WHU数据集处理完成！")
    print("=" * 50)


# 如果您想分别处理test文件夹，可以使用这个函数
def process_whu_test():
    """
    处理WHU数据集的test文件夹
    """
    whu_path = r"D:\WHU Building"
    sub_folders = ['image', 'label', 'edge']

    print("=" * 50)
    print("开始处理WHU测试集")
    print("=" * 50)

    for sub_folder in sub_folders:
        folder_path = os.path.join(whu_path, 'test', sub_folder)

        if not os.path.exists(folder_path):
            print(f"\n⚠️ 警告：文件夹不存在，跳过：{folder_path}")
            continue

        print(f"\n处理 test/{sub_folder} 文件夹...")
        batch_rename_simple(folder_path, extension='tif')

    print("\n" + "=" * 50)
    print("✅ WHU测试集处理完成！")
    print("=" * 50)


if __name__ == "__main__":
    # ===== 选择要处理的文件夹 =====
    print("请选择要处理的文件夹：")
    print("1. 处理 train 文件夹 (image, label, edge)")
    print("2. 处理 test 文件夹 (image, label, edge)")
    print("3. 处理自定义文件夹")

    choice = input("请输入选项 (1/2/3): ").strip()

    if choice == '1':
        process_whu_dataset()
    elif choice == '2':
        process_whu_test()
    elif choice == '3':
        # 自定义文件夹
        folder = input("请输入要处理的文件夹路径: ").strip()
        ext = input("请输入文件扩展名 (如 tif, png, jpg): ").strip()
        batch_rename_simple(folder, extension=ext)
    else:
        print("无效选项！")