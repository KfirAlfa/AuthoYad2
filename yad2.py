#!/usr/bin/python
# -*- coding: utf-8 -*-

import yad2_api
import mail

from models import HouseAd
from bs4 import BeautifulSoup
import re
import time


class AdParser(object):
    def __init__(self):
        self._ads = self._load_ads()
        self._new_adds = []
        #self._mail = mail.AddSender()

    def get_raw_adds(selfs, from_rooms):
        raise NotImplementedError()

    def parse_ad(self, add):
        raise NotImplementedError()

    @staticmethod
    def _load_ads():
        return {}

    def add_ad(self, ad):
        if ad._id not in self._ads:
            self._ads[ad._id] = ad._id
            self._new_adds.append(ad)

    def find_apartments(self, from_rooms):
        print "Looking for new apt"
        self._new_adds = []

        for add in self.get_raw_adds(from_rooms):
            self.add_ad(self.parse_ad(add))

        return self._new_adds

            #self._mail.send_new_adds(self._new_adds)


class Yad2Parser(AdParser):

    TD_STREET = 8
    TD_PRICE = 10
    TD_ROOMS = 12
    TD_DATE = 20


    @classmethod
    def parse_ad(cls, ad):
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

    def get_raw_adds(self, from_rooms):
        html = yad2_api.get_ads(from_rooms)
        soup = BeautifulSoup(html, "html.parser")
        main_table = soup.find("table", attrs={"class": "main_table"})
        table_body = main_table.find("tbody")
        rows = table_body.find_all("tr", attrs={"class": "showPopupUnder"})
        return  rows


class KomoParser(AdParser):

    @classmethod
    def parse_ad(cls, metadata):
        data_table = metadata.find_all("table")[2]
        rows = data_table.find_all("td")
        try:
            price = int(rows[1].text.strip()[:-1].replace(",", ""))
        except UnicodeEncodeError:
            price = None
        link = cls._parse_link(rows[0].a["href"])
        title = metadata.find_all("div", id=re.compile("^dv"))[0]
        title_name = title["bigtitle"]
        id_ = title["id"]

        house = HouseAd(id_=id_, price=price, link=link, address=title_name)
        print unicode(house)
        return house

    @staticmethod
    def get_raw_adds(from_rooms):
        html = yad2_api.get_komo_adds()
        soup = BeautifulSoup(html, "html.parser")
        adds = soup.find_all("table", {"class": "tblModaa"})
        return [add.tr("td", {"class": "tdKotarot"})[0] for add in adds]

    @staticmethod
    def _parse_link(href):
        return "?".join([yad2_api.KOMO_URL, href.split("?")[-1]])


class AddDogem(object):
    def __init__(self, *args):
        self._parsers = [parser() for parser in args if issubclass(parser, AdParser)]
        self._mail = mail.AddSender()

    def run(self):
        new_adds = []
        while True:
            for parser in self._parsers:
                print "Geting new", parser
                new_adds.append(parser.find_apartments(4))
            if new_adds:
                self._mail.send_new_adds(new_adds)
                new_adds = []
            time.sleep(30*60*60)

def main():
    fuck = AddDogem(KomoParser, Yad2Parser)
    fuck.run()

if __name__ == '__main__':
    main()
