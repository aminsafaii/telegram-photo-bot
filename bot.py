import os
import json
import asyncio
from telegram import Bot
from datetime import datetime, timedelta


TOKEN = "8996786410:AAH8t-toh7ONOB4dcL4mkT6UslWuG58dpIo"
CHANNEL = "@grecu14fd"

bot = Bot(TOKEN)


DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "day": 0,
            "last_send": None
        }

    with open(DATA_FILE,"r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)


async def send_day(day):

    folder = f"photos/day{day}"

    if not os.path.exists(folder):
        return False


    for file in sorted(os.listdir(folder)):

        path = os.path.join(folder,file)

        if file.endswith((".jpg",".png",".jpeg")):

            await bot.send_photo(
                chat_id=CHANNEL,
                photo=open(path,"rb")
            )


    return True



async def main():

    while True:

        data = load_data()

        now = datetime.now()


        if data["last_send"] is None:

            ok = await send_day(data["day"])

            if ok:
                data["last_send"] = str(now)
                save_data(data)



        else:

            last = datetime.fromisoformat(
                data["last_send"]
            )

            if now-last >= timedelta(hours=24):

                data["day"] += 1

                ok = await send_day(data["day"])


                if ok:
                    data["last_send"] = str(now)
                    save_data(data)
                else:
                    break


        await asyncio.sleep(60)



asyncio.run(main())