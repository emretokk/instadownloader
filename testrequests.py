import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime

username,password = "emre.tok05","şevval52207+"
base_url = 'https://www.instagram.com/'
login_url = 'https://www.instagram.com/accounts/login/?force_classic_login&hl=pl'
post_ajx_login_url = 'https://www.instagram.com/accounts/login/ajax/'
photo_details_url_tmpl = 'https://www.instagram.com/p/{0}/?__a=1' # in {0} goes the image code GET __a=1 - return only json
target_base_url = "https://www.instagram.com/emre.tok05/?__a=1"

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
accept_language = 'pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4'
content_type = 'application/x-www-form-urlencoded'

headers = dict()
ajx_headers = dict()
cookies = dict()

session = requests.Session()

def log_in(username, password):
	global headers
	global ajx_headers
	global cookies
	global session 
	time = int(datetime.now().timestamp())
	payload = {
		'username' : username,
		"enc_password" : f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
		'queryParams': {},
    	'optIntoOneTap': 'false'
	}
	# get unique csrftoken from server
	response = session.get(base_url, headers={"User-Agent": "user_agent"})
	prepare_request(response)

    # post request to login
	response = session.post(post_ajx_login_url, data=payload, headers=ajx_headers)
	prepare_request(response)
	return response

def prepare_ajax_request(request_response):
	global headers
	global ajx_headers
	global cookies
	global session
	ajx_headers = {
        'origin': base_url,
        'referer': request_response.url,
        'User-Agent': user_agent,
        'content-type': content_type,
        'accept-language': accept_language,
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'x-csrftoken': request_response.cookies['csrftoken'],
        'x-instagram-ajax': '1',
        'x-request-with': 'XMLHttpRequest'
    }

def prepare_request(response):
	global headers
	global ajx_headers
	global cookies
	global session
	headers = {
		'origin': base_url,
        'referer': response.url,
        'User-Agent': user_agent,
        'content-type': content_type,
        'accept-language': accept_language,
        'x-csrftoken': response.cookies['csrftoken'],
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	}
	cookies = response.cookies
	prepare_ajax_request(response)

def get_image_link(photo_code):
	global headers
	global ajx_headers
	global cookies
	global session
	#log in
	response = log_in(username, password)

	# get the post page url
	response = session.get(photo_details_url_tmpl.format(photo_code), headers=headers)
	prepare_request(response)

	# output to a file
	file = open("content.txt", "wb")
	file.write(response.content)
	file.close()

	# get the image url
	image_url = json.loads(response.content.decode('utf-8'))['graphql']['shortcode_media']['display_url']
	
	return image_url

def download(image_links):
	downloaded_count = 0
	if not os.path.exists("Download"):
		os.makedirs("Download")
	for image_link in image_links:
		downloaded_count+=1
		response = requests.get(image_link)
		file = open("Download/image_{}.png".format(downloaded_count), "wb")
		file.write(response.content)
		file.close()

def get_photo_codes():
	global headers
	global session
	response = log_in(username, password)
	print(response.status_code)
	prepare_request(response)

	response = session.get(target_base_url, headers=headers)
	prepare_request(response)
	soup = BeautifulSoup(response.content, 'html.parser')
	
	file = open("content.txt", "wb")
	file.write(response.content)
	file.close()
	
	print("COVSzBRprMf7ZmvQQO5XxL2-frbiNZIevfrJtU0" in str(response.text))
	print(response.status_code)


#image = download([get_image_link("COVSzBRprMf7ZmvQQO5XxL2-frbiNZIevfrJtU0")])
get_photo_codes()