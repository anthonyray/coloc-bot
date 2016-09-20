 # coding: utf8 
import json
import codecs
from post_to_fb import *

from pprint import pprint
from appartment import *

def get_json_from_file(filename):
	with codecs.open(filename,"r","utf-8") as data_file:
		return json.load(data_file, encoding="utf-8")

def extract_date(raw_date):
	""" 
	Examples : 
		- Hier, 18:36
		- 16 sept, 20:26
		- Urgent 10 sept, 17:15
	"""
	return raw_date

def extract_price(raw_price):
	"""
	Examples : 
		- 3 974 € C.C.
		- 3 400 € 
	"""
	euro_index = raw_price.index(u'€')
	refined_price = raw_price[:euro_index].strip(" ")
	refined_price = refined_price.replace(" ","")
	refined_price = float(refined_price)

	return refined_price


def vectorize_entry(raw_json_entry):
	url = raw_json_entry['url']
	raw_title = raw_json_entry["title"]
	raw_price = raw_json_entry["price_raw"]
	raw_description = raw_json_entry["description"]
	raw_date = raw_json_entry["date"]
	print raw_description

	date = extract_date(raw_date)
	price = extract_price(raw_price)

	print price
	


def save_entry_to_db(raw_json_entry):
	url = raw_json_entry["url"]
	raw_title = raw_json_entry["title"]
	raw_price = raw_json_entry["price_raw"]
	raw_description = raw_json_entry["description"]
	raw_date = raw_json_entry["date"]

	price = extract_price(raw_price)
	print raw_title
	print raw_price
	print raw_description
	print raw_date
	Appartment.get_or_create(url=url, raw_title=raw_title, raw_date=raw_date, raw_description=raw_description, raw_price=raw_price, price=price)


def is_appartment_interesting(appartment):
	if (appartment.price <= 3600.0):
		return True
	else:
		return False


if __name__ == "__main__":
	apparts = get_json_from_file('data/run_results_02.json')["selection1"]
	
	map(save_entry_to_db, apparts) # Save new appartments

	for appartment in Appartment.select().where(Appartment.interesting_label == "UNKNOWN"): # We choose appartment that have not been labeled yet. 
		if (is_appartment_interesting(appartment)):
			appartment.interesting_label = "INTERESTING"
			appartment.save()
		else:
			appartment.interesting_label = "NOT_INTERESTING"
			appartment.save()



