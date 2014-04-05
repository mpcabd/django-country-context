from django.conf import settings

import country_context


class CountryContextMiddleware(object):
    def process_request(self, request):
        country_code = self.get_country_code_from_request(request) or settings.DEFAULT_COUNTRY
        country_context.activate_country(country_code)

    def process_response(self, request, response):
        country_context.deactivate_country()
        return response

    def get_country_code_from_request(self, request):
        raise NotImplementedError