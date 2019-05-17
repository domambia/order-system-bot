from app import app, db
from app.models import User, Text, Button, Admin, Order 
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, 
							CallbackQueryHandler,RegexHandler,ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from functools import wraps


# ================================================================
#GLOBAL VARIABLES
# ================================================================
# implements 
token 			             = "889640663:AAFor4Cvbn9oHcWZGHAdK1IvV05JLbu7iuw"
updater 		             = Updater(token = token)
dispatcher 		             = updater.dispatcher 

# Defining diffirent states 
INVITE_PHONE                 = 'invite_phone'
INVITE_COLLECTION            = 'invite_collection'
QUANTITY                     = 'quantity'
TIME                         = 'time'
INVITE_CONFIRM               = 'invite_confirm'
INVITE_SEND                  = 'invite_send'
INVITE_LOCATION              = 'invite_location'
END_CONVERSATION             = ConversationHandler.END

ORDER                        = 'order'
JOKE                         = 'joke'
NEW_CUSTOMER                 = 'new'
REVIEWS                      = 'reviews'
VARIETY                      = 'variety'
CUSTOMER_NAME                = 'customer_name'    
CUSTOMER_ID_NUMBER           = 'customer_id_number'
CUSTOMER_PHOTO               = 'customer_photo'
CUSTOMER_LINK                = 'customer_link'
CUSTOMER_LOCATION            = 'customer_location'
CUSTOMER_LOC                 = 'customer_loc'
CUSTOMER_SEND                = 'customer_send'


    
class Invitation(object):
    
    def __init__(self):
        self.store  = dict()
        
    def entry_point(self, bot, update):
        username  = update.message.chat.username
        self.store['username'] = username 
        msg  = "Thank you for choosing order invitation. Please enter your phone number, with your country's code area number"
        bot.send_message(chat_id  = update.message.chat_id, text  = msg)
        
        return INVITE_PHONE
    
    def invite_phone(self, bot, update):
        phone  = update.message.text
        self.store['phone'] = phone
        msg  = "Thank you. Please enter your desired collections. If your have a many, seperate them with commans."
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return INVITE_COLLECTION
    
    def invite_collection(self, bot, update):
        collection  = update.message.text
        msg = 'Thank you. Provide your desired quantity. It must be a number, for instance, 3.'
        self.store['collection'] = collection
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return QUANTITY
        
    
    def invite_quantity(self, bot, update):
        quantity = update.message.text
        print("Form Quantity",)        
        msg = "Thank you. Give your location. Your location must be a name. eg. Nairobi, Kenya."
        self.store['quantity'] = quantity
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return INVITE_LOCATION
    
    def invite_location(self, bot, update):
        location = update.message.text
        self.store['location'] = location
        msg   = "Please choose your arrival time bettern (10000hours and 0000hours). Eg 1120hours"
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return TIME 
    
    def invite_time(self, bot, update):
        time  = update.message.text  
        self.store['time'] = time
        phone       = self.store['phone']
        collection  = self.store['collection']
        location    = self.store['location']
        quantity    = self.store['quantity']
        time        = self.store['time']
        # show this to user
        msg = "Can we continue? (Reply with yes or no)"
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return INVITE_CONFIRM
    
    def invite_confirm(self, bot, update):
        phone       = self.store['phone']
        username    = self.store['username']
        collection  = self.store['collection']
        location    = self.store['location']
        quantity    = self.store['quantity']
        time        = self.store['time']
        # store
        order = Order(phone = phone, 
                username        = username,
                collections     = collection, 
                location        = location, 
                quantity        = quantity,
                time            = time)
        db.session.add(order)
        db.session.commit()
        msg  = "Thank you welcome back. Your order has been send for approval"
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return END_CONVERSATION
    
    
    def invite_send(self, bot, udpate):
        user        = update.message.username
        
        phone       = self.store['phone']
        collection  = self.store['collection']
        location    = self.store['location']
        quantity    = self.store['quantity']
        msg = """Invitation. for **{}** phone number **{}** collections **{}** whose location is **{}** and  quantity is {} needs approval"""
        bot.send_message(chat_id = udpate.message.chat_id, 
                         text = msg.format(user, phone, collection, location, quantity), 
                         reply_markup = ReplyKeyboardRemove())
        return END_CONVERSATION
    
    
    def cancel(self, bot, update):
        bot.send_message(chat_id = udpate.message.chat_id,  msg  = "Thank you. welcome again.")
        return END_CONVERSATION
    
    
    def invite_conversation(self):
        pass
       


