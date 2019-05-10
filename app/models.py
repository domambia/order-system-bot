from app import db 


class User(db.Model):
	id       	= db.Column(db.Integer, primary_key = True)
	username 	= db.Column(db.String(100), unique = True)
	first_name  = db.Column(db.String(200))
	link 		= db.Column(db.String(300))
	id_photo	= db.Column(db.String(200))
	is_user     = db.Column(db.Integer, default = 0)

	def __str__(self):
		return self.username


class Text(db.Model):
	id 			= db.Column(db.Integer, primary_key = True)
	text 		= db.Column(db.String(500))

	def __str__(self):
		return self.text

class Button(db.Model):
	id  		= db.Column(db.Integer, primary_key = True)
	name 		= db.Column(db.String(100))
	description = db.Column(db.String(500))

	def __str__(self):
		return self.name