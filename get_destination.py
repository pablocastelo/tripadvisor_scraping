#!/usr/bin/env python
from selenium import webdriver
from lxml.cssselect import CSSSelector

import selenium.webdriver.support.ui as ui
import MySQLdb
import time


class MyDatabase:
	# Don't forget to add your credentials
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

	def __del__(self):
		self.connection.close()


def check_row_duplicate(db, url, tablename, colname):
	query = "SELECT * from "+str(tablename)+" where "+colname+"='"+str(url)+"'"
	x = db.query(query)
	if x:
		return True
	else:
		return False

def check_rating_duplicate(db, tablename, user, review_title):
	query = "SELECT * from "+str(tablename)+" where user='"+str(user)+"' AND review_title='"+str(review_title)+"'"
	x = db.query(query)
	if x:
		return True
	else:
		return False

def get_id_from_table(db, x_id, tablename, url, colname):
	query = "SELECT "+x_id+" from "+str(tablename)+" where "+colname+"='"+str(url)+"'"
	x = db.query(query)
	return x


def get_restaurant_urls(db, d_id):
	query = "SELECT ta_url from ta_restaurant where destination_id="+str(d_id)
	x = db.query(query)
	return x



def get_destination(url):

	br = webdriver.PhantomJS('phantomjs')

	wait = ui.WebDriverWait(br,9)

	db = MyDatabase()

	br.get(url)


	restaurant_url_sel = u'.restaurants a'
	country_sel = u'.breadcrumbs li:nth-child(1) span'
	short_desc_sel = u'.shortDescription'
	name_sel = u'#HEADING'
	hotels_url_sel = u'.hotels a'
	attraction_url_sel = u'.attractions a'
	forum_url_sel = u'.forum a'


	ta_name = br.find_element_by_css_selector(name_sel).text
	ta_country = br.find_element_by_css_selector(country_sel).text
	ta_short_desc = br.find_element_by_css_selector(short_desc_sel).text

	ta_restaurant_url = br.find_element_by_css_selector(restaurant_url_sel).get_attribute("href")
	ta_hotels_url = br.find_element_by_css_selector(hotels_url_sel).get_attribute("href")
	ta_attraction_url = br.find_element_by_css_selector(attraction_url_sel).get_attribute("href")
	ta_forum_url = br.find_element_by_css_selector(forum_url_sel).get_attribute("href")

	try:
		duplicate = check_row_duplicate(db, url, 'destination', 'tripadvisor_url_main')

		if not duplicate:
			params = (None, None, ta_name, ta_country, ta_short_desc, url, ta_restaurant_url, ta_hotels_url, ta_attraction_url, ta_forum_url)
			query = 'INSERT INTO destination VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
			db.insert_row(query, params)

	except:
		print "Error: url not added to db"

	ta_hotels_button = br.find_element_by_css_selector(hotels_url_sel)
	ta_attraction_button = br.find_element_by_css_selector(attraction_url_sel)
	ta_forum_button = br.find_element_by_css_selector(forum_url_sel)



	print "get_destination success!"

#get_destination('http://www.tripadvisor.co.uk/Tourism-g150807-Cancun_Yucatan_Peninsula-Vacations.html')
#get_destination('http://www.tripadvisor.com/Tourism-g150812-Playa_del_Carmen_Yucatan_Peninsula-Vacations.html')
