 # coding: utf8 
import json
import codecs
from post_to_fb import *

from pprint import pprint
from appartment import *


def is_appartment_interesting(appartment):
	if (appartment.price <= 3600.0):
		return True
	else:
		return False


if __name__ == "__main__":

	print "STARTING"
	print "----------------------------------------"
	for appartment in Appartment.select().where(Appartment.interesting_label == "INTERESTING"): # We choose appartment that have not been labeled yet. 
		
		print "------------------------------------"
		print appartment.raw_title
		print str(appartment.price) + u"€"
		print appartment.raw_description
		
		user_input = raw_input("Interesting ? (y/n) ")

		if (user_input[0].lower() == "y"):
			appartment.interesting_label = "INTERESTING"
			appartment.save()
		else:
			appartment.interesting_label = "NOT_INTERESTING"
			appartment.save()

	print "----------------------------------------"
	print "DONE"

