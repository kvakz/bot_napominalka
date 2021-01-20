import time
from threading import Thread
import telebot
from telebot import types

bot = telebot.AsyncTeleBot('token')

users = {}
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text='Начать', callback_data='LetsGo')
    keyboard.add(start_button)
    bot.send_message(message.chat.id, f'''Тевирп, {str(message.chat.first_name)}! Меня зовут Рич! Рад тебя видеть! Если нужно напомнить о чем-то, тыкни "Начать"''', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda  call: True)
def callback_worker(call):
    if call.data == 'LetsGo':
        bot.send_message(call.message.chat.id, 'О чем мне надо тебе напомнить?')

@bot.message_handler(content_types=['text'])
def get_message(message):
    alert = message.text
    chat_id = message.chat.id
    answer = f'{str(message.chat.first_name)}, Через сколько минут напомнить?'
    bot.send_message(message.chat.id, text=answer)
    bot.register_next_step_handler(message, get_time)
    users[chat_id] = [alert]

def get_time(message):
    timelaps = message.text
    chat_id = message.chat.id
    users[chat_id].insert(1, timelaps)
    while timelaps.isdigit() != True:
        bot.send_message(message.chat.id, 'Я умею обрабатывать только цифры :)')
        bot.register_next_step_handler(message, get_time)
        users[chat_id].pop() 
        break    
    else:
        check_in(message)

def check_in(message):
    chat_id = message.chat.id
    timelaps = users[chat_id][1]
    alert = users[chat_id][0]
    time.sleep(int(timelaps)*60)
    bot.send_message(message.chat.id, text=f'Кажется ты просил напомнить: {alert}')
    
bot.polling(none_stop=True, timeout=20)
