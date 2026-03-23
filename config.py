# config.py
import os

# Берем токены из переменных окружения
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
GIGACHAT_CLIENT_SECRET = os.environ.get('GIGACHAT_SECRET', '')

# Проверка для отладки
if not TELEGRAM_BOT_TOKEN:
    print("⚠️ ВНИМАНИЕ: TELEGRAM_TOKEN не найден!")
if not GIGACHAT_CLIENT_SECRET:
    print("⚠️ ВНИМАНИЕ: GIGACHAT_SECRET не найден!")
