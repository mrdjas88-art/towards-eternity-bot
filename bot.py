from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, VIDEO_1, VIDEO_2, VIDEO_3, VIDEO_4

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# память шагов пользователя
user_step = {}

# Функция для прогресс-бара
def get_progress_bar(step):
    progress = ["○"] * 4
    for i in range(step):
        progress[i] = "●"
    return " ".join(progress)

# 1. АВТОМАТИЧЕСКОЕ ПРИВЕТСТВИЕ
@dp.message_handler(content_types=types.ContentTypes.ANY)
async def welcome_new_user(message: types.Message):
    user_id = message.from_user.id
    
    # Если пользователь еще не начинал путь (первое сообщение не /start)
    if user_id not in user_step:
        user_step[user_id] = 0
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                text="🕋 НАЧАТЬ ПУТЬ РАЗМЫШЛЕНИЙ",
                callback_data="step_1"
            )
        )
        
        await message.answer(
            "Ассаляму алейкум. 🌙\n\n"
            "Добро пожаловать в бот «НАВСТРЕЧУ ВЕЧНОСТИ».\n\n"
            "Этот путь из 4 шагов поможет тебе задуматься...\n"
            "О самом главном — о жизни, смерти и вечности.\n\n"
            "Готов сделать первый шаг?",
            reply_markup=keyboard
        )

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_step[message.from_user.id] = 0

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="▶️ Начать путь размышлений",
            callback_data="step_1"
        )
    )

    await message.answer(
        "Ассаляму алейкум.\n\n"
        "Если ты сейчас здесь — это не случайно.\n"
        "Иногда достаточно одного напоминания,\n"
        "чтобы что-то внутри встало на своё место.\n\n"
        "Готов уделить время самому важному?\n"
        "Пройди путь из 4 шагов — от смерти до вечности.",
        reply_markup=keyboard
    )

@dp.callback_query_handler(text="step_1")
async def step_1(call: types.CallbackQuery):
    user_step[call.from_user.id] = 1

    # 2. РАЗНООБРАЗИЕ КНОПОК - вариант 1 для шага 1
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="🕯️ Досмотрел(а) до конца",
            callback_data="step_2"
        )
    )

    await call.message.answer(
        f"{get_progress_bar(1)}\n"
        "🕯️ *Что ждет душу в первые сутки после смерти?*\n\n"
        "• Момент, когда приходит ангел смерти\n"
        "• Последний шёпот шайтана\n"
        "• Вопросы в могиле: «Кто твой Господь?»\n\n"
        "⚠️ _Смотри до конца — последние минуты самые важные._",
        parse_mode="Markdown"
    )

    await bot.send_video(
        chat_id=call.message.chat.id,
        video=VIDEO_1
    )

    await call.message.answer(
        "Когда досмотришь — нажми кнопку ниже.",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query_handler(text="step_2")
async def step_2(call: types.CallbackQuery):
    if user_step.get(call.from_user.id) != 1:
        await call.answer("Сначала посмотри предыдущее видео.", show_alert=True)
        return

    user_step[call.from_user.id] = 2

    # 2. РАЗНООБРАЗИЕ КНОПОК - вариант 2 для шага 2
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🌍 Готов(а) увидеть знамения",
            callback_data="step_3"
        )
    )

    await call.message.answer(
        f"{get_progress_bar(2)}\n"
        "🌍 *Конец света: как это будет?*\n\n"
        "• Трубный глас, разрушающий миры\n"
        "• 10 признаков, которые уже сбываются\n"
        "• Великие знамения: Даджаль, Махди, Иса (мир ему)\n\n"
        "Это не фантастика. Это — обещанное.",
        parse_mode="Markdown"
    )

    await bot.send_video(
        chat_id=call.message.chat.id,
        video=VIDEO_2
    )

    await call.message.answer(
        "Когда досмотришь — нажми кнопку ниже.",
        reply_markup=keyboard
    )

    await call.answer()

@dp.callback_query_handler(text="step_3")
async def step_3(call: types.CallbackQuery):
    if user_step.get(call.from_user.id) != 2:
        await call.answer("Сначала пройди предыдущий шаг.", show_alert=True)
        return

    user_step[call.from_user.id] = 3

    await call.message.answer(
        f"{get_progress_bar(3)}\n"
        "⚖️ *День, когда всё откроется*\n\n"
        "• Книга дел в правой или левой руке\n"
        "• Мост Сират — тоньше волоса, острее меча\n"
        "• Весы, на которых взвешивается *каждая* мысль",
        parse_mode="Markdown"
    )

    await bot.send_video(
        chat_id=call.message.chat.id,
        video=VIDEO_3
    )

    # 2. РАЗНООБРАЗИЕ КНОПОК - вариант 3 для шага 3
    # и 3. ПЕРЕНОС ВОПРОСА ПОСЛЕ ВИДЕО
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="⚖️ Осознал(а) важность отчета",
            callback_data="step_3_watched"
        )
    )

    await call.message.answer(
        "Когда досмотришь видео — нажми кнопку ниже.",
        reply_markup=keyboard
    )

    await call.answer()

