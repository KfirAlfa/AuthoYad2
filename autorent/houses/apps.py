# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

import multiprocessing
import prog.yad2

class HousesConfig(AppConfig):
    name = 'houses'

    def ready(self):
        proc = multiprocessing.Process(target=prog.yad2.main)
        proc.start()

