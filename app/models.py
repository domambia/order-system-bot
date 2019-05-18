from app import db 


class User(db.Model):
    id       	= db.Column(db.Integer, primary_key = True)
    username 	= db.Column(db.String(100), unique = True)
    first_name  = db.Column(db.String(200))
    last_name   = db.Column(db.String(200))
    link 		= db.Column(db.String(300))
    photo		= db.Column(db.String(200))
    approved    = db.Column(db.Integer, default = 0)
    lon 		= db.Column(db.String(100))
    lat 		= db.Column(db.String(100)) 
    chat_id     = db.Column(db.Integer, default = 751026322)
    
    def __str__(self):
        return self.username
    
class Order(db.Model):
	id 			= db.Column(db.Integer, primary_key = True)
	username 	= db.Column(db.String(100))
	phone		= db.Column(db.String(20))
	collections	= db.Column(db.String(200))
	quantity 	= db.Column(db.String(12))
	location	= db.Column(db.String(100))
	time 		= db.Column(db.String(10))
    
class Admin(db.Model):
	id  		= db.Column(db.Integer,  primary_key = True)
	name 		= db.Column(db.String(100))
    
	def __str__(self):
		return name 


class UserText(db.Model):
    id 			= db.Column(db.Integer, primary_key = True)
    text 		= db.Column(db.String(500))
    chat_id     = db.Column(db.Integer)
    
    def __str__(self):
        return self.text

class UserButton(db.Model):
    id  		= db.Column(db.Integer, primary_key = True)
    name 		= db.Column(db.String(100))
    chat_id     = db.Column(db.Integer)

    def __str__(self):
        return self.name