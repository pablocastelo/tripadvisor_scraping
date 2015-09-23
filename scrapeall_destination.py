#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from get_destination import get_destination
from get_restaurants import get_restaurants
from get_restaurant_reviews import get_reviews
from get_hotels import get_hotels
from get_hotel_reviews import get_hotel_reviews



#Enter the url of the destination here.
#e.g. http://www.tripadvisor.com/Tourism-g150812-Playa_del_Carmen_Yucatan_Peninsula-Vacations.html

url = 'http://www.tripadvisor.com/Tourism-g150812-Playa_del_Carmen_Yucatan_Peninsula-Vacations.html'


get_destination(url)
get_restaurants(url)
get_reviews(url)
get_hotels(url)
get_hotel_reviews(url)
