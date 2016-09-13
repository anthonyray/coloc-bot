from peewee import *

db = SqliteDatabase('lbc.db')

class Appartment(Model):
	url = CharField()
	raw_title = CharField()
	raw_date = CharField()
	raw_price = CharField()
	raw_description = CharField()

	class Meta:
		database = db # This model uses the "people.db" database.


db.connect()
db.create_tables([Appartment])