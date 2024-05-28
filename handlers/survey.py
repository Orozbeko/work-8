from config import database
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


survey_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary_or_grade = State()


@survey_router.message(Command("opros"))
async def start_survey(message: types.Message, state: FSMContext):
    await state.set_state(BookSurvey.name)
    await message.answer("Как вас зовут?")

@survey_router.message(BookSurvey.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.set_state(BookSurvey.age)
    await message.answer("сколько вам лет?")

@survey_router.message(BookSurvey.age)
async def process_age(message: types.Message, state:FSMContext):
    age = message.text
    await state.set_state(BookSurvey.occupation)
    await message.answer("чем вы увлекаетесь?")

@survey_router.message(BookSurvey.occupation)
async def process_occupation(message: types.Message, state:FSMContext):
    occupation = message.text
    await state.set_state(BookSurvey.salary_or_grade)
    if 18 <= BookSurvey.age <= 60:
        await message.answer("ваша зарплата?")
    elif 18 >= BookSurvey.age > 7:
        await message.answer('ваша средняя оценка?')
    else:
        await state.clear()

@survey_router.message(BookSurvey.salary_or_grade)
async def process_salary_or_grade(message: types.Message, state: FSMContext):
    salery_or_grade = message.text
    await message.answer(f"Спасибо за прохождение опроса, {message.from_user.full_name}!")
    await state.clear()


@survey_router.message(Command("stop"))
@survey_router.message(F.text.lower() == "стоп")
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за прохождение опроса!")