#!/usr/bin/env python
from selenium import webdriver
from lxml.cssselect import CSSSelector

import selenium.webdriver.support.ui as ui
import MySQLdb
import time

class MyDatabase:

    host = 'newsdb.quody.co'
    user = 'trinnus'
    password = 'TFMGXX4BXt5DAHwP'
    db = 'TripAdvisor'

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


def check_duplicate(db, hname):
	query = 'SELECT * from ta_hotel WHERE name=%s'
	params = (hname)
	x = db.queryp(query,params)
	if x:
		return True
	else:
		return False


def get_hotels(url):

	br = webdriver.PhantomJS('phantomjs')

	wait = ui.WebDriverWait(br,9)

	db = MyDatabase()

	br.get(url)

	hotels_url_sel = u'.hotels a'

	ta_hotels_button = br.find_element_by_css_selector(hotels_url_sel)
	ta_hotels_button.click()
	time.sleep(1)

	destination_id_tupl = get_id_from_table(db, 'destination_id', 'destination', url, 'tripadvisor_url_main')
	destination_id = destination_id_tupl[0].get('destination_id')


	#now for the ta_hotel table
	ta_hotel_listing_sel = u'.listing'
	ta_hotel_url_sel = u'.property_title'

	ta_hotel_class_sel = u'.sprite-ratings-gry'

	next_button_sel = u'.sprite-pageNext'
	ta_hotel_url = []
	ta_hotel_names = []
	DUPLICATE_ERR = False

	x=0
	while True:
		ta_hotel_class = []
		ta_hotel_name = []


		ta_hotel_listings = br.find_elements_by_css_selector(ta_hotel_listing_sel)

		for rowx in ta_hotel_listings:

			ta_hotel_name.append( rowx.find_element_by_css_selector(ta_hotel_url_sel).text )
			ta_hotel_names.append( rowx.find_element_by_css_selector(ta_hotel_url_sel).text )
			ta_hotel_url.append( rowx.find_element_by_css_selector(ta_hotel_url_sel).get_attribute("href") )


			try:
				ta_hotelx_class = rowx.find_element_by_css_selector(ta_hotel_class_sel)
				ta_hotel_class.append( ta_hotelx_class.get_attribute("alt") )
			except:
				ta_hotel_class.append( "no rating" )


		m=0
		for rowx in ta_hotel_listings:
			#check for duplicates
			duplicate = check_duplicate(db, ta_hotel_name[m])

			if not duplicate:
				try:
					params = (None, None, destination_id, ta_hotel_name[m], ta_hotel_class[m], None, None, ta_hotel_url[m])
					query = 'INSERT INTO ta_hotel VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
					db.insert_row(query, params)

				except:
					print "Error: restaurant not added to db"
			else:
				#DUPLICATE_ERR = True
				pass

			m+=1

		#check for more pages of reviews
		try:
			ta_more_button = br.find_element_by_css_selector(next_button_sel)
			ta_more_button.click()
			time.sleep(5)

		except:
			break

		print "hotel page"+str(x)
		x+=1


	ta_hotel_website_sel = ".test"
	ta_hotel_address_sel = ".standard_width .format_address"

	#print ta_hotel_url
	#if not DUPLICATE_ERR:
	n=0
	for urlx in ta_hotel_url:
		try:
			br.get(urlx)
			time.sleep(4)

			ta_hotel_address = br.find_element_by_css_selector(ta_hotel_address_sel).text
			ta_hotel_site_button = br.find_elements_by_css_selector(ta_hotel_website_sel)
			ta_hotel_site_button[1].click()
			time.sleep(3)

			handles = br.window_handles
			br.switch_to_window(handles[2]);

			hotel_site_url = br.current_url

			#print str(hotel_site_url)
			#print str(ta_hotel_address)
			query = "UPDATE ta_hotel SET website=%s, address=%s WHERE name=%s"
			params = (hotel_site_url, ta_hotel_address, ta_hotel_names[n])
			db.insert_row(query,params)

			print "updating hotel website + address..."
			br.close()
			br.switch_to_window(handles[1]);
		except:
			pass

		n+=1

	print "get_hotels() success!"

#get_restaurants('http://www.tripadvisor.co.uk/Tourism-g150807-Cancun_Yucatan_Peninsula-Vacations.html')
#get_hotels('http://www.tripadvisor.com/Tourism-g150812-Playa_del_Carmen_Yucatan_Peninsula-Vacations.html')
