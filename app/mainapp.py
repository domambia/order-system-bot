from app import app 
from app.models import User, Text, Button 
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, 
							CallbackQueryHandler,RegexHandler,ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from app.orders import orders, start_order_handler
from functools import wraps


# ================================================================
 #GLOBAL VARIABLES
# ================================================================

# implements 
token 			= "889640663:AAFor4Cvbn9oHcWZGHAdK1IvV05JLbu7iuw"
updater 		= Updater(token = token)
dispatcher 		= updater.dispatcher 

LIST_MANAGAGERS = ['pyther_ke',] # this are ids
LIST_DIRECTORS  = ['pyther_ke',]

'''
==============================================================
Ranges to give the chances of Conversations
==============================================================
'''
# stich the menu option
ORDER, NEW, JOKE, REVIEWS, VARIETY, OPEN 		= range(6) 
## on send final stage

'''
=============================================================
Assigning permissions and restrictions decorators 
=============================================================
'''
# check if directors 
def restricted(func):
	@wraps 
	def wrapped(update, context, *args, **kwargs):
		user_id = update.effective_user.id
		if user_id not in LIST_OF_ADMINS:
			print("Unauthorized access denied for {}.".format(user_id))
			return
			return func(update, context, *args, **kwargs)
		return wrapped

'''
===============================================================
ORDER PARTS
===============================================================
'''
class Customer(object):
    pass



class Setting(object):
    pass 


class Button(object):
    pass



READ, UPDATE, DELETE, CREATE = range(4)

class Text(object):
    def welcome(self, bot, update):
        msg  = "You can create a new text by entering it down here, or skip by entering /skip"
        bot.send_message(chat_id  = update.message.chat_id, text = msg)
        
        return READ
    
    def read(self, bot, update):
        #texts = Text.query.all()
        # output all texts
        bot.send_message(chat_id = update.message.chat_id, 
                         text  = "This are the texts available")
        return CREATE
    
    
    def skip_read(self, bot, update):
        # skip the reading part
        bot.send_message(chat_id = update.message.chat_id, text = "Enter /skip the read part to skip")
        return CREATE
    
    
    def create(self, bot, update):
        get_text = update.message.text 
        #save 
        bot.send_message(chat_id = update.message.chat_id, 
                         text = "Please you can now update a text(By trying to match any in the existence) or Skip by entering /skip ")
        return UPDATE
    
    
    def skip_create(self, bot, update):
        msg  = "You never created any text"
        bot.send_message(chat_id = udpate.message.chat_id, text  = msg)
        
        return UPDATE
    
    def udpate(self, bot, update):
        get_text  = update.message.text
        #check if the some text simillar to this exist
        # update
        bot.send_message(chat_id  = update.message.chat_id, msg  = "Thank you. You can now delete any text by  trying to match an existing one or skip")
        
        return DELETE
    
    
    def skip_update(self, bot, update):
        msg  = "You never update any text"
        bot.send_message(chat_id = udpate.message.chat_id, text  = msg)
        
        return DELETE
    
    
    def delete(self, bot, udpate):
        get_text  = update.message.text 
        #check if exists
        #delete if exists
        bot.send_message(chat_id = update.message.chat_id, msg  = "Sucess you have deleted a text")
        return ConversationHandler.END
    
    
    
    def skip_delete(self, bot, update):
        msg  = "You never update any text"
        bot.send_message(chat_id = udpate.message.chat_id, text  = msg)
        
        return ConversationHandler.END
    
    def cancel(self, bot, udpate):
        msg  = "Thank for joining us. welcome bank again"
        bot.send_message(chat_id  = udapte.message.chat_id, text = msg)
        return ConversationHandler.END

'''
===============================================================
ORDER PARTS
===============================================================
'''

INVITE_PHONE = 'invite_phone'
INVITE_COLLECTION = 'invite_collection'
QUANTITY = 'quantity'
TIME = 'time'
CONFIRM = 'confirm'
SEND = 'CONFIRM'
INVITE_LOCATION = 'invite_location'
END_CONVERSATION = ConversationHandler.END


# Invitation

class Invitation(object):
    
