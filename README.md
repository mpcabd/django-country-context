# Django Country Context

This module solves a small problem that can be found in many sites, where the website has to support multiple countries, e.g. e-commerce website with different stores for different countries, this module allows the developer to define a context per thread, this context holds all the information about the currently available country, and allows the developer to rely on the context always to get the current country instead of passing it through the different levels of code. This module is thread-safe, it defines a different context for each thread.

## Using The Context
To use the country context

* You activate the country of choice when you start to process the request, one place for activating the country is by writing a [Django middleware](https://docs.djangoproject.com/en/dev/topics/http/middleware/) that activates the country in the `process_request` method.
* After that your code should depend on the `country_context.get_current_country_code` to get the current country code, and that should be everywhere, so that you don't have to pass the current country from the view to the controllers and to other parts of your code.
* In the end when you finish processing the request you should deactivate the country, also you can do that in the middleware in the `process_response` method.

If you want to create a middleware you can extend the <code>CountryContextMiddleware</code> included with this package.

## Settings
You should have the following two variables:

  1. `DEFAULT_COUNTRY`: The default country code that will be the active country by default.
  2. `ENABLED_COUNTRIES`: A list of country codes that are enabled for your site. Codes are in [ISO 3166-1 Alpha 2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) format.
  
## Example Usage
We will imagine a Django site, an e-commerce site that serves multiple stores in US and UK, by default it'll be serving the US site, but if the URL was prefixed with UK then the site will serve the UK store.

    # site/settings.py
    # ...
    DEFAULT_COUNTRY = 'US'
    ENABLED_COUNTRIES = ['US', 'UK']
    # ...
    MIDDLEWARE_CLASSES = (
      # ...
      'site.country_context_middleware.SiteCountryContextMiddleware',
      # ...
    )


---

    # site/country_context_middleware.py
    import re
    
    from django_country_context.country_context_middleware import CountryContextMiddleware
    
    
    class SiteCountryContextMiddleware(CountryContextMiddleware):
      def get_country_code_from_request(self, request):
        if re.match(r'^/UK/', request.path_info, re.I):
          return 'UK'
        return 'US'

---

    # site/urls.py
    
    from django.contrib import admin
    from django.conf import settings
    from django.conf.urls import patterns, include, url
    
    urlpatterns = patterns('',
      url(r'^(?:%s)?/' % '|'.join(
        ''.join(
          '[%s%s]' % (c.upper(), c.lower()) for c in country
        ) for country in settings.ENABLED_COUNTRIES
      ), include('app.urls')),
    )

---

    # app/models.py
    
    from django.db import models
    from django_country_context import country_context, countries_data
    
    
    class StoreManager(models.Manager):
      def __init__(self, countries_enabled=True):
        super(StoreManager, self).__init__()
        self.countries_enabled = countries_enabled
    
      def get_query_set(self):
        qs = super(StoreManager, self).get_query_set()
        if self.countries_enabled:
          qs = qs.filter(country=country_context.get_current_country_code())
        return qs
    
    
    class Store(models.Model):
      # ...
      country = models.CharField(max_length=2, default=country_context.get_current_country_code, choices=countries_data.ENABLED_COUNTRIES_TUPLE, db_index=True)
    
      objects = StoreManager()
      objects_no_countries = StoreManager(countries_enabled=False)

---

    # app/admin.py
    
    from django.contrib import admin
    from models import Store
    
    
    class StoreAdmin(admin.ModelAdmin):
      model = Store
      def queryset(self, request):
        self.model._default_manager = self.model.objects_no_countries
        return super(StoreAdmin, self).queryset(request)
      # ...
    
    admin.site.register(Store, StoreAdmin)

Using the setup above will allow the views to call the query the Store model without handling special cases for countries, and you can change the logic of getting the current country without any change to your views, this way we've separated the country context completely from the logic of the site. And when you need to get the current country name or code you can use `country_context.get_current_country_name()` and `country_context.get_current_country_code()` respectively. Please note that the setup above was written for a Django 1.4.x.

## Download
[Django Country Context on source code on GitHub](https://github.com/mpcabd/django-country-context/)

## Read Blog Post
[Django Country Context on mpcabd.igeex.biz](http://mpcabd.xyz/django-country-context/)
