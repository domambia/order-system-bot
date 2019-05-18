from app import app, db
import telegram
from app.models import User, UserText, UserButton, Order 
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
CREATE_TEXT                  = "create_text"
DELETE_TEXT                  = "delete_text"
CREATE                       = 'create'
DELETE_TEXT                  = 'delete_text'
MANAGER                      = 751026322
SEND_WELCOME                 = 'send_welcome'
SEND_MESSAGE                 = 'send_message'

'''
Decorator to restrict authorizations'''
def permission_required(func):
	@wraps 
	def wrapped(update, context, *args, **kwargs):
		user_id = update.effective_user.id
		if user_id != MANAGER:
			print("Unauthorized access denied for {}.".format(user_id))
			return
			return func(update, context, *args, **kwargs)
		return wrapped

'''
=============================================================
The Order Invitation Abstraction
=============================================================
'''

class Invitation(object):
    
    def __init__(self):
        self.store  = dict()
        
    def entry_point(self, bot, update):
        username  = update.message.chat.username
        print(update)
        self.store[username] = {} 
        msg  = "Thank you for choosing order invitation. Please enter your phone number, with your country's code area number"
        bot.send_message(chat_id  = update.message.chat_id, text  = msg)
        
        return INVITE_PHONE
    
    def invite_phone(self, bot, update):
        phone       = update.message.text
        username    = update.message.chat.username
        self.store[username]['phone'] = phone
        msg  = "Thank you. Please enter your desired collections. If your have a many, seperate them with commans."
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return INVITE_COLLECTION
    
    def invite_collection(self, bot, update):
        collection  = update.message.text
        username    = update.message.chat.username
        msg = 'Thank you. Provide your desired quantity. It must be a number, for instance, 3.'
        self.store[username]['collection'] = collection
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return QUANTITY
        
    
    def invite_quantity(self, bot, update):
        quantity    = update.message.text 
        username    = update.message.chat.username
        msg = "Thank you. Give your location. Your location must be a name. eg. Nairobi, Kenya."
        self.store[username]['quantity'] = quantity
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return INVITE_LOCATION
    
    def invite_location(self, bot, update):
        location    = update.message.text
        username    = update.message.chat.username
        self.store[username]['location'] = location
        print(self.store)
        msg   = "Please choose your arrival time bettern (10000hours and 0000hours). Eg 1120hours"
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return TIME 
    
    def invite_time(self, bot, update):
        username    = update.message.chat.username
        time        = update.message.text  
        self.store[username]['time'] = time
        phone       = self.store[username]['phone']
        collection  = self.store[username]['collection']
        location    = self.store[username]['location']
        quantity    = self.store[username]['quantity']
        msg = (
            "```"
            
            "Are all the details correct? Reply with *yes* or *no**" 
            
            "```"
        )
        button= [
                [InlineKeyboardButton('Phone: {}'.format(str(phone)), callback_data = 'phone')],
                [InlineKeyboardButton("Collection: {}".format(str(collection)), callback_data = 'collection')],
                 [InlineKeyboardButton("Your Location: {}".format(str(location)),  callback_data="locale")], 
            [InlineKeyboardButton("Quantity: {}".format(str(quantity)), callback_data = 'value')], 
            [InlineKeyboardButton("Expected Time of Arrival: {}".format(str(time)), callback_data = 'time')]]
        reply_markup = InlineKeyboardMarkup(button)
        bot.send_message(chat_id  = update.message.chat_id, text = msg,
                         reply_markup = reply_markup, 
                         parse_mode  = telegram.ParseMode.MARKDOWN)
        return INVITE_CONFIRM
    
    def invite_confirm(self, bot, update):
        username    = update.message.chat.username
        phone       = self.store[username]['phone']
        collection  = self.store[username]['collection']
        location    = self.store[username]['location']
        quantity    = self.store[username]['quantity']
        time        = self.store[username]['time']
        if update.message.text.lower() == "yes":
            order = Order(phone = phone, 
                    username        = username,
                    collections     = collection, 
                    location        = location, 
                    quantity        = quantity,
                    time            = time)
            db.session.add(order)
            db.session.commit()
            # send to admin
            msg  = "Thank you welcome back. Your order has been send for approval"
            button= [
                [InlineKeyboardButton('Phone: {}'.format(str(phone)), callback_data = 'phone')],
                [InlineKeyboardButton("Collection: {}".format(str(collection)), callback_data = 'collection')],
                 [InlineKeyboardButton("Your Location: {}".format(str(location)),  callback_data="locale")], 
            [InlineKeyboardButton("Quantity: {}".format(str(quantity)), callback_data = 'value')], 
            [InlineKeyboardButton("Expected Time of Arrival: {}".format(str(time)), callback_data = 'time')], [InlineKeyboardButton("Ready for approval", callback_data = 'approval')]]
            reply_markup = InlineKeyboardMarkup(button)
            bot.send_message(MANAGER, text = msg,
                             reply_markup = reply_markup, 
                             parse_mode  = telegram.ParseMode.MARKDOWN)
            self.store.pop(username)
            return END_CONVERSATION
        
        msg  = "Thank you. You can start a making an order"
        self.store.pop(username)
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return END_CONVERSATION
    
    def invite_send(self, bot, udpate):
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

