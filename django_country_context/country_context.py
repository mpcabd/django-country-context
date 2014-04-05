# -*- coding: utf-8 -*-
from contextlib import contextmanager
from django.conf import settings

import threading
import countries_data

thread__local = threading.local()


class CountryContext(object):
    def __init__(self):
        self.last_country = [settings.DEFAULT_COUNTRY]
        self.current_country_code = settings.DEFAULT_COUNTRY

    def activate(self, country_code):
        self.last_country.insert(0, self.current_country_code)
        self.current_country_code = country_code

    def deactivate(self):
        self.current_country_code = self.last_country.pop(0)


def __get_context():
    if not hasattr(thread__local, 'django_country_context'):
        thread__local.django_country_context = CountryContext()
    return thread__local.django_country_context


def activate_country(country_code):
    __get_context().activate(country_code)


def deactivate_country():
    __get_context().deactivate()


def get_current_country_code():
    return __get_context().current_country_code


def get_current_country_name():
    return countries_data.COUNTRIES_DICT[get_current_country_code()]


@contextmanager
def country(country_code):
    activate_country(country_code)
    yield country_code
    deactivate_country()