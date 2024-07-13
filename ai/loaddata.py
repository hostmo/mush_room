from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data import random_split, DataLoader

def load_data(img_dir, train_rate=0.8, batch_size=64):
    # VGG16 预训练模型推荐的均值和标准差
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    transform = transforms.Compose([
        transforms.Resize(256),  # VGG16 推荐的输入大小为 224x224，但通常会先resize到256再随机裁剪
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])

    # 加载数据集
    dataset = ImageFolder(img_dir, transform=transform)

    # 划分训练集和测试集
    total_length = len(dataset)
    train_length = int(total_length * train_rate)
    test_length = total_length - train_length
    train_dataset, test_dataset = random_split(dataset, [train_length, test_length])

    # 创建 DataLoader
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)  # 测试集不需要shuffle

    return train_loader, test_loader, dataset.classes