'''
====================================================
The Customer ConversationHandler Abstraction for the 
bot.
====================================================
'''       

class Customer():
    def __init__(self):
        self.store = dict()

    def new_customer(self, bot, update):
        username            = update.message.chat.username
        first_name          = update.message.chat.first_name
        self.store[username] = {}
        self.store[username]['first_name'] = first_name
        msg  = "Thank you. Please provide your second name."
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return  CUSTOMER_NAME

    def name(self, bot, update):
        self.store[update.message.chat.username]['last_name']  = update.message.text
        msg  = "Thank you. Please provide your id number."
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return CUSTOMER_ID_NUMBER

    def id_number(self, bot, update):
        id      = update.message.text 
        self.store[update.message.chat.username]['id'] = id 
        msg  = "Thank you.Please you. Please your photo."
        bot.send_message(chat_id = update.message.chat_id, text  = msg) 
        return  CUSTOMER_PHOTO

    def photo(self, bot, update):
        username = update.message.chat.username
        self.store[username]['photo'] = update.message.photo[-1].file_id
        print(self.store)
        msg  = "Thank you for sharing the photo. Please share your facebook profile link"
        bot.send_message(chat_id = update.message.chat_id, text  = msg)
        return CUSTOMER_LOCATION

    def location(self, bot, update): 
        username  = update.message.chat.username
        self.store[username]['link']   = update.message.text
        button = [[KeyboardButton("Share location", request_location = True)]]
        reply_markup = ReplyKeyboardMarkup(button)
        bot.send_message(chat_id = update.message.chat_id,
                         text = "Thank you. Please share your location", 
                         reply_markup = reply_markup)

        return CUSTOMER_LOC

    def save_location(self, bot, update):
        print("save Location")
        username    = update.message.chat.username
        self.store[username]['lat'] = update.message.location['longitude']
        self.store[username]['lon'] = update.message.location['latitude']
        last_name   = self.store[username]['last_name']
        first_name  = self.store[username]['first_name']
        id          = self.store[username]['id']
        link        = self.store[username]['link']
        msg  = "Thank you for sharing your location.Please confirm your details and respond with *yes* or *no*"
        bot.send_message(chat_id = update.message.chat_id, text  = msg, 
                         reply_markup = ReplyKeyboardRemove(), 
                         parse_mode  = telegram.ParseMode.MARKDOWN)
        return CUSTOMER_SEND

    def save_send(self, bot, update):
        username    = update.message.chat.username
        last_name   = self.store[username]['last_name']
        first_name  = self.store[username]['first_name']
        id          = self.store[username]['id']
        photo       = self.store[username]['photo']
        link        = self.store[username]['link']
        lon         = self.store[username]['lon']
        lat         = self.store[username]['lat']
        if update.message.text.lower() == "yes":
            msg  = "Thank you for registering with us. Wait for a details to be approved"
            print("Saved Data")
            print(self.store)
            user_available = User.query.filter(User.username == username).first()
            if user_available:
                bot.send_message(chat_id = update.message.chat_id, 
                                 text  = "Thank you. You are already our member. Please Continue to Ordering. Enter /start")
                return END_CONVERSATION
            user = User(username = username, chat_id = update.message.chat_id,
                        first_name = first_name, last_name = last_name,
                        lat=lat, lon = lon, link = link, photo =photo)
            db.session.add(user)
            db.session.commit()
            msg  = "Thank you. You have declined your registration. Welcome back again by entering /start."
            button= [
                [InlineKeyboardButton("Username: {}".format(str(username)), callback_data = 'user')],
                [InlineKeyboardButton("Id number: {}".format(str(id)), callback_data = 'id')],
                 [InlineKeyboardButton("Facebook Link: {}".format(str(link)),  callback_data="link")], 
            [InlineKeyboardButton("Latitude: {}".format(str(lat)), callback_data = 'loca_tion')],
                [InlineKeyboardButton("longititude:{}".format(lon), callback_data = 'loca_tion')],
                [InlineKeyboardButton("Customer for approval", callback_data = 'appr')]]
            reply_markup = InlineKeyboardMarkup(button)
            bot.send_message(chat_id = update.message.chat_id, text = "Thank you. Wait for approval.",
                             reply_markup = reply_markup, parse_mode  = telegram.ParseMode.MARKDOWN)
            bot.send_message(MANAGER, text = msg,
                             reply_markup = reply_markup, parse_mode  = telegram.ParseMode.MARKDOWN)
            
            return END_CONVERSATION
        return END_CONVERSATION

    def cancel(self, bot, update):
        bot.send_message(chat_id = udpate.message.chat_id,  msg  = "Thank you. welcome again.")
        return END_CONVERSATION

