#!/usr/bin/python
# -*- coding: utf-8 -*-

import yad2_api
import mail

from models import HouseAd
from bs4 import BeautifulSoup
import time


class AdParser(object):
    pass


class Yad2Parser(AdParser):

    TD_STREET = 8
    TD_PRICE = 10
    TD_ROOMS = 12
    TD_DATE = 20

    def __init__(self):
        self._ads = self._load_ads()
        self._new_adds = []
        self._mail = mail.AddSender()

    @staticmethod
    def _load_ads():
        return {}

    def add_ad(self, ad):
        if ad._id not in self._ads:
            self._ads[ad._id] = ad._id
            self._new_adds.append(ad)

    @classmethod
    def parse_yad2_ad(cls, ad):
        id_ = ad["id"].split("_")[-1]
        cols = ad.find_all("td")

        price_with_comma = cols[cls.TD_PRICE].text.strip()[:-1]
        price = int(price_with_comma.replace(",",   ""))

        rooms_txt = cols[cls.TD_ROOMS].text.strip()
        if rooms_txt:
            rooms = float(rooms_txt)
        else:
            rooms = None

        street = cols[cls.TD_STREET].text.strip()
        date = cols[cls.TD_DATE].text.strip()

        return HouseAd(id_=id_, date=date, address=street, rooms=rooms, price=price,
                       link=yad2_api.get_ad_link(id_))

    def find_apartments(self, from_rooms):
        print "Looking for new apt"
        self._new_adds = []
        html = yad2_api.get_ads(from_rooms)
        soup = BeautifulSoup(html, "html.parser")
        main_table = soup.find("table", attrs={"class": "main_table"})
        table_body = main_table.find("tbody")
        rows = table_body.find_all("tr", attrs={"class": "showPopupUnder"})

        for row in rows:
            self.add_ad(self.parse_yad2_ad(row))

        self._update_new_adds()

    def _update_new_adds(self):
        if self._new_adds:
            print "New adds!"
            self._mail.send_new_adds(self._new_adds)


def main():
    parser = Yad2Parser()
    while True:
        parser.find_apartments(4)
        time.sleep(60*60)

if __name__ == '__main__':
    main()
