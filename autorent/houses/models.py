# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class HouseAd(models.Model):

    ad_id = models.CharField(max_length=100)
    rooms = models.FloatField()
    price = models.IntegerField(0)
    link = models.CharField(max_length=1000)
    date = models.DateField()

    def __str__(self):
        return u"{address}. {rooms} חדרים {price} שח {link}".format(
            address=self._address, rooms=self._rooms, price=self._price, link=self._link)