'''
====================================================
The Text ConversationHandler Abstraction for the 
bot.
====================================================
'''   

class Text(object):
    """
    The module allows the user of the bot to create buttons and text, change permissions
    Methods: 
            - entry --> Returns a message for where the user is prompted to give the output as yes or no.
            - create_init -->  This initializes the text creation process.
            - create -->  this create a text in the database.
            - delete --> this deletes a given text.
    """
    def __init__(self):
        """
        The Initializer of the module"""
        self.store = dict()
        
    def entry(self, bot, update):
        """
        Entry point to the text area conversation"""
        print("Text Coming Here")
        username  = update.message.chat.username
        self.store[username] = {}
        msg  = "Welcome to *Text*. Do you want to create a text?(*yes* or *no*)"
        bot.send_message(chat_id = update.message.chat_id, text  = msg, 
                         parse_mode  = telegram.ParseMode.MARKDOWN)
        
        return CREATE_TEXT
    
    def create_init(self, bot, update):
        username  = update.message.chat.username
        if update.message.text.lower() == "yes":
            print("Yes")
            msg  = "Thank your. Please provide your text"
            bot.send_message(chat_id = update.message.chat_id, text  = msg, 
                         parse_mode  = telegram.ParseMode.MARKDOWN)
            
            return CREATE
        
        msg  = "Thank you.Let us go to deleting part. Enter text to delete, *Enter some part of the text that you might remember.*"
        texts = UserText.query.all()
        if texts:
            inline_array = []
            for x in texts:
                inline_array.append(InlineKeyboardButton(str(x), callback_data=str(x)))
            keyboard_elements = [[element] for element in inline_array]
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_elements )
            bot.send_message(chat_id = update.message.chat_id, 
                             text  = msg, reply_markup = keyboard, 
                             parse_mode = telegram.ParseMode.MARKDOWN)
            return DELETE_TEXT

    def create(self, bot, update):
        print("Text Create")
        username = update.message.chat.username
        text = update.message.text
        self.store[username]['text'] = text
        if text:
            print("Text available")
            t  = UserText(text  = text, chat_id  = update.message.chat_id)
            db.session.add(t)
            db.session.commit()
            self.store.pop(username)
            texts = UserText.query.all()
            if texts:
                inline_array = []
                for x in texts:
                    inline_array.append(InlineKeyboardButton(str(x), callback_data=str(x)))
                keyboard_elements = [[element] for element in inline_array]
                keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_elements )
                msg = "Thank you creating a text. This are all texts"
                bot.send_message(chat_id = update.message.chat_id, 
                                 text  = msg, reply_markup = keyboard, 
                                 parse_mode = telegram.ParseMode.MARKDOWN)
            return END_CONVERSATION
        bot.send_message(chat_id = update.message.chat_id, text  = "Please provide a text")
        return CREATE
    
    def delete(self, bot, update):
        print("deleting text")
        user_text  = update.message.text
        text       = UserText.query.filter(text = user_text).all()
        print(text)
        if text:
            print("Am in")
            db.session.delete(text)
            db.session.commit()
            bot.send_message(chat_id = update.message.chat_id, text  =" Successfully delete text that is, o has *{}* as a part of the whole of it.".format(update.message.text), 
                             parse_mode  =telegram.ParseMode.MARKDOWN)
            return END_CONVERSATION
        
        bot.send_message(chat_id  = update.message.chat_id, text  = "Text Does Not exists. enter /setting")
        return END_CONVERSATION
    
    def cancel(self, bot, update):
        bot.send_message(chat_id = update.message.chat_id, text = "Thank you. Welcome again")
        return END_CONVERSATION

