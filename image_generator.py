# image_generator.py
from PIL import Image, ImageDraw, ImageFont
import random
import os
import logging

logger = logging.getLogger(__name__)


def generate_avatar(colors, output_path="avatar.png", size=(500, 500)):
    """
    Генерирует аватарку для соцсетей на основе цветовой палитры

    colors: список HEX-цветов
    output_path: путь для сохранения
    size: размер изображения
    """
    try:
        # Создаем белый фон
        img = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(img)

        # Выбираем 3 случайных цвета из палитры
        color1 = colors[0] if colors else "#FF6B6B"
        color2 = colors[1] if len(colors) > 1 else "#4ECDC4"
        color3 = colors[2] if len(colors) > 2 else "#45B7D1"

        # Рисуем абстрактные фигуры
        width, height = size

        # Круг в центре
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            fill=color1,
            outline=color2,
            width=10
        )

        # Рисуем треугольники вокруг
        for i in range(6):
            angle = i * 60  # 60 градусов между треугольниками
            x = center_x + (radius + 30) * random.uniform(0.8, 1.2) * random.choice([-1, 1])
            y = center_y + (radius + 30) * random.uniform(0.8, 1.2) * random.choice([-1, 1])
            points = [
                (x, y),
                (x + random.randint(20, 40), y + random.randint(20, 40)),
                (x - random.randint(20, 40), y + random.randint(20, 40))
            ]
            draw.polygon(points, fill=color3)

        # Добавляем маленькие точки
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=color2)

        # Сохраняем изображение
        img.save(output_path)
        logger.info(f"Аватарка сохранена: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Ошибка при генерации аватарки: {e}")
        return None


def generate_background(colors, output_path="background.png", size=(1200, 630)):
    """
    Генерирует фон для соцсетей на основе цветовой палитры

    colors: список HEX-цветов
    output_path: путь для сохранения
    size: размер изображения (1200x630 - стандарт для соцсетей)
    """
    try:
        # Создаем изображение
        img = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(img)

        width, height = size

        # Создаем градиент (упрощенная версия)
        color_start = colors[0] if colors else "#FF6B6B"
        color_end = colors[1] if len(colors) > 1 else "#4ECDC4"

        # Рисуем полосы
        for i in range(10):
            y = i * (height // 10)
            color_ratio = i / 10
            # Смешиваем цвета
            r = int(int(color_start[1:3], 16) * (1 - color_ratio) + int(color_end[1:3], 16) * color_ratio)
            g = int(int(color_start[3:5], 16) * (1 - color_ratio) + int(color_end[3:5], 16) * color_ratio)
            b = int(int(color_start[5:7], 16) * (1 - color_ratio) + int(color_end[5:7], 16) * color_ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            draw.rectangle([0, y, width, y + height // 10], fill=color)

        # Добавляем геометрические фигуры
        for _ in range(30):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size_shape = random.randint(20, 80)
            color = random.choice(colors)
            draw.rectangle([x, y, x + size_shape, y + size_shape], fill=color, outline=None)

        # Сохраняем изображение
        img.save(output_path)
        logger.info(f"Фон сохранен: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Ошибка при генерации фона: {e}")
        return None


def generate_pattern(colors, output_path="pattern.png", size=(800, 800)):
    """
    Генерирует паттерн для упаковки или мерча

    colors: список HEX-цветов
    output_path: путь для сохранения
    size: размер изображения
    """
    try:
        img = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(img)

        width, height = size
        pattern_size = 80

        # Создаем повторяющийся паттерн
        for x in range(0, width, pattern_size):
            for y in range(0, height, pattern_size):
                color = random.choice(colors)
                # Рисуем разные формы
                shape_type = random.choice(['circle', 'square', 'triangle'])

                if shape_type == 'circle':
                    draw.ellipse([x, y, x + pattern_size - 10, y + pattern_size - 10], fill=color)
                elif shape_type == 'square':
                    draw.rectangle([x, y, x + pattern_size - 10, y + pattern_size - 10], fill=color)
                else:
                    points = [
                        (x + pattern_size // 2, y),
                        (x + pattern_size - 10, y + pattern_size - 10),
                        (x, y + pattern_size - 10)
                    ]
                    draw.polygon(points, fill=color)

        img.save(output_path)
        logger.info(f"Паттерн сохранен: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Ошибка при генерации паттерна: {e}")
        return None


def generate_all_images(colors, output_folder="generated_images"):
    """
    Генерирует все три типа изображений

    colors: список HEX-цветов
    output_folder: папка для сохранения
    возвращает список путей к сгенерированным файлам
    """
    # Создаем папку, если её нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = []

    # Генерируем аватарку
    avatar_path = os.path.join(output_folder, "avatar.png")
    if generate_avatar(colors, avatar_path):
        images.append(avatar_path)

    # Генерируем фон
    background_path = os.path.join(output_folder, "background.png")
    if generate_background(colors, background_path):
        images.append(background_path)

    # Генерируем паттерн
    pattern_path = os.path.join(output_folder, "pattern.png")
    if generate_pattern(colors, pattern_path):
        images.append(pattern_path)

    return images