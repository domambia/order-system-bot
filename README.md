# Customer Order System Bot
This is my first telegram chatbot that allows an esteemed customer to join the telegram  channel bot, and be able to provide of the information that is important for product delivery.
The **customer** is able to place an order and then wait for the manager's approval,after which the
the **product** is delivered. If the customer cancels his/her order then the **manager** is notified to stop the order. [Join channel](t.me/order_system_bot)

# Installation 
Let me guess that you want to try it locally, but not with my **token**, using yours that means a different **bot**

To install it, clone the project directly or using the link ```https://github.com/domambia/order-system-bot.git```, then follow  to run it locally.

## Create a virtual Environment and Activate it

```
$ python -m venv venv  # or virtaulenv -p python3 venv
$ source venv/bin/activate
```
## Install the requirements from ``` requirements.txt``` file
```
(venv)$ pip install -r requirements.txt 
```
## Database Migrations 
- This will allow you have the required database for the bot to function fully
```
(venv)$ flask db upgrade
```
## Run the bot
```
(venv)$ python run.py 
```

# Usage

To use some of the functionalities on this bot on your bot if you joined this or created new one and type the following commands.
```
/start 			#  starting menu 
/invite 		#  to acess only details about your order
/settings 		#  for **manager** settings about the order-system bot
/stats          # show the statistics of the bot
```

# Author
1. O.M. Dauglous

# Questions
- For more questions [email](omambiadauglous@gmail.com)

# Acknowledgment
My best spirit of learning new ideas daily and trying to represent anything i learn in a better way.

# Project Status 
This project is under development, please always make a ``` git pull ``` to get new updates

# Licence 
You may copy, distribute and modify the software provided that modifications are described and licensed for free under [New Rules](https"//google.com)
