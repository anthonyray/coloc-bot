from peewee import *
from appartment import Appartment

db = SqliteDatabase('lbc.db')


if __name__ == "__main__":
	"""
	This script initializes the databases. 
	It create the Appartment database. 
	"""
	db.connect()
	db.create_tables([Appartment])