'''
=========================================================
Send Module Abstractions
=========================================================
'''   
class Send(object):
    def __init__(self):
        pass
    def welcome(self, bot, update):
        msg  = "Welcome To Sending messages. Write a message to send to everyone using the bot."
        bot.send_message(chat_id = update.message.chat_id,  text = msg)
        return  SEND_MESSAGE
        
    def send(self,bot, update):
        print("Welcome sending Message to Everyone")
        msg     = "Thank you message received by everyone."
        users   = User.query.all()
        if users:
            for user in users:
                print(user.chat_id)
                bot.send_message(chat_id  = user.chat_id, text  = update.message.text)
                bot.send_message(chat_id  = user.chat_id, text  = msg)
            return END_CONVERSATION
        
        bot.send_message(chat_id  = update.message.chat_id, text  = "You have now Registered Users in your bot")
        return END_CONVERSATION
    
    def cancel(self, bot, update):
        msg  = "Thank you for using sending message to everyone helper"
        bot.send_message(chat_id = update.message.chat_id, text = msg)
        return  END_CONVERSATION

'''
==========================================================
Buttons Abstraction Module.
==========================================================
'''
BUTTON_WELCOME              = 'button_welcome'
BUTTON_OPTION               = 'button_option'
BUTTON_CREATE               = 'button_create'
BUTTON_DELETE_OPT           = 'button_delete'

class Button(object):
    def __init__(self):
        pass
    
    def welcome(self, bot, update):
        msg  = "Welcome to Managing Buttons of the bot. Do you want to create a bot? *Yes* or *No*"
        bot.send_message(chat_id  = update.message.chat_id, text  = msg, 
                         parse_mode = telegram.ParseMode.MARKDOWN)
        return BUTTON_OPTION
    def option(self, bot, update):
        answer  = update.message.text
        if update.message.text.lower() == 'yes':
            print("creat button")
            msg   = "Thank you.Please provide the name of your buttons. And please a name for your button."
            bot.send_message(chat_id = update.message.chat_id, text = msg)
            return BUTTON_CREATE
        
        msg  = "Thank you. Continue to deleting section of buttons"
        bot.send_message(chat_id  = update.message.chat_id, text  = msg)
        
        return BUTTON_DELETE_OPT
    
    def create(self, bot, update):
        print("Yes Answer")
        text_name  = update.message.text.lower()
