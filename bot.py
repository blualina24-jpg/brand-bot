import asyncio
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Импорты из наших файлов
from config import TELEGRAM_BOT_TOKEN, GIGACHAT_CLIENT_SECRET
from gigachat_helper import get_brand_concept
from image_generator import generate_all_images
from html_generator import create_brandbook_html as create_brandbook

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния диалога
NAME, VALUES, AUDIENCE, IMAGE_CHOICE = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога - запрос названия бренда"""
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        "Я помогу тебе создать полную бренд-концепцию:\n"
        "• Легенду бренда\n"
        "• Цветовую палитру\n"
        "• Рекомендации по шрифтам\n"
        "• Тон коммуникации\n"
        "• Визуальные материалы (аватарка, фон, паттерн)\n"
        "• Полный брендбук в HTML (можно сохранить как PDF)\n\n"
        "Давай начнем! Напиши название компании или бренда."
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получаем название бренда"""
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        "Отлично! 📝\n\n"
        "Теперь опиши ценности бренда.\n"
        "Например: 'инновации, забота о клиентах, качество'"
    )
    return VALUES


async def get_values(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получаем ценности бренда"""
    context.user_data['values'] = update.message.text
    await update.message.reply_text(
        "Понял! 🎯\n\n"
        "И последнее: опиши целевую аудиторию.\n"
        "Например: 'молодые мамы 25-35 лет, ценящие комфорт'"
    )
    return AUDIENCE


async def get_audience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получаем аудиторию и запускаем генерацию концепции"""
    context.user_data['audience'] = update.message.text

    # Показываем, что начали обработку
    await update.message.reply_text("✅ Бриф собран! Начинаю обработку...")

    # Подготавливаем данные для GigaChat
    brief = {
        'name': context.user_data['name'],
        'values': context.user_data['values'],
        'audience': context.user_data['audience'],
        'client_secret': GIGACHAT_CLIENT_SECRET
    }

    await update.message.reply_text("🤖 Запрашиваю концепцию у GigaChat... Это займет 5-10 секунд.")

    # Получаем концепцию от GigaChat
    concept = get_brand_concept(brief)

    # Формируем красивый ответ
    response = f"""
✨ **Бренд-концепция готова!** ✨

**📖 Легенда бренда:**
{concept['legend']}

**🎨 Цветовая палитра:**
{', '.join(concept['colors'])}

**✍️ Рекомендуемые шрифты:**
{', '.join(concept['fonts'])}

**💬 Тон коммуникации:**
{concept['tone']}
    """

    await update.message.reply_text(response, parse_mode='Markdown')

    # Сохраняем концепцию и бриф для следующего шага
    context.user_data['concept'] = concept
    context.user_data['brief'] = brief

    # Спрашиваем про генерацию изображений
    await update.message.reply_text(
        "🎨 **Хотите сгенерировать визуальные материалы?**\n\n"
        "Я могу создать:\n"
        "• Аватарку для соцсетей\n"
        "• Фоновое изображение\n"
        "• Паттерн для мерча\n"
        "• Полный брендбук в HTML (можно сохранить как PDF)\n\n"
        "Напишите **да** или **нет**",
        parse_mode='Markdown'
    )

    return IMAGE_CHOICE


async def handle_image_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатываем выбор пользователя о генерации изображений"""
    choice = update.message.text.lower()

    if choice in ['да', 'yes', 'конечно', 'давай', 'давай!', 'д', 'ye', 'y']:
        await update.message.reply_text(
            "🎨 Начинаю генерацию материалов...\n"
            "Это займет около 30 секунд."
        )

        concept = context.user_data.get('concept')
        brief = context.user_data.get('brief')

        if concept and concept.get('colors') and brief:
            try:
                # 1. Генерируем изображения
                await update.message.reply_text("📸 Шаг 1/2: Генерирую изображения...")
                images = generate_all_images(concept['colors'], output_folder="generated_images")

                # 2. Создаем HTML брендбук
                await update.message.reply_text("📄 Шаг 2/2: Создаю HTML брендбук...")
                brandbook_path = create_brandbook(
                    brief,
                    concept,
                    images_folder="generated_images",
                    output_path="brandbook.html"
                )

                if images or brandbook_path:
                    await update.message.reply_text("✅ Все материалы готовы! Отправляю...")

                    # Отправляем изображения
                    for img_path in images:
                        if os.path.exists(img_path):
                            with open(img_path, 'rb') as photo:
                                # Определяем тип изображения для подписи
                                img_name = os.path.basename(img_path).replace('.png', '').capitalize()
                                if 'Avatar' in img_name:
                                    caption = "👤 Аватарка для соцсетей"
                                elif 'Background' in img_name:
                                    caption = "🖼️ Фоновое изображение"
                                elif 'Pattern' in img_name:
                                    caption = "🎨 Паттерн для мерча"
                                else:
                                    caption = f"✨ {img_name}"

                                await update.message.reply_photo(
                                    photo=photo,
                                    caption=caption
                                )

                    # Отправляем HTML брендбук
                    if brandbook_path and os.path.exists(brandbook_path):
                        with open(brandbook_path, 'rb') as html_file:
                            await update.message.reply_document(
                                document=html_file,
                                filename=f"brandbook_{brief['name'].replace(' ', '_')}.html",
                                caption="📘 **Брендбук в формате HTML!**\n\n"
                                        "📌 **Как сохранить как PDF:**\n"
                                        "1. Откройте файл в браузере\n"
                                        "2. Нажмите Ctrl+P (Cmd+P на Mac)\n"
                                        "3. Выберите 'Сохранить как PDF'\n\n"
                                        "📋 **В документе:**\n"
                                        "• Легенда бренда\n"
                                        "• Цветовая палитра (5 цветов)\n"
                                        "• Рекомендации по шрифтам\n"
                                        "• Все визуальные материалы\n"
                                        "• Рекомендации по использованию",
                                parse_mode='Markdown'
                            )

                    # Финальное сообщение
                    await update.message.reply_text(
                        "🎉 **Готово! Бренд-концепция полностью готова!** 🎉\n\n"
                        "✅ **Вы получили:**\n"
                        "• Легенду бренда\n"
                        "• Цветовую палитру (5 цветов)\n"
                        "• Рекомендации по шрифтам\n"
                        "• Тон коммуникации\n"
                        "• 3 визуальных материала (аватарка, фон, паттерн)\n"
                        "• Полный брендбук в HTML\n\n"
                        "💡 **Совет:** Сохраните все файлы - они понадобятся для дальнейшей работы!\n\n"
                        "Чтобы создать новый бренд, отправьте /start",
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text(
                        "❌ Не удалось создать материалы.\n"
                        "Попробуйте позже или обратитесь к администратору."
                    )

            except Exception as e:
                logger.error(f"Ошибка при создании материалов: {e}")
                await update.message.reply_text(
                    f"❌ Произошла ошибка: {str(e)}\n\n"
                    "Попробуйте еще раз, отправив /start"
                )
        else:
            await update.message.reply_text(
                "❌ Нет данных для создания материалов.\n"
                "Пожалуйста, начните заново с команды /start"
            )

    else:
        await update.message.reply_text(
            "Хорошо! 👍\n\n"
            "Ваша концепция сохранена выше в диалоге.\n"
            "Если захотите сгенерировать визуальные материалы позже, "
            "просто запустите бота заново командой /start"
        )

    # Очищаем данные пользователя
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена диалога"""
    await update.message.reply_text(
        "❌ Диалог отменен.\n\n"
        "Для начала нового используйте команду /start"
    )
    context.user_data.clear()
    return ConversationHandler.END


def main() -> None:
    """Запуск бота"""
    # Создаем папку для изображений, если её нет
    if not os.path.exists("generated_images"):
        os.makedirs("generated_images")
        logger.info("📁 Создана папка generated_images")

    # Создаем приложение
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Создаем ConversationHandler для управления диалогом
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            VALUES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_values)],
            AUDIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_audience)],
            IMAGE_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_image_choice)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик
    application.add_handler(conv_handler)

    # Запускаем бота
    logger.info("🚀 Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()