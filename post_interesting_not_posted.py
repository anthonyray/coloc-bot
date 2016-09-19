 # coding: utf8 
import json
import codecs
from post_to_fb import *

from pprint import pprint
from appartment import *

if __name__ == "__main__":
	
	for appartment in Appartment.select().where(Appartment.interesting_label == "INTERESTING", Appartment.posted == False): # We choose appartment that are interesting and not yet posted
		post_appartment_to_fb(appartment.raw_title, appartment.price, appartment.url)
		