#        btns  = UserButton.query.filter(name == text_name).first()
#        print("Next")
#        if btns:
#            msg = "Thank you. A button with the same name already exists. Please use another name."
#            bot.send_message(chat_id = update.message.chat_id, text = msg)
#            return BUTTON_CREATE
        print("Creating Btn")
        btn = UserButton(name  = text_name, chat_id  = update.message.chat_id)
        db.session.add(btn)
        db.session.commit()
        bot.send_message(chat_id = update.message.chat_id, text ="Thank for you creating a button")
        return END_CONVERSATION
    
    def delet_option(self, bot, update):
        print("Buttons")
        buttons = UserButton.query.all()
        if buttons:
            inline_array = []
            for x in buttons:
                inline_array.append(InlineKeyboardButton(str(x), callback_data=str(x)))
            keyboard_elements = [[element] for element in inline_array]
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_elements )
            msg = "These are the available buttons. To delete one please enter the name as you it below and send it."
            bot.send_message(chat_id = update.message.chat_id, 
                             text  = msg, reply_markup = keyboard, 
                             parse_mode = telegram.ParseMode.MARKDOWN)

            return END_CONVERSATION
            
        msg  = "You don't have any button.Please Enter the name of your new button"
        bot.send_message(chat_id  = update.message.chat_id, text  = msg)
        return CREATE_BUTTON
    def cancel(self, bot, update):
        msg  = "Thank you for managing buttons. Welcome again."
        bot.send_message(chat_id  = update.message.chat_id, text  = msg)
        return END_CONVERSATION
        
        
        
        
    
'''
Sending everyone message Conversation Handler'''
btn  = Button()
btn_handler  = ConversationHandler(
    entry_points = [CommandHandler('button', btn.welcome)],
    states = {
        BUTTON_OPTION: [MessageHandler(Filters.text, btn.option)],
        BUTTON_CREATE: [MessageHandler(Filters.text, btn.create)],
        BUTTON_DELETE_OPT: [MessageHandler(Filters.text, btn.delet_option)],
    },
    fallbacks=[CommandHandler('cancel', btn.cancel)]
)
dispatcher.add_handler(btn_handler)
         
        
'''
Sending everyone message Conversation Handler'''
send  = Send()
msg_handler  = ConversationHandler(
    entry_points = [CommandHandler('send', send.welcome)],
    states = {
        SEND_MESSAGE: [MessageHandler(Filters.text, send.send)],
    },
    fallbacks=[CommandHandler('cancel', send.cancel)]
)
dispatcher.add_handler(msg_handler)
 
    
'''
The Text Conversation handler for the bot'''

text  = Text()
text_handler  = ConversationHandler(
    entry_points = [CommandHandler('text', text.entry)],
    states = {
        CREATE_TEXT: [MessageHandler(Filters.text, text.create_init)],
        DELETE_TEXT: [MessageHandler(Filters.text, text.delete)],
        CREATE: [MessageHandler(Filters.text, text.create)],
    },
    fallbacks=[CommandHandler('cancel', text.cancel)]
)
dispatcher.add_handler(text_handler)
        
'''
The New Customer handler for the bot'''

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
'''
The bot order invitation'''

