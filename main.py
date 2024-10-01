from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from hugchat import hugchat
from hugchat.login import Login

BOT_TOKEN = "7921078426:AAGE9AzemlTU6XeiopTCot18tudIk27IyAg"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

banworld = open("banword.txt", encoding='utf-8')
banworld_list = banworld.readlines()

admin_name = open("ADMIN_NAME", encoding='utf-8')
admin_name_list = admin_name.readlines()

ban_user_name = open("BAN_USER_NAME", encoding='utf-8')
ban_user_name_list = ban_user_name.readlines()

MAX_MATS = 5

users = {}

def AiDialog(user_input, email, passwork):
    sing = Login(email, passwork)

    cooke = sing.login()

    chat_bot = hugchat.ChatBot(cookies=cooke.get_dict())

    return chat_bot.chat(user_input)


#Просто выдаем сколько предупреждений у пользователя
@dp.message(Command(commands=["mats"]))
async def mats_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            "name": message.from_user.first_name,
            "mats": 0,
            "is_ban": False
        }
    await message.answer(f"Число пердупреждений: {users[message.from_user.id]['mats']}")


@dp.message(F.text)
async def filter_message(message: Message):

    is_mat_message = False

    #Если пользователя нет в списке то мы его добавляем по его id
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            "name": str(message.from_user.first_name),
            "mats": 0,
            "is_ban": False
        }
    #Если пользователь по какой-то причине не забанен то баним
    if users[message.from_user.id]["is_ban"]:
        await bot.ban_chat_member(message.chat.id, message.from_user.id)

    #Делаем админами людей из списка
    for admin_name_index in range(0, len(admin_name_list)):
        if users[message.from_user.id]["name"] == admin_name_list[admin_name_index]:
            await bot.promote_chat_member(message.chat.id, message.from_user.id, is_anonymous=True ,can_delete_messages=True, can_restrict_members=True)
    #Баним админами людей из списка
    for ban_user_name_index in range(0, len(ban_user_name_list)):
        if users[message.from_user.id]["name"] == ban_user_name_list[ban_user_name_index]:
            await bot.ban_chat_member(message.chat.id, message.from_user.id)


    # Делим сообщение на отдельные слова
    message_text = message.text.lower().split()

    #Убираем пробелы из сообщения
    full_message_text = message.text.replace(" ", "").lower()

    # Проверка на маты
    for a in range(0, len(message_text)):

        for i in range(0, len(banworld_list)):

            #Проверяем все слова по очереди или все слова вместе из сообщения на список матов
            if str(message_text[a]) + "\n" == banworld_list[i] or str(full_message_text) + "\n" == banworld_list[i]:

                #Если подошёл даем предупреждение
                users[message.from_user.id]["mats"] += 1

                #Костыль
                full_message_text = str()

                is_mat_message = True

                # Если предупреждений много баним
                if users[message.from_user.id]["mats"] >= MAX_MATS:
                    users[message.from_user.id]["is_ban"] = True
                    await bot.ban_chat_member(message.chat.id, message.from_user.id)

                #Пишем что выдали предупреждение
                await message.answer(f"Я выдаю предуприждение пользователю {message.from_user.first_name}\nЧисло предупреждений: {users[message.from_user.id]['mats']}")
                await message.delete()

                break

    if not is_mat_message:
        r = "" + AiDialog(str(message.text), "bratiya234@gmail.com", "Wede12345678900")
        print(1)
        await message.reply(r)

banworld.close()
admin_name.close()
ban_user_name.close()

if __name__ == "__main__":
    dp.run_polling(bot)