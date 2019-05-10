from app import app 
from app.models import User, Text, Button 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

token 			= "889640663:AAFor4Cvbn9oHcWZGHAdK1IvV05JLbu7iuw"
'''
Update object
'''
updater  		= Updater(token  = token)
#dispatcher
dispatcher 		= updater.dispatcher
'''
Start Command
'''

'''

{"ok":true,"result":[{"update_id":685677420,
"message":{"message_id":2,"from":{"id":751026322,"is_bot":false,"first_name":"pyther_ke","username":"pytherke","language_code":"en"},"chat":{"id":751026322,"first_name":"pyther_ke","username":"pytherke","type":"private"},"date":1557480543,"text":"fuck yourself"}},{"update_id":685677421,
"message":{"message_id":3,"from":{"id":751026322,"is_bot":false,"first_name":"pyther_ke","username":"pytherke","language_code":"en"},"chat":{"id":751026322,"first_name":"pyther_ke","username":"pytherke","type":"private"},"date":1557480545,"text":"today"}},{"update_id":685677422,
"message":{"message_id":4,"from":{"id":751026322,"is_bot":false,"first_name":"pyther_ke","username":"pytherke","language_code":"en"},"chat":{"id":751026322,"first_name":"pyther_ke","username":"pytherke","type":"private"},"date":1557480550,"text":"i wil teach you"}}]}

'''
def start(bot, update):
	msg = "Welcome to Order System @ordersystem bot, for deliver quality services."
	button= [[InlineKeyboardButton('Authentication of New customer', callback_data = 'new_customer')],
	[InlineKeyboardButton("Joke", callback_data = 'joke'), 
	InlineKeyboardButton("Reviews", callback_data="reviews"), 
	InlineKeyboardButton("Order",  callback_data="order")], 
	[InlineKeyboardButton("Variety Channel", callback_data = 'variety')]]
	reply_markup = InlineKeyboardMarkup(button)
	bot.send_message(chat_id  = update.message.chat_id,text = msg)
	bot.send_message(chat_id  = update.message.chat_id, text = "Choose your options from this below.",reply_markup = reply_markup)
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

"""
Authentication of New Customer
"""
def username_first_name(update):
	username  	= update.message.username
	first_name  = update.message.first_name   
	user  = User.query.filter(User.username == username).first()
	if user:
		return False 
	else:
		new_user  = User(username = username, first_name  = first_name)
		db.session.add(new_user)
		db.session.commit()
		return True
def save_link(update):
	username  = update.message.username
	user = User.query.filter(User.username == username)
	msg  = udpate.message.text 
	if msg.startwith('http'):
		return msg 
	else:
		msg  = None 
	user.link  = msg
	db.session.commit() 

def save_photo(update):
	username  = update.message.username
	user = User.query.filter(User.username == username)

"Handle the start-menus"
def start_menu_callback(bot, update):
	query = update.callback_query
	print(query) 
	if query.data == "new_customer":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)

	elif query.data == "order":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)
	elif query.data == "joke":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)
	elif query.data == "variety":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)
	elif query.data == "reviews":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)

start_menu_callback_handler = CallbackQueryHandler(start_menu_callback)
dispatcher.add_handler(start_menu_callback_handler)