#    def order(self, bot, update):
#        bot.send_message(chat_id  = update.message.chat_id, 
#                        text  = "Welcome. How are you doing?")
#        return INVITE

    def order_entry(self, bot, update):
        bot.send_message(chat_id = update.message.chat_id, 
                         text = "Thank you. Please provide your phone number.")
        return INVITE_PHONE 

    def phone(self, bot, update):
        phone  = update.message.text 
        #save phone
        msg  = "Please enter your collections"
        update.message.reply_text(msg)
        #bot.send_message(chat_id  = update.message.chat_id, text = msg)
        return INVITE_COLLECTON 

    def skip_phone(self, bot, udpate):
        msg = "please you Never Entered your phone number"
        bot.send_message(chat_id  = udapte.message.chat_id, text = msg)
        return INVITE_COLLECTON  

    def collection(self, bot, update):
        collection  = udpate.message.text 
        #save 
        update.message.reply_text("Please enter physical location for your shippment. enter /location to go to location and quantity and time")
        return INVITE_LOCATION 

    def skip_collection(self, bot, udpate):
        bot.send_message(chat_id  = udapte.message.chat_id, text = "You have skipped your collections")
        return INVITE_LOCATION

    def location(self, bot, udpate):
        location  = udpate.message.text 
        msg  = "Please enter the quantity of your collection"
        bot.send_message(chat_id  = udapte.message.chat_id, text = msg)
        return QUANTITY 

    def skip_location(self, bot, udpate):
        bot.send_message(chat_id  = udapte.message.chat_id, text = "You have skipped your collections")
        
        return QUANTITY



    def quantity(self, bot, update):
        msg  = "Please enter the quantity of your collection"
        bot.send_message(chat_id  = udapte.message.chat_id, text = msg)
        return TIME

    def skip_quantity(self, bot, update):
        msg  = "You haven't entered the quantity of your collection"
        bot.send_message(chat_id  = udapte.message.chat_id, text = msg)
        return TIME

    def time(self, bot, update):
        time = update.message.text 
        #save it 
        msg  = "Please Confirm details of your invations"
        confrim_buttons  = [['Confirm Your Invitation',], ['Send your Invitation to Manage']]
        reply_markup = InlineKeyboardButton(confrim_buttons)
        bot.send_message(chat_id  = update.message.chat_id, 
                         text = msg, 
                         reply_markup = reply_markup)
        return CONFIRM

    def invitation_confirm(sef, bot, update):
        # preview your items
        msg  = "Your are at one step to finish your inivation"
        bot.send_message(chat_id  = update.message.chat_id, text = msg, 
                         reply_markup=ReplyKeyboardRemove())
        return TIME 

        return LOCATION

    def send_invitation_to_manager(self, bot, update):
        # send to manger and also send to private group
        msg  = "Your Invation has been send for approval and wait to be added to a prvate group."
        bot.send_message(chat_id  = udapte.message.chat_id, text = msg)
        return ConversationHandler.END


    def cancel(self, bot, udpate):
        msg  = "Thank for joining us. welcome bank again"
        bot.send_message(chat_id  = udapte.message.chat_id, text = msg)
        return ConversationHandler.END
'''
The Customer 
'''



'''
TheConverstion Handlers 
'''
#instances 
invite  = Invitation()
text = Text()
# the invitation Conversation Handlers
invitation_handler  = ConversationHandler(
    entry_points = [CommandHandler('order', invite.order_entry)],
    states = {
        INVITE_PHONE: [MessageHandler(Filters.text, invite.phone)],
        INVITE_COLLECTION: [MessageHandler(Filters.text, invite.collection)],
        QUANTITY: [MessageHandler(filters = Filters.text, callback = invite.quantity)],
        INVITE_LOCATION: [MessageHandler(filters = Filters.text, callback = invite.location)],
        TIME: [MessageHandler(filters = Filters.text, callback = invite.time)],
        CONFIRM: [MessageHandler(filters = Filters.text, callback = invite.invitation_confirm)],
        SEND: [MessageHandler(filters = Filters.text, callback = invite.send_invitation_to_manager)],
    },
    fallbacks=[CommandHandler('cancel', invite.cancel)]
)
dispatcher.add_handler(invitation_handler)
#location_and_quantity_handler  = ConversationHandler(
#    entry_points = [CommandHandler('location', invite.location)],
#    states = {
#        QUANTITY: [MessageHandler(filters = Filters.text, callback = invite.quantity)],
#        TIME: [MessageHandler(filters = Filters.text, callback = invite.time)],
#        CONFIRM: [MessageHandler(filters = Filters.text, callback = invite.invitation_confirm)],
#        SEND: [MessageHandler(filters = Filters.text, callback = invite.send_invitation_to_manager)],
#    },
#    fallbacks=[CommandHandler('cancel', invite.cancel)]
#)
#dispatcher.add_handler(location_and_quantity_handler)

#the text handler
text_handler  = ConversationHandler(
    entry_points = [CommandHandler('text', text.welcome)],
    states = {
        CREATE: [MessageHandler(Filters.text, text.create),CommandHandler('skip', text.skip_create)],
        READ: [MessageHandler(filters = Filters.text, callback = text.read), 
                     CommandHandler('skip', text.skip_read)],
        UPDATE: [MessageHandler(filters = Filters.text, callback = text.skip_update), 
                     CommandHandler('skip', text.skip_update)],
        DELETE: [MessageHandler(filters = Filters.text, callback = text.delete),
                    CommandHandler('skip', text.skip_delete)
                ],
    },
    fallbacks=[CommandHandler('cancel', text.cancel)]
)
# adding to dispatcher
dispatcher.add_handler(text_handler)
# new customers handlers conversation




'''
================================================================
START Menu Applications
================================================================
'''
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


#handler of the start buttons
def start_menu_callback(bot, update):
	query = update.callback_query
	if query.data == "new_customer":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)

	elif query.data == "order":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Please enter input /order to continue to the order menu", message_id  = query.message.message_id)
	elif query.data == "joke":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Please enter input /text to continue to the order menu", message_id  = query.message.message_id)
	elif query.data == "variety":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)
	elif query.data == "reviews":
		bot.edit_message_text(chat_id = query.message.chat_id,text = "Thanks for choosing {}".format(query.data), message_id  = query.message.message_id)

start_menu_callback_handler = CallbackQueryHandler(start_menu_callback)
dispatcher.add_handler(start_menu_callback_handler)
