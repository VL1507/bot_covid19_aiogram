import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token='', parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def start_help(msg: types.Message):
    text = """Привет!\nЭтот бот умеет отправлять статистику по COVID-19\U0001F9A0\n\n\
Чтобы получить статистику, введите название страны на английском"""
    await msg.answer(text)
    #await bot.send_message(msg.from_user.id, "reply",reply_to_message_id=msg.message_id)
    

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

        country = soup.find("div", style="text-align:center;width:100%").text.strip()

        text = f"Статистика {country}\n\n<b>Случаев заражения</b>:  \
{coronavirus_cases}\n<b>Умерло</b>:  {deaths}\n<b>Выздоровело</b>:  {recovered}"
        await msg.answer(text)
    except:
        await msg.answer("неверный ввод")


if __name__ == "__main__":
    print("===== bot online =====")
    executor.start_polling(dp, skip_updates=False)  # True
