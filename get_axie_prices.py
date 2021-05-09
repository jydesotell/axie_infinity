import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apscheduler.schedulers.blocking import BlockingScheduler

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import datetime


# Create driver
def create_driver(path='C:/Users/JSPAUN/Downloads/chromedriver_win32/chromedriver.exe', url='https://axieinfinity.com/'):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--disable-blink-features=AutomationControlled")

	driver = webdriver.Chrome(executable_path=path, options=chrome_options)  # Optional argument, if not specified will search path.

	# access axie infinity
	driver.get(url)

	time.sleep(5) # Wait for page to load

	return driver

def open_marketplace(driver):

	element = driver.find_element_by_link_text("Marketplace")
	element.click()

	time.sleep(15) # Wait for page to load

	driver.switch_to.window(driver.window_handles[-1])

	return driver

def get_price(driver):

	# Pull filters
	pull_dict = {
	'plant':'https://marketplace.axieinfinity.com/axie?part=tail-carrot&part=mouth-serious&part=horn-cactus&part=back-pumpkin&pureness=6',
	'bird':'https://marketplace.axieinfinity.com/axie?part=back-raven&part=mouth-hungry-bird&part=horn-kestrel&part=tail-post-fight&pureness=6',
	'beast':'https://marketplace.axieinfinity.com/axie?part=back-ronin&part=mouth-goda&part=horn-imp&part=tail-cottontail&pureness=6',
	'aqua':'https://marketplace.axieinfinity.com/axie?part=back-goldfish&part=mouth-risky-fish&part=horn-shoal-star&part=tail-navaga&pureness=6'
	}

	for key in pull_dict:
		url = pull_dict[key]
		driver.get(url)
		time.sleep(10) # Loading page
		axie_box = driver.find_elements_by_class_name('axie-card')
		price_list = []
		for box in axie_box:
			box_html = box.get_attribute('innerHTML')
			soup = BeautifulSoup(box_html, "lxml")
			for d in soup.findAll('h6',attrs={'class':'truncate ml-8 text-gray-1 font-medium'}):
				price_list.append(d.get_text())

		date_col = [datetime.datetime.now().strftime("%Y%m%d-%H%M")] * len(price_list)
		
		df = {'price':price_list, 'date':date_col}

		# print(df)

		# pd.DataFrame(df).to_csv(str(key)+'_'+str(datetime.datetime.now().strftime("%Y%m%d-%H%M"))+'.csv')

		df_master = pd.read_csv('data/'+key+'_master.csv')


		df_new = pd.DataFrame(df)


		df_master = df_master.append(df_new, ignore_index=True)


		df_master.to_csv('data/'+key+'_master.csv',index=False)

	return driver

def main():
	print('starting'+ str(datetime.datetime.now()))
	

	driver = create_driver(path='C:/Users/JSPAUN/Downloads/chromedriver_win32/chromedriver.exe', url='https://axieinfinity.com/')
	driver = open_marketplace(driver)
	driver = get_price(driver)
	driver.quit()
	print('finished')

if __name__ == "__main__":
	scheduler = BlockingScheduler()
	scheduler.add_job(main, 'interval', hours=.5)
	scheduler.start()
	# main()
