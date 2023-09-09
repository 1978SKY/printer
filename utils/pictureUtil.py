import os.path

from PIL import Image


# 计算点阵
def calculate_dot_matrix(file_path):
    if not os.path.exists(file_path):
        return 0, 0, 0

    image = Image.open(file_path)
    image = image.convert('RGB')

    width, height = image.size

    # 计算图片的点阵
    total_count, black_count, color_count = 0, 0, 0
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            total_count += 1
            if pixel == (0, 0, 0):  # 黑色
                black_count += 1
            elif pixel != (255, 255, 255):  # 非白，即彩色
                color_count += 1
    return total_count, black_count, color_count


# 计算价格ink_amount墨量，base_price基础价格，incremental_price递增价
def calculate_price(ink_amount, base_price, incremental_price):
    if ink_amount <= 0:
        return 0
    else:
        if ink_amount <= 1:
            return base_price
        else:
            return base_price + incremental_price * (ink_amount - 1)


if __name__ == '__main__':
    total = 0.1
    total += calculate_price(0.2, 0.1, 0.2)
    print(total)
