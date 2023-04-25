from asyncio import sleep

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.menu import menu, TetrisAction, nav

from tetris import Field

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Нажмите кнопку для начала игры',
        reply_markup=menu()
    )


@router.callback_query(TetrisAction.filter(F.action == "start"))
async def game(callback: CallbackQuery, callback_data: TetrisAction, state: FSMContext):
    await state.clear()
    field = Field()
    for time in range(2, -1, -1):
        await callback.message.edit_text('Игра начнётся через: {time}\n\n{field}'.format(
            time=time, field=field.get_field()
        ))
        await sleep(1)

    field.add()
    await state.update_data(field=field)
    await callback.message.edit_text(field.get_field(), reply_markup=nav())

    lose = True
    while lose:
        await sleep(1)
        data = await state.get_data()
        field = data['field']
        field.fly()
        field.win()
        lose = field.lose()
        await state.update_data(field=field)
        await callback.message.edit_text(field.get_field(), reply_markup=nav())


@router.callback_query(TetrisAction.filter(F.action == "move"))
async def move(callback: CallbackQuery, callback_data: TetrisAction, state: FSMContext):
    data = await state.get_data()
    field = data['field']
    match callback_data.type:
        case 'shift':
            field.move(direction=callback_data.direction)
        case 'rotation':
            field.rotate(direction=callback_data.direction)
    await state.update_data(field=field)
    await callback.message.edit_text(field.get_field(), reply_markup=nav())
