import os
import requests
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup


myusername = input("Enter username: ")
mypassword = input("Enter password: ")
target = input("Enter target: ")
downloaded_count = 0

def opendriver():
    global driver_path
    driver_path = "Drivers/chromedriver.exe"
    global driver
    driver = webdriver.Chrome(driver_path)

def signin(myusername, mypassword):
    opendriver()
    driver.get(
        "https://www.instagram.com/accounts/login/?source=private_profile")
    sleep(3)
    username = driver.find_element_by_name('username')
    password = driver.find_element_by_name('password')
    login_button = driver.find_element_by_xpath(
        '//*[@id="loginForm"]/div/div[3]/button')
    username.send_keys(myusername)
    password.send_keys(mypassword)
    login_button.click()
    sleep(5)

def goto(url):
    driver.get(url)
    sleep(2)

def get_images(username):
	goto("https://www.instagram.com/{}/".format(username))
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	imgs = soup.find_all("img", attrs={"class": "FFVAD"})
	imgs_source = []
	for img in imgs:
		imgs_source.append(img['src'])
	return imgs_source

def download_image(img_url):
	global downloaded_count
	downloaded_count+=1
	response = requests.get(img_url)
	if not os.path.exists("Downloaded"):
		os.makedirs("Downloaded")
	file = open("Downloaded/image_{}.png".format(downloaded_count), "wb")
	file.write(response.content)
	file.close()

def download_images(images_link):
	for image_link in images_link:
		download_image(image_link)

def download(username):
	global myusername, mypassword
	signin(myusername, mypassword)
	images_link = get_images(username)
	download_images(images_link)

download(target)