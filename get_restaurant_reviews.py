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


def check_row_duplicate(db, url, tablename, colname):
	query = "SELECT * from "+str(tablename)+" where "+colname+"='"+str(url)+"'"
	x = db.query(query)
	if x:
		return True
	else:
		return False

def check_rating_duplicate(db, user, review_title):
	rt = review_title.replace("'", "\\'")
	rt = rt.replace('"', '\\"')
	rt = unicode(rt).encode('utf-8')
	query = 'SELECT * from ta_rest_review WHERE user=%s AND review_title=%s'
	params = (user, rt)
	x = db.queryp(query,params)
	if x:
		return True
	else:
		return False

def get_id_from_table(db, x_id, tablename, url, colname):
	query = "SELECT "+x_id+" from "+str(tablename)+" where "+colname+"='"+str(url)+"'"
	#query = "SELECT destination_id from destination where tripadvisor_url_main=%s"
	#params = (x_id, str(tablename), colname, str(url))
	#print params
	#x = db.queryp(query, params)
	x = db.query(query)
	return x

#def get_id_from_table(db, x_id, tablename, url, colname):
	#query = "SELECT "+x_id+" from "+str(tablename)+" where "+colname+"='"+str(url)+"'"
	#x = db.query(query)
	#return x

def get_restaurant_urls(db, d_id):
	query = "SELECT ta_url from ta_restaurant where destination_id="+str(d_id)
	x = db.query(query)
	return x


