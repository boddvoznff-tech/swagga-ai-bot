import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai = AsyncOpenAI(api_key=OPENAI_API_KEY)
SYSTEM = """Ты SWAGGA — харизматичная, загадочная и дружелюбная ИИ-гадалка.
Отвечай на русском языке, живо и разнообразно. Делай развлекательные расклады,
символические предсказания и гадания на любовь, деньги, удачу и выбор.
Не утверждай, что реально видишь будущее или обладаешь сверхъестественными силами.
Не давай опасных медицинских, юридических или финансовых указаний; в важных вопросах
напоминай, что гадание — развлечение, а решения нужно принимать по фактам.
Не повторяй один и тот же шаблон, если можно ответить оригинально. Обычно 2–5 абзацев.
"""

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("🔮 Добро пожаловать. Я SWAGGA — твоя ИИ-гадалка.\n\nЗадай вопрос о любви, деньгах, удаче или своей судьбе. Или напиши /help.")

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("✨ Просто напиши свой вопрос. Например: «Что меня ждёт на этой неделе?» или «Сделай расклад на любовь».")

@dp.message(F.text)
async def chat(message: Message):
    wait = await message.answer("🔮 Перемешиваю карты судьбы...")
    try:
        response = await ai.responses.create(
            model=MODEL,
            instructions=SYSTEM,
            input=message.text,
            max_output_tokens=450,
        )
        answer = response.output_text or "Карты пока молчат. Попробуй задать вопрос иначе."
        await wait.edit_text(answer)
    except Exception:
        logging.exception("AI request failed")
        await wait.edit_text("⚠️ Сейчас не получилось прочитать знаки. Попробуй чуть позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
