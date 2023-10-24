import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(massage):
	sti = open('welcome/dart.jpg', 'rb')
	bot.send_sticker(massage.chat.id, sti)


	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton("Рандомное число")
	item2 = types.KeyboardButton("Как дела?")

	markup.add(item1, item2)

	bot.send_message(massage.chat.id,"Приветствую,{0.first_name}!\n Я- <b>{1.first_name}</b>,\n Меня создал, мой царь и Бог,\n Всемогущий Никитос! 😆".format(massage.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup)

#@bot.message_handler(func=lambda message: True)
@bot.message_handler(content_types=['text'])
#def echo_all(message):
def send_echo(massage):
	if massage.chat.type == 'private':
		if massage.text == 'Рандомное число':
			bot.send_message(massage.chat.id, str(random.randint(0,100)))
		elif massage.text == 'Как дела?':

			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
			item2 = types.InlineKeyboardButton("Плохо", callback_data='bad')

			markup.add(item1, item2)


			bot.send_message(massage.chat.id, 'Отлично, сам как?', reply_markup=markup)
		else:
			bot.send_message(massage.chat.id, 'Сорян,не могу ничего ответить.')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'good':
				bot.send_message(call.message.chat.id, 'Вот и отлично  🙃 ')
			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'Бывает 😕')

			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Как дела?', 
				reply_markup=None)
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
				text="Крепись :)")
			
	except Exception as e:
		print(repr(e))
	



bot.polling()