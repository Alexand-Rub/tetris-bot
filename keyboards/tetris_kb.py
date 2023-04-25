from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class TetrisAction(CallbackData, prefix='tetris'):
    action: str
    direction: Optional[str]


def start() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Начать игру',
        callback_data=TetrisAction(action='start')
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def joystick() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='⬅️',
        callback_data=TetrisAction(
            action='shift',
            direction='left'
        )
    )
    kb.button(
        text='➡️️',
        callback_data=TetrisAction(
            action='shift',
            direction='right'
        )
    )
    kb.button(
        text='⬅️',
        callback_data=TetrisAction(
            action='rotation',
            direction='left'
        )
    )
    kb.button(
        text='➡️️',
        callback_data=TetrisAction(
            action='rotation',
            direction='right'
        )
    )
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
