# gigachat_helper.py
import json
import logging
from gigachat import GigaChat

logger = logging.getLogger(__name__)


def get_brand_concept(brief_data):
    """
    Отправляет бриф в GigaChat и получает концепцию бренда

    brief_data: словарь с ключами 'name', 'values', 'audience', 'client_secret'
    """

    # Формируем промпт (инструкцию) для GigaChat
    prompt = f"""
Ты — профессиональный бренд-стратег. Создай концепцию бренда по брифу.

Бриф:
- Название бренда: {brief_data['name']}
- Ценности: {brief_data['values']}
- Целевая аудитория: {brief_data['audience']}

Ответь ТОЛЬКО в формате JSON, без лишнего текста:
{{
    "legend": "короткая вдохновляющая история бренда (1-2 предложения)",
    "colors": ["#HEX1", "#HEX2", "#HEX3", "#HEX4", "#HEX5"],
    "fonts": ["шрифт1", "шрифт2"],
    "tone": "описание тона общения (например: дружелюбный, профессиональный)"
}}
"""

    try:
        # Проверяем, есть ли секрет
        if not brief_data.get('client_secret'):
            logger.warning("Нет client_secret для GigaChat")
            return get_default_concept()

        # Подключаемся к GigaChat
        with GigaChat(
                credentials=brief_data['client_secret'],
                scope="GIGACHAT_API_PERS",
                verify_ssl_certs=False
        ) as giga:

            logger.info("Отправляем запрос в GigaChat...")
            response = giga.chat(prompt)
            result_text = response.choices[0].message.content
            logger.info(f"Получен ответ от GigaChat: {result_text[:200]}...")

            # Пытаемся извлечь JSON из ответа
            concept = extract_json(result_text)
            if concept:
                return concept
            else:
                logger.error("Не удалось извлечь JSON из ответа")
                return get_default_concept()

    except Exception as e:
        logger.error(f"Ошибка при обращении к GigaChat: {e}")
        return get_default_concept()


def extract_json(text):
    """Пытается извлечь JSON из текста"""
    try:
        # Ищем где начинается и заканчивается JSON
        start = text.find('{')
        end = text.rfind('}') + 1

        if start != -1 and end > start:
            json_str = text[start:end]
            return json.loads(json_str)
        else:
            return json.loads(text)
    except:
        return None


def get_default_concept():
    """Возвращает дефолтную концепцию, если GigaChat недоступен"""
    return {
        "legend": "Бренд, созданный для вдохновения и достижения целей.",
        "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
        "fonts": ["Montserrat", "Open Sans"],
        "tone": "Дружелюбный и вдохновляющий"
    }