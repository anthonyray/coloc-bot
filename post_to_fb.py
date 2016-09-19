# coding: utf8
import requests
from credentials import *

FB_API_ROOT_URL = "https://graph.facebook.com/v2.7/"
ME_FEED = "me/feed"

def post_appartment_to_fb(message, price, link_url):
	message = u"[{price} €] {message}".format(price=str(price), message=message)
	print message
 	#requests.post(FB_API_ROOT_URL+ME_FEED, data = {'access_token': ACCESS_TOKEN, 'message' : message, 'link':link_url })