# -*- coding: utf-8 -*-
class HouseAd(object):
    def __init__(self, id_=None, address=None, rooms=None, price=None, phone=None, link=None,
                 date=None):
        self._id = id_
        self._address = address
        self._rooms = rooms
        self._price = price
        self._phone = phone
        self._link = link
        self._date = date

    def __unicode__(self):
        return u"{address}. {rooms} חדרים {price} שח {link}".format(
            address=self._address, rooms=self._rooms, price=self._price, link=self._link)