class Customer():
    def __init__(self):
        self.store = dict()

    def new_customer(self, bot, update):
        username            = update.message.chat.username
        first_name          = update.message.chat.first_name
        # user                = User.query.filter(username  = username).first()
        # if user:
        #     msg  = "You are not a new customer. Please start your chat and go to other parts of the bot. from /start"
        #     bot.send_message(chat_id = update.message.chat_id, text  = msg)
        #     return END_CONVERSATION
        self.store['username'] = username
        self.store['first_name'] = first_name
        msg  = "Thank you. Please provide your second name."
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return  CUSTOMER_NAME

    def name(self, bot, update):
        self.store['last_name']  = update.message.text
        msg  = "Thank you. Please provide your id number."
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return CUSTOMER_ID_NUMBER

    def id_number(self, bot, update):
        id      = update.message.text 
        self.store['id'] = id 
        msg  = "Thank you.Please you. Please your photo."
        bot.send_message(chat_id = update.message.chat_id, text  = msg) 
        return  CUSTOMER_PHOTO

    def photo(self, bot, update):
        # print(update)
        photo  = "some photo is here"
        self.store['photo'] = photo 
        msg  = "Thank you for sharing the photo. Please share your facebook profile link"
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return CUSTOMER_LOCATION

    def location(self, bot, update): 
        print(update)
        self.store['link']   = update.message.text
        button = [[KeyboardButton("Share location", request_location = True)]]
        reply_markup = ReplyKeyboardMarkup(button)
        bot.send_message(chat_id = update.message.chat_id,
                         text = "Thank you. Please share your location", 
                         reply_markup = reply_markup)

        return CUSTOMER_LOC

    def save_location(self, bot, update):
        lat = update.message.location.latitude
        lon = update.message.locaton.longitude
        self.store['lat'] = lat 
        self.store['lon'] = lon 
        msg  = "Thank you for sharing your location.Please confirm your details. "
        bot.send_message(chat_id = update.message.chat_id, text  = msg, reply_markup = ReplyKeyboardRemove())
        return CUSTOMER_SEND

    def save_send(self, bot, update):
        last_name  = self.store['last_name']
        id         = self.store['id']
        photo      = self.store['photo']
        link       = self.store['link']
        lon        = self.store['lon']
        lat        = self.store['lat']
        msg  = "Thank you for registering with us. Wait for your details to be approved."
        bot.send_message(chat_id = update.message.chat_id, msg  = msg)
        return END_CONVERSATION

    def cancel(self, bot, update):
        bot.send_message(chat_id = udpate.message.chat_id,  msg  = "Thank you. welcome again.")
        return END_CONVERSATION

customer  = Customer()
customer_handler  = ConversationHandler(
    entry_points = [CommandHandler('register', customer.new_customer)],
    states = {
        CUSTOMER_NAME: [MessageHandler(Filters.text, customer.name)],
        CUSTOMER_ID_NUMBER: [MessageHandler(Filters.text, customer.id_number)],
        CUSTOMER_PHOTO: [MessageHandler(Filters.photo, customer.photo)],
        CUSTOMER_LOCATION: [MessageHandler(Filters.text, customer.location)],
        CUSTOMER_LOC: [MessageHandler(Filters.location, customer.save_location)],
        CUSTOMER_SEND: [MessageHandler(Filters.text, customer.save_send)],
    },
    fallbacks=[CommandHandler('cancel', customer.cancel)]
)
dispatcher.add_handler(customer_handler)
 
invite  = Invitation()

invitation_handler  = ConversationHandler(
    entry_points = [CommandHandler('invite', invite.entry_point)],
    states = {
        INVITE_PHONE: [MessageHandler(Filters.text, invite.invite_phone)],
        INVITE_COLLECTION: [MessageHandler(Filters.text, invite.invite_collection)],
        QUANTITY: [MessageHandler(Filters.text, invite.invite_quantity)],
        INVITE_LOCATION: [MessageHandler(Filters.text, invite.invite_location)],
        TIME: [MessageHandler(Filters.text, callback = invite.invite_time)],
        INVITE_CONFIRM: [MessageHandler(Filters.text, callback = invite.invite_confirm)],
        INVITE_SEND: [MessageHandler(Filters.text, callback = invite.invite_send)],
    },
    fallbacks=[CommandHandler('cancel', invite.cancel)]
)
dispatcher.add_handler(invitation_handler)
 
def start_menu_callback(bot, update):
	query = update.callback_query
	if query.data == "new_customer":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Welcome to Order SystemPlease register with us by entering  /register and answer some questions.", 
                        message_id  = query.message.message_id)
	elif query.data == "order":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Please enter input /invite to continue to the order menu", message_id  = query.message.message_id)
	elif query.data == "joke":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Please enter input /text to continue to the order menu", message_id  = query.message.message_id)
	elif query.data == "variety":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)
	elif query.data == "reviews":
		bot.edit_message_text(chat_id = query.message.chat_id, text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)
  
        
start_menu_callback_handler = CallbackQueryHandler(start_menu_callback)
dispatcher.add_handler(start_menu_callback_handler)
        
"""
Start"""
def start(bot, update):
	msg = "Welcome to Order System @ordersystem bot, for deliver quality services."
	button= [[InlineKeyboardButton('Authentication of New customer', callback_data = 'new_customer')],
	[InlineKeyboardButton("Joke", callback_data = 'joke'), 
	InlineKeyboardButton("Reviews", callback_data="reviews"), 
	InlineKeyboardButton("Order",  callback_data="order")], 
	[InlineKeyboardButton("Variety Channel", callback_data = 'variety')]]
	reply_markup = InlineKeyboardMarkup(button)
	bot.send_message(chat_id  = update.message.chat_id, text = msg,reply_markup = reply_markup)
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
