import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from Dataloader import MyDataset
from model.EGAFNet import EGAF

print("=" * 60)
print("开始调试训练脚本")
print("=" * 60)

# 设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"1. 设备: {device}")

# 创建网络
try:
    print("2. 创建网络...")
    net = EGAF()
    net.to(device)
    print(f"   ✅ 网络创建成功，参数量: {sum(p.numel() for p in net.parameters()) / 1e6:.2f}M")
except Exception as e:
    print(f"   ❌ 网络创建失败: {e}")
    exit(1)

# 损失函数
criterion = nn.BCELoss()
print(f"3. 损失函数: {criterion}")

# 数据路径
train_path1 = r'D:\WHU Building\train\image'
train_path2 = r'D:\WHU Building\train\label'
train_path3 = r'D:\WHU Building\train\edge'

print("4. 检查数据路径:")
print(f"   image: {train_path1} - {'存在' if os.path.exists(train_path1) else '不存在'}")
print(f"   label: {train_path2} - {'存在' if os.path.exists(train_path2) else '不存在'}")
print(f"   edge: {train_path3} - {'存在' if os.path.exists(train_path3) else '不存在'}")

# 检查文件数量
if os.path.exists(train_path1):
    files = os.listdir(train_path1)
    print(f"   image文件夹中有 {len(files)} 个文件")
    if len(files) > 0:
        print(f"   前5个文件: {files[:5]}")

# 创建数据集
print("5. 创建数据集...")
try:
    train_dataset = MyDataset(train_path1, train_path2, train_path3)
    print(f"   ✅ 数据集创建成功，样本数: {len(train_dataset)}")
except Exception as e:
    print(f"   ❌ 数据集创建失败: {e}")
    import traceback

    traceback.print_exc()
    exit(1)

# 创建数据加载器
print("6. 创建数据加载器...")
try:
    train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, num_workers=0)
    print(f"   ✅ 数据加载器创建成功，batch数量: {len(train_loader)}")
except Exception as e:
    print(f"   ❌ 数据加载器创建失败: {e}")
    exit(1)

# 优化器
optimizer = torch.optim.Adam(net.parameters(), lr=0.0005)
print("7. 优化器创建成功")

print("\n" + "=" * 60)
print("准备开始训练循环")
print("=" * 60)

# 尝试获取第一个batch
print("8. 尝试获取第一个batch的数据...")
try:
    # 获取迭代器
    data_iter = iter(train_loader)
    print("   ✅ 成功创建数据迭代器")

    # 尝试获取第一个batch
    print("   正在加载第一个batch...")
    images, labels, edges = next(data_iter)
    print(f"   ✅ 成功加载第一个batch")
    print(f"   图像形状: {images.shape}")
    print(f"   标签形状: {labels.shape}")
    print(f"   边缘形状: {edges.shape}")

    # 测试前向传播
    print("\n9. 测试前向传播...")
    images = images.to(device)
    outputs, out_edges, out3, out4, out5 = net(images)
    print(f"   ✅ 前向传播成功")
    print(f"   输出形状: {outputs.shape}")

    # 测试损失计算
    print("\n10. 测试损失计算...")
    loss = criterion(outputs, labels.to(device))
    print(f"    ✅ 损失计算成功: {loss.item():.4f}")

except StopIteration:
    print("   ❌ 数据迭代器为空，没有数据！")
    exit(1)
except Exception as e:
    print(f"   ❌ 加载数据时出错: {e}")
    import traceback

    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("所有测试通过！现在开始正式训练循环")
print("=" * 60)

# 正式训练循环
num_epochs = 100
print(f"\n开始 {num_epochs} 个epoch的训练")

try:
    for epoch in range(num_epochs):
        print(f"\n>>> Epoch {epoch + 1}/{num_epochs} 开始")

        running_loss = 0
        batch_count = 0

        for i, (images, labels, edges) in enumerate(train_loader):
            # 简单的训练步骤
            images, labels, edges = images.to(device), labels.to(device), edges.to(device)

            outputs, out_edges, out3, out4, out5 = net(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            batch_count += 1

            if i % 10 == 0:
                print(f"   batch {i}/{len(train_loader)}, loss: {loss.item():.4f}")

        avg_loss = running_loss / batch_count
        print(f"✅ Epoch {epoch + 1} 完成，平均损失: {avg_loss:.4f}")

        # 只运行1个epoch测试
        if epoch >= 0:
            print("\n测试完成，退出循环")
            break

except Exception as e:
    print(f"训练循环中出错: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)
print("调试完成")
print("=" * 60)