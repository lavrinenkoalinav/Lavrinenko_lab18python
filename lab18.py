import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
import asyncio
import os

TOKEN = "7945351462:AAE6U6hWc9zE4SzZm9iDbLMmTcstD2ms9n8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

DATA_FILE = "notes.json"

# Завантаження/збереження нотаток
def load_notes():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Команди
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Вітаю! Це бот для нотаток. Напишіть /help для списку команд.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "/start - Почати роботу\n"
        "/help - Допомога\n"
        "/info - Про бота\n"
        "/exit - Завершити\n\n"
        "/addnote <текст> - Додати нотатку\n"
        "/shownotes - Показати всі нотатки\n"
        "/clearnotes - Очистити всі нотатки"
    )

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer("📝 Цей бот дозволяє зберігати, переглядати та очищати ваші нотатки.")

@dp.message(Command("exit"))
async def cmd_exit(message: types.Message):
    await message.answer("До зустрічі! Щоб повернутись, напишіть /start.")

@dp.message(Command("addnote"))
async def cmd_add_note(message: types.Message):
    note_text = message.text[9:].strip()
    if not note_text:
        await message.answer("❗ Будь ласка, додайте текст нотатки після команди.")
        return

    notes = load_notes()
    user_id = str(message.from_user.id)
    user_notes = notes.get(user_id, [])
    user_notes.append(note_text)
    notes[user_id] = user_notes
    save_notes(notes)

    await message.answer("✅ Нотатку додано!")

@dp.message(Command("shownotes"))
async def cmd_show_notes(message: types.Message):
    notes = load_notes()
    user_id = str(message.from_user.id)
    user_notes = notes.get(user_id, [])

    if not user_notes:
        await message.answer("📭 У вас поки немає нотаток.")
    else:
        formatted = "\n".join(f"{idx+1}. {note}" for idx, note in enumerate(user_notes))
        await message.answer(f"🗒 Ваші нотатки:\n{formatted}")

@dp.message(Command("clearnotes"))
async def cmd_clear_notes(message: types.Message):
    notes = load_notes()
    user_id = str(message.from_user.id)
    if user_id in notes:
        notes[user_id] = []
        save_notes(notes)
        await message.answer("🧹 Усі ваші нотатки видалено.")
    else:
        await message.answer("У вас немає нотаток для видалення.")

# Запуск бота
async def main():
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
