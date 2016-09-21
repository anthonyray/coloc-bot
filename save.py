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

def extract_area(raw_description):
	pass

def extract_appartment_sharing(raw_description):
	raw_description = raw_description.lower()
	trigger = "coloc"
	negative_triggers = ["pas","refus","non"]
	positive_triggers = ["accept","ok","possible"]

	if trigger in raw_description:  # Coloc is mentionned. 
		neighboors = get_trigger_word_neighboring(raw_description, trigger)
		if sum( [any(neg_trigger in neighboor for neg_trigger in negative_triggers) for neighboor in neighboors]  ) > 0: # negative trigger words in neighboors -> NOT ACCEPTED:
			return "NOT_ACCEPTED"
		else:  # No negative triggers in neighboors
			if sum([any(pos_trigger in neighboor for pos_trigger in positive_triggers ) for neighboor in neighboors]) > 0: # There is positive triggers in neighboors
				return "ACCEPTED"
			else:
				return "UNKNOWN"
	else:
		return "UNKNOWN"


def get_trigger_word_neighboring(raw_description, trigger):
	trigger_index = raw_description.index(trigger)
	right_neighbors = raw_description[:trigger_index].split(" ")[-3:]
	left_neighbors = raw_description[trigger_index:].split(" ")[:3]

	return right_neighbors + left_neighbors

def extract_number_of_rooms(raw_description):
	pass

def vectorize_entry(raw_json_entry):
	url = raw_json_entry['url']
	raw_title = raw_json_entry["title"]
	raw_price = raw_json_entry["price_raw"]
	raw_description = raw_json_entry["description"]
	raw_date = raw_json_entry["date"]
	print raw_description

	date = extract_date(raw_date)
	price = extract_price(raw_price)
	appartment_sharing = extract_appartment_sharing(raw_description)

	print price
	


def save_entry_to_db(raw_json_entry):
	url = raw_json_entry["url"]
	raw_title = raw_json_entry["title"]
	raw_price = raw_json_entry["price_raw"]
	raw_description = raw_json_entry["description"]
	raw_date = raw_json_entry["date"]

	price = extract_price(raw_price)
	appartment_sharing = extract_appartment_sharing(raw_description)

	print raw_title
	print raw_price
	print raw_description
	print raw_date
	Appartment.get_or_create(url=url, defaults={'raw_title':raw_title, 'raw_date':raw_date, 'raw_description':raw_description, 'raw_price':raw_price, 'price':price, 'appartment_sharing': appartment_sharing})


def is_appartment_interesting(appartment):
	if (appartment.price <= 3600.0):
		return True
	else:
		return False


if __name__ == "__main__":
	apparts = get_json_from_file('data/run_results_05.json')["selection1"]
	
	map(save_entry_to_db, apparts) # Save new appartments

	for appartment in Appartment.select().where(Appartment.interesting_label == "UNKNOWN"): # We choose appartment that have not been labeled yet. 
		if (is_appartment_interesting(appartment)):
			appartment.interesting_label = "INTERESTING"
			appartment.save()
		else:
			appartment.interesting_label = "NOT_INTERESTING"
			appartment.save()



