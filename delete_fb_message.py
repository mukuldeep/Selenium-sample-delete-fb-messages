from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

def is_available_by_xpath(driver,xpath,time_out):
	i=0
	while len(driver.find_elements_by_xpath(xpath))<=0:
		time.sleep(0.1)
		i=i+100
		if(time_out!=-1):
			if(i==time_out*1000):
				print("timeout(slow network): please wait")
				return -1
	return 0

def crw_fbbasic(url,l_url,user,pwd):
	options = Options()
	options.add_argument('--headless')
	#driver = webdriver.Firefox(options=options)
	driver = webdriver.Firefox()
	
	#logging in to fbbasic using provided username and password
	driver.get(l_url)
	em_in=driver.find_element_by_id('m_login_email')
	em_in.send_keys(user)
	pd_in=driver.find_element_by_xpath("//input[@name='pass']")
	pd_in.send_keys(pwd)
	sbm_in=driver.find_element_by_xpath("//input[@name='login']")
	sbm_in.submit()
	#might require manual verification so I,m adding 60 sec of sleep to verify , assuming that 60 sec is enough time for verification 
	#you may use automatic detection of verification using while(is_available_by_xpath(driver,X_PATH_FORMAT_HERE,10)==-1):
	time.sleep(60)
	
	#infinite loop
	while(1):
		#fetching message page
		driver.get(url)
		
		msg_list=[]#list to hold message urls
		elems = driver.find_elements_by_xpath("//a[@href]")#getting all urls from current page
		for elem in elems:#itterating over urls
			if(elem.get_attribute("href").startswith("https://mbasic.facebook.com/messages/read/?tid=cid.c.")):
				
				msg_list.append(elem.get_attribute("href"))#putting correct message url to list
				print(elem.get_attribute("href"))#printing the url
		#breaking the infinite loop, incase all messages has been deleted		
		if(len(msg_list)==0):
			break
		#else deleting one by one
		cc=0
		while(cc<len(msg_list)):#iterating over all the url in the list
			#opening message and clicking on delete
			driver.get(msg_list[cc])#opening url from list
			dlt_bnt=driver.find_element_by_xpath("//input[@name='delete']")#fetchinng delete button
			driver.execute_script("arguments[0].click();", dlt_bnt)#clicking it
			#time.sleep(3)
			while(is_available_by_xpath(driver,"//a[@class='bk bm']",10)==-1):#waiting for next page to load
				time.sleep(1)
			#
			eles = driver.find_elements_by_xpath("//a[@href]")#getting all urls from delete page
			for ele in eles:#finding correct confirm delete url from all urls i delete page
				if(ele.get_attribute("href").startswith("https://mbasic.facebook.com/messages/action/?mm_action=delete")):
					driver.get(ele.get_attribute("href"))#loading confirm deletion url
					break#delete is done so breaking from the loop
			cc=cc+1
			
			

url="https://mbasic.facebook.com/messages/"
l_url="https://mbasic.facebook.com/login/"
user="YOUR_USERNAME_OR_EMAIL_OR_PHONE_NO"
pwd="YOUR_PASSWORD"
crw_fbbasic(url,l_url,user,pwd)

