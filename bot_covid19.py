import requests
from bs4 import BeautifulSoup

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token='5989915776:AAG709kHNQBFJ3mV8ziKmYL0-SYrLGdjw1A',
          parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def start_help(msg: types.Message):
    text = """Привет!\nЭтот бот умеет отправлять статистику по COVID-19\U0001F9A0\n\n\
Чтобы получить статистику, введите название страны на английском"""
    await msg.answer(text)
    # await msg.answer(msg.reply)
    # await bot.send_message(msg.from_user.id, msg.text)


@dp.message_handler(commands="countries")
async def echo_send(msg: types.Message):
    # print(msg)
    print(msg.text)
    await msg.answer(msg)


@dp.message_handler()
async def parser(msg: types.Message):
    print(msg.text)
    try:
        link = "https://www.worldometers.info/coronavirus/country/" + msg.text

        respons = requests.get(link).text

        soup = BeautifulSoup(respons, "lxml")

        block = soup.find_all("div", id="maincounter-wrap")

        coronavirus_cases = block[0].find("span").text.replace(",", " ")
        deaths = block[1].find("span").text.replace(",", " ")
        recovered = block[2].find("span").text.replace(",", " ")

        country = soup.find(
            "div", style="text-align:center;width:100%").text.strip()

        text = f"Статистика {country}\n\n<b>Случаев заражения</b>:  \
{coronavirus_cases}\n<b>Умерло</b>:  {deaths}\n<b>Выздоровело</b>:  {recovered}"
        await msg.answer(text)
    except:
        await msg.answer("неверный ввод")


# @dp.message_handler()
# async def echo_send(msg: types.Message):
    # print(msg)
    # print(msg.text)
    # await msg.answer(msg)


if __name__ == "__main__":
    print("===== bot online =====")
    executor.start_polling(dp, skip_updates=False)  # True