# -*- coding: utf-8 -*-

from requests import Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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


def _get_html(url, params=None):
    chrmoe_options =  Options()
    chrmoe_options.add_argument("--headless")
    browser = webdriver.Chrome(chrome_options=chrmoe_options)
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
