from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class TetrisAction(CallbackData, prefix='tetris'):
    action: str
    type: Optional[str]
    direction: Optional[str]


def menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Начать игру", callback_data=TetrisAction(action='start'))
    return kb.as_markup(resize_keyboard=True)


def nav() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="⬅️️",
        callback_data=TetrisAction(
            action='move',
            type='shift',
            direction='left'
        )
    )
    kb.button(
        text="➡️",
        callback_data=TetrisAction(
            action='move',
            type='shift',
            direction='right'
        )
    )
    kb.button(
        text="↪️",
        callback_data=TetrisAction(
            action='move',
            type='rotation',
            direction='left'
        )
    )
    kb.button(
        text="↩️",
        callback_data=TetrisAction(
            action='move',
            type='rotation',
            direction='right'
        )
    )
    return kb.as_markup(resize_keyboard=True)
