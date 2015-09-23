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


def get_id_from_table(db, x_id, tablename, colname, url):
	query = "SELECT "+x_id+" from "+str(tablename)+" where "+colname+"='"+str(url)+"'"
	x = db.query(query)
	return x

def get_hotel_urls(db, d_id):
	query = "SELECT ta_hotel_url from ta_hotel where destination_id="+str(d_id)
	x = db.query(query)
	return x

def check_rating_duplicate(db, user, review_title):
	rt = review_title.replace("'", "\\'")
	rt = rt.replace('"', '\\"')
	rt = unicode(rt).encode('utf-8')
	query = 'SELECT * from ta_hotel_review WHERE user=%s AND review_title=%s'
	params = (user, rt)
	x = db.queryp(query,params)
	if x:
		return True
	else:
		return False

def get_hotel_reviews(url):
	br = webdriver.PhantomJS('phantomjs')


	#path_to_chromedriver = '/home/user/Desktop/2014/programs/chromedriver/chromedriver' # change path as needed
	#br = webdriver.Chrome(executable_path = path_to_chromedriver)


	wait = ui.WebDriverWait(br,9)

	db = MyDatabase()

	br.get(url)


	destination_id_tupl = get_id_from_table(db, 'destination_id', 'destination', 'tripadvisor_url_main', url)
	destination_id = destination_id_tupl[0].get('destination_id')

	#Now to scrape all of the hotel reviews
	hotel_url_tupl = get_hotel_urls(db, destination_id)
	#print hotel_url_tupl


	for colx in hotel_url_tupl:

		hotelx_url = colx.get('ta_hotel_url')
		hotel_id_tupl = get_id_from_table(db, 'ta_hotel_id', 'ta_hotel', 'ta_hotel_url', hotelx_url)
		#print restaurant_id_tupl


		hotel_id = hotel_id_tupl[0].get('ta_hotel_id')
		br.get(hotelx_url)

		ta_hotelreview_listing_sel = u'.provider0'
		ta_hotelreview_listing_ext_sel = u'.extended.provider0'
		ta_hotelreview_user_sel = u'.scrname'
		ta_hotelreview_usertitle_sel = u'.reviewerTitle'
		ta_hotelreview_city_sel = u'.location'
		ta_hotelreview_revtitle_sel = u'.noQuotes'
		ta_hotelreview_ratedate_sel = u'.ratingDate'
		ta_hotelreview_visitdate_sel = u'.recommend-titleInline'
		ta_hotelreview_rating_sel = u'.rating_s img'
		ta_hotelreview_revbody_sel = u'.entry p'
		ta_hotelreview_ratingVLQRCS_text_sel = u'.recommend-answer'
		ta_hotelreview_ratingVLQRCS_sel = u'.rating_ss_fill'
		ta_hotelreview_roomtip_sel = u'.inlineRoomTip'

		ta_hotelreview_more_button_sel = u'.moreLink'
		next_button_sel = u'.sprite-pageNext'

		x=1
		REVIEW_ERROR = False

		ta_hotelreviewx_userx = []
		ta_hotelreviewx_usertitlex = []
		ta_hotelreviewx_cityx = []
		ta_hotelreviewx_revtitlex = []
		ta_hotelreviewx_ratedatex = []
		ta_hotelreviewx_visitdatex = []
		ta_hotelreviewx_ratingx = []
		ta_hotelreviewx_revbodyx = []
		ta_hotelreviewx_rateValuex = []
		ta_hotelreviewx_rateLocationx = []
		ta_hotelreviewx_rateSleepQx = []
		ta_hotelreviewx_rateRoomsx = []
		ta_hotelreviewx_rateCleanx = []
		ta_hotelreviewx_rateServx = []
		ta_hotelreviewx_roomtipx = []
		ta_hotelreview_listing = []

		ta_hotelreview_listing = br.find_elements_by_css_selector(ta_hotelreview_listing_sel)


		n=0
		while n < len(ta_hotelreview_listing):
			row1 = ta_hotelreview_listing[n]
			n+=1
			try:
				ta_hotelreview_more_button = row1.find_element_by_css_selector(ta_hotelreview_more_button_sel)
				ta_hotelreview_more_button.click()
				time.sleep(3)
				ta_hotelreview_listing = []
				ta_hotelreview_listing = br.find_elements_by_css_selector(ta_hotelreview_listing_ext_sel)

			except:
				pass


		for rowx in ta_hotelreview_listing:
			try:
				ta_hotelreviewx_rateVLQRCS = rowx.find_elements_by_css_selector(ta_hotelreview_ratingVLQRCS_text_sel)
				ta_hotelreviewx_VLQRCS_ratings = rowx.find_elements_by_css_selector(ta_hotelreview_ratingVLQRCS_sel)

				ta_hotelreviewx_rateValuex.append("")
				ta_hotelreviewx_rateLocationx.append("")
				ta_hotelreviewx_rateSleepQx.append("")
				ta_hotelreviewx_rateRoomsx.append("")
				ta_hotelreviewx_rateCleanx.append("")
				ta_hotelreviewx_rateServx.append("")

				#print str(ta_hotelreviewx_rateVLQRCS)
				if len(ta_hotelreviewx_rateVLQRCS) > 0:
					idx=0
					for rowy in ta_hotelreviewx_rateVLQRCS:
						VLQRCS_text = rowy.text

						if VLQRCS_text=='Value':
							del ta_hotelreviewx_rateValuex[-1]
							ta_hotelreviewx_rateValuex.append( ta_hotelreviewx_VLQRCS_ratings[idx].get_attribute("alt") )
						elif VLQRCS_text=='Location':
							ta_hotelreviewx_rateLocationx.pop()
							ta_hotelreviewx_rateLocationx.append( ta_hotelreviewx_VLQRCS_ratings[idx].get_attribute("alt") )
						elif VLQRCS_text=='Sleep Quality':
							ta_hotelreviewx_rateSleepQx.pop()
							ta_hotelreviewx_rateSleepQx.append( ta_hotelreviewx_VLQRCS_ratings[idx].get_attribute("alt") )
						elif VLQRCS_text=='Rooms':
							ta_hotelreviewx_rateRoomsx.pop()
							ta_hotelreviewx_rateRoomsx.append( ta_hotelreviewx_VLQRCS_ratings[idx].get_attribute("alt") )
						elif VLQRCS_text=='Cleanliness':
							ta_hotelreviewx_rateCleanx.pop()
							ta_hotelreviewx_rateCleanx.append( ta_hotelreviewx_VLQRCS_ratings[idx].get_attribute("alt") )
						elif VLQRCS_text=='Service':
							ta_hotelreviewx_rateServx.pop()
							ta_hotelreviewx_rateServx.append( ta_hotelreviewx_VLQRCS_ratings[idx].get_attribute("alt") )
						idx+=1


			except:
				ta_hotelreviewx_rateValuex.append( "" )
				ta_hotelreviewx_rateLocationx.append( "" )
				ta_hotelreviewx_rateSleepQx.append( "" )
				ta_hotelreviewx_rateRoomsx.append( "" )
				ta_hotelreviewx_rateCleanx.append( "" )
				ta_hotelreviewx_rateServx.append( "" )



		for rowx in ta_hotelreview_listing:
			try:
				ta_hotelreviewx_visitdate = rowx.find_element_by_css_selector(ta_hotelreview_visitdate_sel)
				ta_hotelreviewx_visitdatex.append( ta_hotelreviewx_visitdate.text )
			except:
				ta_hotelreviewx_visitdatex.append( "" )
			#print str(ta_hotelreviewx_visitdatex)


		for rowx in ta_hotelreview_listing:
			try:
				ta_hotelreviewx_roomtip = rowx.find_element_by_css_selector(ta_hotelreview_roomtip_sel)
				ta_hotelreviewx_roomtipx.append( ta_hotelreviewx_roomtip.text )
			except:
				ta_hotelreviewx_roomtipx.append( "" )

			#print str(ta_hotelreviewx_roomtipx)


		for rowx in ta_hotelreview_listing:
			try:
				ta_hotelreviewx_user = rowx.find_element_by_css_selector(ta_hotelreview_user_sel)
				ta_hotelreviewx_userx.append(ta_hotelreviewx_user.text)

			except:
				ta_hotelreviewx_userx.append("anon")

			try:
				ta_hotelreviewx_usertitle = rowx.find_element_by_css_selector(ta_hotelreview_usertitle_sel)
				ta_hotelreviewx_usertitlex.append( ta_hotelreviewx_usertitle.text )

			except:
				ta_hotelreviewx_usertitlex.append( "unknown" )

			try:
				ta_hotelreviewx_city = rowx.find_element_by_css_selector(ta_hotelreview_city_sel)
				if not ta_hotelreviewx_city.text:
					ta_hotelreviewx_cityx.append("unknown")
				else:
					ta_hotelreviewx_cityx.append( ta_hotelreviewx_city.text )
			except:
				ta_hotelreviewx_cityx.append( "unknown" )


			try:
				ta_hotelreviewx_revtitle = rowx.find_element_by_css_selector(ta_hotelreview_revtitle_sel)
				ta_hotelreviewx_revtitlex.append( ta_hotelreviewx_revtitle.text )
			except:
				ta_hotelreviewx_revtitlex.append( "no title" )



			try:
				ta_hotelreviewx_ratedate = rowx.find_element_by_css_selector(ta_hotelreview_ratedate_sel)
				ta_hotelreviewx_ratedatex.append( ta_hotelreviewx_ratedate.text )
			except:
				ta_hotelreviewx_ratedatex.append( "" )



			try:
				ta_hotelreviewx_revbody = rowx.find_element_by_css_selector(ta_hotelreview_revbody_sel)
				ta_hotelreviewx_revbodyx.append( ta_hotelreviewx_revbody.text )
			except:
				ta_hotelreviewx_revbodyx.append( "" )
				REVIEW_ERROR = True

			try:
				ta_hotelreviewx_rating = rowx.find_element_by_css_selector(ta_hotelreview_rating_sel)
				ta_hotelreviewx_ratingx.append( ta_hotelreviewx_rating.get_attribute("alt") )
			except:
				ta_hotelreviewx_ratingx.append( "" )









		m = 0
		for rowx in ta_hotelreview_listing:
			#check for duplicates
			duplicate = check_rating_duplicate(db, ta_hotelreviewx_userx[m], ta_hotelreviewx_revtitlex[m])
			#print str(ta_hotelreviewx_ratingx[m])
			if not duplicate and not REVIEW_ERROR:
				try:
					params = (None, None, hotel_id, ta_hotelreviewx_userx[m], ta_hotelreviewx_usertitlex[m], ta_hotelreviewx_cityx[m], ta_hotelreviewx_revtitlex[m], ta_hotelreviewx_ratedatex[m], ta_hotelreviewx_visitdatex[m], ta_hotelreviewx_ratingx[m], ta_hotelreviewx_revbodyx[m], ta_hotelreviewx_rateValuex[m], ta_hotelreviewx_rateLocationx[m], ta_hotelreviewx_rateSleepQx[m], ta_hotelreviewx_rateRoomsx[m], ta_hotelreviewx_rateCleanx[m], ta_hotelreviewx_rateServx[m], ta_hotelreviewx_roomtipx[m])

					#print params
					query = 'INSERT INTO ta_hotel_review VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
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

		print "REVIEWS UPDATED! hotel_id: "+str(hotel_id)

			#x+=1 (end of while loop for multiple page scrape



	print "get_hotel_reviews success!"

#get_hotel_reviews('http://www.tripadvisor.com/Tourism-g150812-Playa_del_Carmen_Yucatan_Peninsula-Vacations.html')
