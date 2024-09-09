import telebot
from telebot import types
from web3 import Web3
from eth_account import Account
import requests
import langid

token = "YOUR_TOKEN"
bot = telebot.TeleBot(token)



addresses = []
private_keys = []


@bot.message_handler(commands=["start", "contact", "p", "voice to text"])
def start(message):
    if message.text == "/start":

        markup = types.InlineKeyboardMarkup(row_width=1)
        # btn_website = types.InlineKeyboardButton("Open Website", url="https://vgdl.ir/")
        # markup.add(btn_website)

        # bot.send_message(
        #     message.chat.id,
        #     "Click the button to open the website:",
        #     reply_markup=markup,
        # )
        chat_id = message.chat.id
        show_menu(chat_id)
    elif message.text == "/contact":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_website = types.InlineKeyboardButton("contact", url="https://t.me/Leo_nu4")
        markup.add(btn_website)

        bot.send_message(
            message.chat.id, "Click the button contact me :", reply_markup=markup
        )


@bot.message_handler(commands=["create"])
def create(message):
    try:
        # Ask the user for the number of addresses to create
        bot.send_message(message.chat.id, "How many addresses do you want to create?")

        # Register the process_count_input function as the next step handler
        bot.register_next_step_handler(message, count_input)

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


def count_input(message):
    try:
        # Check if the user's input is a valid number
        if message.text.isdigit():
            # Get the user's input and convert it to an integer
            count = int(message.text)

            for i in range(count):
                address = Web3().eth.account.create()
                addresses.append(address.address)
                private_keys.append(address._private_key.hex())

            save()
            create_file(message.chat.id)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number.")

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")


def save():
    global kol
    kol = [
        {"address": addr, "password": key} for addr, key in zip(addresses, private_keys)
    ]


def create_file(chat_id):
    try:
        file_name = "addresses_info"
        with open(f"{file_name}.docs", "w") as file:
            for entry in kol:
                file.write(
                    f"Address: {entry['address']}\nPrivate Key: {entry['password']}\n\n"
                )

        # Change the document extension to .doc
        bot.send_document(
            chat_id,
            open(f"{file_name}.docs", "rb"),
            caption="Here are your addresses and private keys.",
        )

    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")


def show_menu(chat_id):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("/start", "/create")
    keyboard.row("/contact")
   

    bot.send_message(chat_id, "Please select an item:", reply_markup=keyboard)

bot.polling()
