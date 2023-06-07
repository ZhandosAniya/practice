import logging
from main import TOKEN
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Обработчик команды /start
@dp.message_handler(commands=['start', 'menu'])
async def start(message: types.Message):
    # Текст приветственного сообщения
    text = "Привет! Хочешь такой же красивый маникюр? Тогда тебе к нам, 10% скидка тому кто запишется сейчас! 😍✨"

    # Путь к файлу фото
    photo_path = "маник.JPG"

    # Создаем главное меню с inline-кнопками
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("О нас 😎", callback_data='about'),
        types.InlineKeyboardButton("Услуги  🗒️", callback_data='services'),
        types.InlineKeyboardButton("Записаться 👍", callback_data='book'),
        types.InlineKeyboardButton("Связь с нами ❤️", callback_data='contact')
    )

    # Отправляем фото с описанием и главное меню
    await bot.send_photo(chat_id=message.chat.id, photo=open(photo_path, 'rb'), caption=text, reply_markup=markup)

# Обработчик нажатий на inline-кнопки
@dp.callback_query_handler(lambda query: True)
async def process_callback(query: types.CallbackQuery):
    choice = query.data

    if choice == 'about':
        await query.answer("Ты не пожалеешь😍")

        text_about = "Привет меня зовут Ания, и я работаю мастером маникюра более 2 лет. Более 2000 тысячи довольных клиентов❤️✅"

        # Путь к файлу фото Мои работы
        my_works_photo_path = "ания.jpg"

        # Создаем inline-кнопки для Мои работы и Главное меню
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("Мои работы 😍", url="https://instagram.com/justaniya_nail?igshid=YmMyMTA2M2Y="),
            types.InlineKeyboardButton("Главное меню🔙", callback_data='main_menu')
        )

        # Отправляем фото Мои работы с inline-кнопками
        await bot.send_photo(chat_id=query.message.chat.id, photo=open(my_works_photo_path, 'rb'), caption=text_about, reply_markup=markup)

    elif choice == 'services':

        # Путь к файлу фото услуг
        services_photo_path = "service.png"

        # Создаем inline-кнопки для Записаться и Главное меню
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("Записаться✅", url="https://dikidi.net/ru/profile/aniya_bot_1135255"),
            types.InlineKeyboardButton("Главное меню🔙", callback_data='main_menu')
        )

        # Отправляем фото услуг с inline-кнопками
        await bot.send_photo(chat_id=query.message.chat.id, photo=open(services_photo_path, 'rb'), reply_markup=markup)

    elif choice == 'book':

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("Записаться✅", url="https://dikidi.net/ru/profile/aniya_bot_1135255"),
            types.InlineKeyboardButton("Главное меню🔙", callback_data='main_menu')
        )
        await bot.send_message(chat_id=query.message.chat.id, text="Спасибо что выбираете нас😍", reply_markup=markup)

    elif choice == 'contact':
        await query.answer("Выберите удобную соц.сеть для связи")

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("Inst", url="https://www.instagram.com/_justaniya_/"),
            types.InlineKeyboardButton("WhatsApp", url="https://wa.me/77763302284"),
            types.InlineKeyboardButton("Telegram", url="https://t.me/justaniya"),
            types.InlineKeyboardButton("Назад🔙", callback_data='main_menu')
        )

        await bot.send_message(chat_id=query.message.chat.id, text="Выберите удобную соц.сеть для связи📞:", reply_markup=markup)

    # Дополнительная логика для кнопок "Главное меню"
    elif choice == 'main_menu':
        await start(query.message)  # Вызываем команду /start снова

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
