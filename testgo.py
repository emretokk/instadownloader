import requests
from datetime import datetime
from bs4 import BeautifulSoup

username,password = "emre.tok05","şevval52207+"
login_url = 'https://www.instagram.com/accounts/login/ajax/'
url = "https://www.instagram.com/p/COVSzBRprMf7ZmvQQO5XxL2-frbiNZIevfrJtU0/"


s = requests.Session()

response = s.get("https://www.instagram.com/", headers={"User-Agent":"ChromeDriver"})
csrf = response.cookies['csrftoken']

time = int(datetime.now().timestamp())
payload = {
		"username":username, 
		"enc_password":f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
		'queryParams': {},
    	'optIntoOneTap': 'false'
	}
header = {
	    "User-Agent": "ChromeDriver",
	    "x-csrftoken": csrf,
	    "X-Requested-With": "XMLHttpRequest",
    	"Referer": "https://www.instagram.com/accounts/login/",
	}

login_response = s.post(login_url, data=payload, headers=header)
cookies = login_response.cookies
cookie_jar = cookies.get_dict()

headers = {
	"User-Agent": "ChromeDriver",
	"x-csrftoken": cookie_jar['csrftoken'],
}

session = {
	"csrf_token": cookie_jar['csrftoken'],
    "session_id": cookie_jar['sessionid']
}

get_response = s.get(url, cookies=session, headers=headers)
soup = BeautifulSoup(get_response.content, 'html.parser')

print(type(get_response.content))

file = open("source.txt", "w")
file.write(soup.prettify())
file.close()