invitation_handler  = ConversationHandler(
    entry_points = [CommandHandler('invite', invite.entry_point)],
    states = {
        INVITE_PHONE: [MessageHandler(Filters.text, invite.invite_phone)],
        INVITE_COLLECTION: [MessageHandler(Filters.text, invite.invite_collection)],
        QUANTITY: [MessageHandler(Filters.text, invite.invite_quantity)],
        INVITE_LOCATION: [MessageHandler(Filters.text, invite.invite_location)],
        TIME: [MessageHandler(Filters.text, invite.invite_time)],
        INVITE_CONFIRM: [MessageHandler(Filters.text, invite.invite_confirm)],
        INVITE_SEND: [MessageHandler(Filters.text, invite.invite_send)],
    },
    fallbacks=[CommandHandler('cancel', invite.cancel)]
)
dispatcher.add_handler(invitation_handler)
 

'''
The start menu--> It is diplayed when you enter the command /start. 
--> Shows also some text that describes the bot a bit.
--> This also handler Events(Callback Methods.)
'''
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
        bot.edit_message_text(chat_id = query.message.chat_id, text = "Welcome to go to the Statistics area /stats", message_id  = query.message.message_id)
    elif query.data == "permission":
        print("Clicked Permission")
    elif query.data == "text":
        bot.edit_message_text(chat_id = query.message.chat_id, text = "Welcome to go to the Text area please enter /text", message_id  = query.message.message_id)
    elif query.data == "button":
        bot.edit_message_text(chat_id = query.message.chat_id, text = "Welcome to go to the Button area please enter /button", message_id  = query.message.message_id)
    elif query.data == "send":
        bot.edit_message_text(chat_id = query.message.chat_id, text = "To send a message to everyone enter the command /send", message_id  = query.message.message_id)
        
start_menu_callback_handler = CallbackQueryHandler(start_menu_callback)
dispatcher.add_handler(start_menu_callback_handler)
        
    
"""
Start ---> Opens the start menus from where the user of the bot interacts with the bot."""

def start(bot, update):
	msg = "Welcome to Order System @ordersystem, for deliver of quality services."
	button= [[InlineKeyboardButton('Authentication of New customer', callback_data = 'new_customer')],
	[InlineKeyboardButton("Joke", callback_data = 'joke'), 
	InlineKeyboardButton("Reviews", callback_data="reviews"), 
	InlineKeyboardButton("Order",  callback_data="order")], 
	[InlineKeyboardButton("Variety Channel", callback_data = 'variety')]]
	reply_markup = InlineKeyboardMarkup(button)
	bot.send_message(chat_id  = update.message.chat_id, text = msg,reply_markup = reply_markup)
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)


"""
The settings part. It give the starting point for the administrator or somebody authorized to handler setting to access it and do settings
"""

#@permission_required
def settings(bot, update):
	msg = "Welcome to Order System @ordersystem, Settings"
	button= [[InlineKeyboardButton('Permission', callback_data = 'permission') ,InlineKeyboardButton("Text", callback_data = 'text')], 
	[InlineKeyboardButton("Buttons", callback_data="button")],
    [InlineKeyboardButton("send message to everyone", callback_data="send")]]
	reply_markup = InlineKeyboardMarkup(button)
	bot.send_message(chat_id  = update.message.chat_id, text = msg,reply_markup = reply_markup)
setting_handler = CommandHandler("setting", settings)
dispatcher.add_handler(setting_handler)

def stats(bot, update):
    cust = db.session.query(User).count()
    orders = db.session.query(Order).count()
    msg = "Order System Statitics"
    button= [[InlineKeyboardButton("Customers : {}".format(str(cust)), callback_data = 'cust')], 
             [InlineKeyboardButton("Orders: {}".format(str(orders)), callback_data="orders")],
             [InlineKeyboardButton("clicks: {}".format(str(23)), callback_data="click")]]
    reply_markup = InlineKeyboardMarkup(button)
    bot.send_message(chat_id  = update.message.chat_id, text = msg,reply_markup = reply_markup)
stats_handler = CommandHandler("stats", stats)
dispatcher.add_handler(stats_handler)



