# html_generator.py
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)


def create_brandbook_html(brief_data, concept, images_folder="generated_images", output_path="brandbook.html"):
    """
    Создает HTML брендбук с изображениями
    """
    try:
        # Получаем цвета
        colors = concept['colors']
        # Убеждаемся, что у всех цветов есть #
        colors_with_hash = []
        for c in colors:
            if not c.startswith('#'):
                c = '#' + c
            colors_with_hash.append(c)

        # Создаем HTML с красивым дизайном и встроенными изображениями
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Брендбук: {brief_data['name']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px;
            line-height: 1.6;
            color: #333;
            background: #fafafa;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: {colors_with_hash[0]};
            border-bottom: 3px solid {colors_with_hash[0]};
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        h2 {{
            color: {colors_with_hash[1] if len(colors_with_hash) > 1 else colors_with_hash[0]};
            margin-top: 25px;
            border-left: 4px solid {colors_with_hash[0]};
            padding-left: 15px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 50px;
            padding: 30px;
            background: linear-gradient(135deg, {colors_with_hash[0]}20, {colors_with_hash[1]}20);
            border-radius: 15px;
        }}
        .header h1 {{
            border: none;
            color: {colors_with_hash[0]};
            font-size: 36px;
            margin-bottom: 10px;
        }}
        .date {{
            text-align: right;
            color: #666;
            font-size: 14px;
            margin-top: 20px;
            padding-top: 10px;
            border-top: 1px solid #eee;
        }}
        .color-palette {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
        }}
        .color-item {{
            text-align: center;
            flex: 1;
            min-width: 100px;
        }}
        .color-box {{
            width: 100%;
            height: 80px;
            border-radius: 8px;
            margin-bottom: 8px;
            border: 2px solid #ddd;
        }}
        .color-code {{
            font-family: monospace;
            font-size: 12px;
        }}
        .info-box {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }}
        .image-gallery {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
        }}
        .image-card {{
            flex: 1;
            min-width: 250px;
            background: #f9f9f9;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }}
        .image-card img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        hr {{
            margin: 30px 0;
            border: none;
            border-top: 2px solid #eee;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 12px;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin: 8px 0;
        }}
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
            .image-card {{
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>✨ Брендбук: {brief_data['name']} ✨</h1>
        <p><em>Ваша уникальная идентичность</em></p>
    </div>

    <div class="date">
        📅 Дата создания: {datetime.now().strftime('%d.%m.%Y')}
    </div>

    <hr>

    <h1>📖 1. О бренде</h1>

    <h2>🏷️ 1.1 Название</h2>
    <p><strong>{brief_data['name']}</strong></p>

    <h2>📜 1.2 Легенда бренда</h2>
    <div class="info-box">
        <p>{concept['legend']}</p>
    </div>

    <h2>💎 1.3 Ценности</h2>
    <p>{brief_data['values']}</p>

    <h2>👥 1.4 Целевая аудитория</h2>
    <p>{brief_data['audience']}</p>

    <h2>💬 1.5 Тон коммуникации</h2>
    <div class="info-box">
        <p><strong>{concept['tone']}</strong></p>
    </div>

    <hr>

    <h1>🎨 2. Визуальная идентификация</h1>

    <h2>🌈 2.1 Цветовая палитра</h2>
    <div class="color-palette">
"""

        # Добавляем цвета
        for color in colors_with_hash:
            html_content += f"""
        <div class="color-item">
            <div class="color-box" style="background-color: {color};"></div>
            <div class="color-code">{color}</div>
        </div>
"""

        html_content += """
    </div>

    <h2>✍️ 2.2 Рекомендуемые шрифты</h2>
    <ul>
"""

        # Добавляем шрифты
        for font in concept['fonts']:
            html_content += f"        <li><strong>{font}</strong></li>\n"

        html_content += """
    </ul>

    <hr>

    <h1>🖼️ 3. Визуальные материалы</h1>
    <div class="image-gallery">
"""

        # Добавляем изображения
        if os.path.exists(images_folder):
            images = [
                ('avatar.png', '👤 Аватарка для соцсетей'),
                ('background.png', '🖼️ Фоновое изображение'),
                ('pattern.png', '🎨 Паттерн для мерча')
            ]

            for img_file, description in images:
                img_path = os.path.join(images_folder, img_file)
                if os.path.exists(img_path):
                    # Кодируем изображение в base64 для вставки в HTML
                    import base64
                    with open(img_path, 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode('utf-8')

                    html_content += f"""
        <div class="image-card">
            <img src="data:image/png;base64,{img_data}" alt="{description}">
            <p><strong>{description}</strong></p>
            <p><small>Создано на основе вашей цветовой палитры</small></p>
        </div>
"""

        html_content += """
    </div>

    <hr>

    <h1>💡 4. Рекомендации по использованию</h1>

    <h2>🎨 4.1 Использование цветов</h2>
    <div class="info-box">
        <p><strong>Основные цвета:</strong> """ + ", ".join(colors_with_hash[:3]) + """</p>
        <p><strong>Акцентные цвета:</strong> """ + ", ".join(colors_with_hash[3:]) + """</p>
        <p>💡 <em>Используйте основной цвет для ключевых элементов бренда, а акцентные — для выделения важной информации.</em></p>
    </div>

    <h2>📝 4.2 Использование шрифтов</h2>
    <ul>
        <li><strong>Для заголовков:</strong> """ + concept['fonts'][0] + """</li>
        <li><strong>Для основного текста:</strong> """ + (
            concept['fonts'][1] if len(concept['fonts']) > 1 else concept['fonts'][0]) + """</li>
    </ul>

    <h2>📍 4.3 Где использовать</h2>
    <ul>
        <li>📱 Социальные сети (аватарка, обложки, посты)</li>
        <li>🌐 Сайт и лендинги</li>
        <li>📄 Печатная продукция (визитки, буклеты)</li>
        <li>🎁 Мерч и сувенирная продукция</li>
        <li>📢 Рекламные материалы</li>
    </ul>

    <hr>

    <h1>🎯 5. Заключение</h1>
    <div class="info-box">
        <p>Данный брендбук создан специально для бренда <strong>«{brief_data['name']}»</strong> на основе предоставленного брифа.</p>
        <p>Он содержит все необходимые элементы для создания единого и узнаваемого стиля бренда.</p>
        <p>✨ <em>При развитии бренда рекомендуется придерживаться заданных параметров для сохранения целостности восприятия.</em></p>
    </div>

    <div class="footer">
        <p>Создано с ❤️ с помощью Бренд-помощника (AI)</p>
        <p>💡 <strong>Совет:</strong> Нажмите Ctrl+P (или Cmd+P) и выберите "Сохранить как PDF"</p>
        <p>Для создания новой концепции отправьте команду /start</p>
    </div>
</div>
</body>
</html>
"""

        # Сохраняем HTML файл
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"✅ HTML брендбук сохранен: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"❌ Ошибка при создании HTML: {e}")
        return None