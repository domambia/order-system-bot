# Order System - (Telegram Bot)
- Permissions
- Menus 
- Settings 


## Commands 
1.  **/start** --> 
	show some welcoming text and then buttons below it.

## Menus 
- Menus below the **start text** --> 
									- Order
									- Reviews
									- Joke
									- Authentication of new Customer
									- Variety channel and 
									- open customers
- **N/B** --> In this bot buttons and text will be changing 

## Build a Customer verification Form
- The customers completes **some questionniares** and then sends it to the director
  for approval.
- The customer will be requested to **share location through menu button**
- Customer will send photocopy of id + slip 
- Send salafi 
- Send a profile link on Facebook
- Confirm details  and send them to the manager for approval.




## Build and Order system + Customers
1. Invitation
- The customer's phone number 
2. Delivery? pickup point
- Collection - skips the entry of a residential address
- Shipment - Passes to enter the physical address.

3. Quantity? - The customer to enter the quantity of the his/order
4. Choose arrival time of the shipment (10:00 - 00:00)
5. Give the Invitation Summary + Confirm Button for the customer --> store
	the order in database(order table) , **send the order tomanager for approval**

- After confirmations of the order a button to end Invitation(Invitation Recived)
 (+) send to group

- Button to update wating time (btn 10mins and two hours) + (send to customer
 the update through the bot)
- Cancel the order button[Message sent to the customer via bot] + send customer message via bot.

## Bot Settings 
- Create and delete Buttons
- Creating  and deleting texts
- Manage Orders option(closed/ open)
- View statistics (number of click on start bot, number of orders completed, number of verified customers).
- bot blocking to users(only authorized users can run)
- send a message to everyone (all users of the bot)


# System Desgin and Structuring 
**-----------------------------**

1. Create **permission** decorators for manager and directors
2. Create a customer Verification 
3. Create orders invitation by the customers
4. Create settings for the bot 

# Parts Remaining
1. Order - sending to Admin,
2. Customer - Send Salafi, get images and saving, send to admin.