# Новый хендлер для подтверждения просмотра 3-го видео
@dp.callback_query_handler(text="step_3_watched")
async def step_3_watched(call: types.CallbackQuery):
    # 3. ВОПРОС О БЛИЗКИХ ПОСЛЕ ПРОСМОТРА
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            # 4. ИСПРАВЛЕНИЕ ДВОЕТОЧИЯ
            text="🤝 ПОДЕЛИТЬСЯ С БЛИЗКИМ ЧЕЛОВЕКОМ",
            switch_inline_query="Этот бот помог мне задуматься о самом важном. Посмотри, возможно, и тебе будет полезно. "
        ),
        types.InlineKeyboardButton(
            text="▶️ ПРОДОЛЖИТЬ СВОЙ ПУТЬ К ВЕЧНОСТИ",
            callback_data="step_4"
        )
    )

    await call.message.answer(
        "🤔 *После этого видео спроси себя:*\n"
        "«Кому из близких это сейчас нужно?»\n\n"
        "👥 *Кому ты хочешь отправить это напоминание?*\n\n"
        "После таких размышлений часто возникает образ\n"
        "человека, которому *сейчас особенно важно* это увидеть.\n\n"
        "Нажми кнопку ниже и выбери контакт —\n"
        "он получит личное сообщение от тебя.\n\n"
        "Если готов продолжить — жми вторую кнопку.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await call.answer()

@dp.callback_query_handler(text="step_4")
async def step_4(call: types.CallbackQuery):
    if user_step.get(call.from_user.id) != 3:
        await call.answer("Сначала пройди предыдущие шаги.", show_alert=True)
        return

    user_step[call.from_user.id] = 4

    await call.message.answer(
        f"{get_progress_bar(4)}\n"
        "🏁 *Финальный выбор: навечно*\n\n"
        "• Рай: то, чего не видел глаз и не слышало ухо\n"
        "• Ад: где один час мук равен 50 000 лет\n"
        "• Лицезрение Аллаха — высшая награда\n\n"
        "Это не сказка. Это — реальность,\nкоторая ждет каждого из нас.",
        parse_mode="Markdown"
    )

    await bot.send_video(
        chat_id=call.message.chat.id,
        video=VIDEO_4
    )

    # 5. КНОПКА ПОДТВЕРЖДЕНИЯ ПРОСМОТРА 4-го ВИДЕО
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🕋 Завершил(а) путь размышлений",
            callback_data="step_4_watched"
        )
    )

    await call.message.answer(
        "Когда досмотришь финальное видео — нажми кнопку ниже.",
        reply_markup=keyboard
    )

    await call.answer()

# Новый хендлер для подтверждения просмотра 4-го видео
@dp.callback_query_handler(text="step_4_watched")
async def step_4_watched(call: types.CallbackQuery):
    # 6. ФИНАЛЬНОЕ СООБЩЕНИЕ БЕЗ КНОПКИ "НАЧАТЬ ЗАНОВО"
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text="🕯️ Продолжить путь на канале «Towards Eternity»",
            url="https://t.me/TowardsEternity_RU"
        ),
        types.InlineKeyboardButton(
            text="🤝 Поделиться этим ботом с другими",
            switch_inline_query="Этот бот помог мне задуматься о самом важном. Посмотри, возможно, и тебе будет полезно. "
        )
    )

    await call.message.answer(
        "🕋 *Ты завершил путь размышлений*\n\n"
        "Теперь ты знаешь:\n"
        "✅ Что ждет после смерти\n"
        "✅ Как наступит Судный день\n"
        "✅ По каним весам будем судимы\n"
        "✅ Что выбираем навечно: Рай или Ад\n\n"
        "*Это знание — не для страха, а для действия.*\n"
        "Один намаз, одно доброе дело, один шаг к Аллаху\n"
        "меняют твою вечную участь.\n\n"
        "Если хочешь продолжить углубляться в эти темы,\n"
        "у нас есть канал с размышлениями о вечности.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

