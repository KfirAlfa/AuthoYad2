# -*- coding: utf-8 -*-

from requests import Request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


MAIN_URL = "http://www.yad2.co.il/Nadlan/"
SEARCH_PAGE = "rent.php?"
GET_AD_PAGE = "iframe_hotPicrent.php?"

GET_AD_PARAMS = {
    "CatID": 2,
    "SubCatID": 2,
    "RecordID": None,
    "Code": "5e32e0e10fe5fafc51cb23d1e0783ab4" #TODO-> WTF ?
}

SEARCH = {
    "City": "תל אביב יפו",
    "Neighborhood": "",
    "HomeTypeID": "",
    "fromRooms": 4,
    "untilRooms": "",
    "fromPrice": "",
    "untilPrice": "",
    "PriceType": 1,
    "FromFloor": "",
    "ToFloor": "",
    "EnterDate": "",
    "Info": "",
}

KOMO_URL = "https://www.komo.co.il/code/nadlan/apartments-for-rent.asp"
KOMO_PARAMS = {
    "subLuachNum":1,
    "nehes": 1,
    "ezorNum": 21,
    "fromRooms": 4,
    "toPrice": 11000,
    "dvSearch": 1,
}


def _get_html(url, params=None):
    caps = DesiredCapabilities.PHANTOMJS
    caps["userAgent"] = "Mozilla/5.0"
    caps["browserName"] = "Google Chrome"
    print url

    browser = webdriver.PhantomJS(desired_capabilities=caps)

    url = Request('GET', url, params=params).prepare().url
    browser.get(url)
    html = browser.page_source
    browser.close()
    return html


def get_ads(from_rooms=None):
    params = SEARCH
    if from_rooms is not None:
        params["fromRooms"] = from_rooms
    html = _get_html(MAIN_URL + SEARCH_PAGE, params)
    return html


def get_ad(ad_id):
    params = GET_AD_PARAMS
    params["RecordID"] = ad_id
    html = _get_html(MAIN_URL + GET_AD_PAGE, params)
    return html


def get_ad_link(ad_id):
    params = GET_AD_PARAMS
    params["RecordID"] = ad_id
    return Request('GET', MAIN_URL + GET_AD_PAGE, params=params).prepare().url


def get_komo_adds(from_rooms=None, to_price=None, ):
    params = KOMO_PARAMS
    if from_rooms is not None:
        params['fromRooms'] = from_rooms
    if to_price is not None:
        params['to_price'] = to_price

    html = _get_html(KOMO_URL, params=params)
    return html
