from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_answers import LEXICON_ANSWERS

router = Router()


@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_ANSWERS['other_answer'])
