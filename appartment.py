from peewee import *
import datetime

db = SqliteDatabase('lbc.db')

class Appartment(Model):
	url = CharField(primary_key=True)
	creation_date = DateTimeField(default=datetime.datetime.now)

	raw_title = CharField()
	raw_date = CharField()
	raw_price = CharField()
	raw_description = CharField()

	price = FloatField(default=0.0)
	posted = BooleanField(default=False)

	appartment_sharing = CharField(default="UNKNOWN")

	interesting_label = CharField(default="UNKNOWN")
	

	class Meta:
		database = db