def get_reviews(url):
	br = webdriver.PhantomJS('phantomjs')

	wait = ui.WebDriverWait(br,9)

	db = MyDatabase()

	br.get(url)


	destination_id_tupl = get_id_from_table(db, 'destination_id', 'destination', url, 'tripadvisor_url_main')
	destination_id = destination_id_tupl[0].get('destination_id')


	#Now to scrape all of the restaurant reviews
	rest_url_tupl = get_restaurant_urls(db, destination_id)
	#print rest_url_tupl


	for colx in rest_url_tupl:

		restx_url = colx.get('ta_url')
		restaurant_id_tupl = get_id_from_table(db, 'ta_restaurant_id', 'ta_restaurant', restx_url, 'ta_url')
		#print restaurant_id_tupl


		restaurant_id = restaurant_id_tupl[0].get('ta_restaurant_id')
		br.get(restx_url)

		ta_restreview_listing_sel = u'.reviewSelector'
		ta_restreview_user_sel = u'.scrname'
		ta_restreview_usertitle_sel = u'.reviewerTitle'
		ta_restreview_city_sel = u'.location'
		ta_restreview_revtitle_sel = u'.noQuotes'
		ta_restreview_ratedate_sel = u'.ratingDate'
		ta_restreview_visitdate_sel = u'.recommend-titleInline'
		#ta_restreview_visitdate_sel = u'.rating-list ul li span'
		ta_restreview_rating_sel = u'.rating_s img'
		ta_restreview_revbody_sel = u'.entry'
		ta_restreview_ratingVASF_sel = u'.recommend img'

		ta_restreview_more_button_sel = u'.moreLink'
		next_button_sel = u'.sprite-pageNext'

		x=1
		REVIEW_ERROR = False

		#the while loop is for multiple pages of reviews, leave commented out to scrape just the first page
		#while True:
		ta_restreviewx_userx = []
		ta_restreviewx_usertitlex = []
		ta_restreviewx_cityx = []
		ta_restreviewx_revtitlex = []
		ta_restreviewx_ratedatex = []
		ta_restreviewx_revbodyx = []
		ta_restreviewx_visitdatex = []
		ta_restreviewx_ratingx = []
		ta_restreviewx_rateValuex = []
		ta_restreviewx_rateAtmx = []
		ta_restreviewx_rateServx = []
		ta_restreviewx_rateFoodx = []

		ta_restreview_listing = br.find_elements_by_css_selector(ta_restreview_listing_sel)

		for rowx in ta_restreview_listing:
			try:
				ta_restreviewx_user = rowx.find_element_by_css_selector(ta_restreview_user_sel)
				ta_restreviewx_userx.append(ta_restreviewx_user.text)
			except:
				ta_restreviewx_userx.append("anon")

			try:
				ta_restreviewx_usertitle = rowx.find_element_by_css_selector(ta_restreview_usertitle_sel)
				ta_restreviewx_usertitlex.append( ta_restreviewx_usertitle.text )
			except:
				ta_restreviewx_usertitlex.append( "unknown" )


			try:
				ta_restreviewx_city = rowx.find_element_by_css_selector(ta_restreview_city_sel)
				ta_restreviewx_cityx.append( ta_restreviewx_city.text )
			except:
				ta_restreviewx_cityx.append( "unknown" )

			try:
				ta_restreviewx_revtitle = rowx.find_element_by_css_selector(ta_restreview_revtitle_sel)
				#rt = ta_restreviewx_revtitle.text.encode('utf8')
				ta_restreviewx_revtitlex.append( ta_restreviewx_revtitle.text )
			except:
				ta_restreviewx_revtitlex.append( "no title" )

			try:
				ta_restreviewx_ratedate = rowx.find_element_by_css_selector(ta_restreview_ratedate_sel)
				ta_restreviewx_ratedatex.append( ta_restreviewx_ratedate.text )
			except:
				ta_restreviewx_ratedatex.append( "" )

			try:
				ta_restreviewx_rating = rowx.find_element_by_css_selector(ta_restreview_rating_sel)
				ta_restreviewx_ratingx.append( ta_restreviewx_rating.get_attribute("alt") )
			except:
				ta_restreviewx_ratingx.append( "no rating" )

			try:
				ta_restreviewx_revbody = rowx.find_element_by_css_selector(ta_restreview_revbody_sel)
				ta_restreviewx_revbodyx.append( ta_restreviewx_revbody.text )
			except:
				ta_restreviewx_revbodyx.append( "" )
				#print "Error no review found"
				REVIEW_ERROR = True



		for rowx in ta_restreview_listing:
			try:
				ta_restreview_more_button = rowx.find_element_by_css_selector(ta_restreview_more_button_sel)
				ta_restreview_more_button.click()
				time.sleep(1)
			except:
				nothing = 0


			try:
				ta_restreviewx_visitdate = rowx.find_element_by_css_selector(ta_restreview_visitdate_sel)
				ta_restreviewx_visitdatex.append( ta_restreviewx_visitdate.text )
			except:
				ta_restreviewx_visitdatex.append( "" )



		for rowx in ta_restreview_listing:

			try:
				ta_restreviewx_rateVASF = rowx.find_elements_by_css_selector(ta_restreview_ratingVASF_sel)
				if len(ta_restreviewx_rateVASF) == 0:
					ta_restreviewx_rateValuex.append( "" )
					ta_restreviewx_rateAtmx.append( "" )
					ta_restreviewx_rateServx.append( "" )
					ta_restreviewx_rateFoodx.append( "" )
				else:
					idx=0
					for rowy in ta_restreviewx_rateVASF:
						if idx==0:
							ta_restreviewx_rateValuex.append( rowy.get_attribute("alt") )
						elif idx==1:
							ta_restreviewx_rateAtmx.append( rowy.get_attribute("alt") )
						elif idx==2:
							ta_restreviewx_rateServx.append( rowy.get_attribute("alt") )
						elif idx==3:
							ta_restreviewx_rateFoodx.append( rowy.get_attribute("alt") )
						idx+=1

			except:
				ta_restreviewx_rateValuex.append( "" )
				ta_restreviewx_rateAtmx.append( "" )
				ta_restreviewx_rateServx.append( "" )
				ta_restreviewx_rateFoodx.append( "" )



		m = 0
		for rowx in ta_restreview_listing:
			#print len(ta_restreviewx_rateServx)
			#check for duplicates
			duplicate = check_rating_duplicate(db, ta_restreviewx_userx[m], ta_restreviewx_revtitlex[m])
			if not duplicate and not REVIEW_ERROR:
				try:
					params = (None, None, restaurant_id, ta_restreviewx_userx[m], ta_restreviewx_usertitlex[m], ta_restreviewx_cityx[m], ta_restreviewx_revtitlex[m], ta_restreviewx_ratedatex[m], ta_restreviewx_visitdatex[m], ta_restreviewx_ratingx[m], ta_restreviewx_revbodyx[m], ta_restreviewx_rateFoodx[m], ta_restreviewx_rateServx[m], ta_restreviewx_rateValuex[m], ta_restreviewx_rateAtmx[m])

					query = 'INSERT INTO ta_rest_review VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
					db.insert_row(query, params)
				except:
					print "Error: reviews not added to db"
			else:
				break

			m+=1


		#check for more pages of reviews
		#try:
			#ta_more_reviews_button = br.find_element_by_css_selector(next_button_sel)
			#ta_more_reviews_button.click()
			#time.sleep(6)

		#except:
			#break

		print "REVIEWS UPDATED! restaurant_id: "+str(restaurant_id)

			#x+=1 (end of while loop for multiple page scrape



	print "get_reviews success!"



#get_reviews('http://www.tripadvisor.co.uk/Tourism-g150807-Cancun_Yucatan_Peninsula-Vacations.html')
#get_reviews('http://www.tripadvisor.com/Tourism-g150812-Playa_del_Carmen_Yucatan_Peninsula-Vacations.html')
