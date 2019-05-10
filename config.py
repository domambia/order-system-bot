import os 
"""
Config class to hold all file configurations
"""

class Config(object):
	SQLALCHEMY_DATABASE_URI='mysql://root:root@localhost/order-system'
	SQLALCHEMY_TRACK_MODIFICATIONS=False
	DEBUG=True



