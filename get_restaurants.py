#!/usr/bin/env python
from selenium import webdriver
from lxml.cssselect import CSSSelector

import selenium.webdriver.support.ui as ui
import MySQLdb
import time

class MyDatabase:

	host = ''
	user = ''
	password = ''
	db = ''

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db,use_unicode=1,charset="utf8")
		self.cursor = self.connection.cursor()

	def insert_row(self, query, params):
	    try:
		    self.cursor.execute(query, params)
		    self.connection.commit()
	    except:
            self.connection.rollback()

	def query(self, query):
		cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
		cursor.execute(query)
		return cursor.fetchall()

	def queryp(self, query, params):
		cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
		cursor.execute(query, params)
		return cursor.fetchall()

	def __del__(self):
		self.connection.close()


def get_id_from_table(db, x_id, tablename, url, colname):
	query = "SELECT "+x_id+" from "+str(tablename)+" where "+colname+"='"+str(url)+"'"
	x = db.query(query)
	return x


def check_duplicate(db, d_id, ta_url):
	query = 'SELECT * from ta_restaurant WHERE destination_id=%s AND ta_url=%s'
	params = (d_id, ta_url)
	x = db.queryp(query,params)
	if x:
		return True
	else:
		return False


def get_restaurants(url):

	br = webdriver.PhantomJS('phantomjs')

	wait = ui.WebDriverWait(br,9)

	db = MyDatabase()

	br.get(url)

	restaurant_url_sel = u'.restaurants a'

	ta_restaurant_button = br.find_element_by_css_selector(restaurant_url_sel)
	ta_restaurant_button.click()
	time.sleep(1)

	destination_id_tupl = get_id_from_table(db, 'destination_id', 'destination', url, 'tripadvisor_url_main')
	destination_id = destination_id_tupl[0].get('destination_id')


	#now for the ta_restaurant table
	ta_restaurant_listing_sel = u'.listing'
	ta_restaurant_url_sel = u'.property_title'

	ta_rest_prices_sel = u'.price'
	ta_rest_cuisine_sel = u'.cuisine'
	next_button_sel = u'.sprite-pageNext'


	x=0
	while True:

		ta_restaurant_listings = br.find_elements_by_css_selector(ta_restaurant_listing_sel)

		for rowx in ta_restaurant_listings:

			ta_restaurant_url = rowx.find_element_by_css_selector(ta_restaurant_url_sel).get_attribute("href")
			ta_restaurant_name = rowx.find_element_by_css_selector(ta_restaurant_url_sel).text

			try:
				ta_rest_prices =  rowx.find_element_by_css_selector(ta_rest_prices_sel).text
			except:
				pass

			try:
				ta_rest_cuisine = rowx.find_element_by_css_selector(ta_rest_cuisine_sel).text
			except:
				pass

			#check for duplicates
			duplicate = check_duplicate(db, destination_id, ta_restaurant_url)

			if not duplicate:
				try:
					params = (None, None, unicode(destination_id), unicode(ta_restaurant_url), unicode(ta_restaurant_name), unicode(ta_rest_prices), unicode(ta_rest_cuisine), None, None, None)
					query = 'INSERT INTO ta_restaurant VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
					db.insert_row(query, params)

				except:
					print "Error: restaurant not added to db"
			else:
				pass

		#check for more pages of reviews
		try:
			ta_more_button = br.find_element_by_css_selector(next_button_sel)
			ta_more_button.click()
			time.sleep(6)

		except:
			break

		print "page"+str(x)
		x+=1


	print "get_restaurants() success!"

#get_restaurants('http://www.tripadvisor.co.uk/Tourism-g150807-Cancun_Yucatan_Peninsula-Vacations.html')
#get_restaurants('http://www.tripadvisor.com/Tourism-g150812-Playa_del_Carmen_Yucatan_Peninsula-Vacations.html')
