from contextlib import suppress

from django.conf import settings

ADMIN_LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
ALLOWED_LANGUAGES = [lang[0] for lang in settings.LANGUAGES]


class ForceTeluguLangMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Ignore Accept-Language HTTP headers.

        This will force the I18N machinery to always choose

          - Telugu for the main site
          - ADMIN_LANGUAGE_CODE for the admin site

        as the default initial language unless another one is set via
        sessions or cookies.

        Should be installed *before* any middleware that checks
        request.META['HTTP_ACCEPT_LANGUAGE'], namely
        `django.middleware.locale.LocaleMiddleware`.
        """
        language = request.GET.get('lang')

        if request.method.lower() == 'get' and \
                language != request.session.get('language') and language in ALLOWED_LANGUAGES:
            request.session['language'] = language
        elif 'language' in request.session:
            language = request.session['language']

        if language in ALLOWED_LANGUAGES:
            # Force Telugu locale for the main site
            accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '').split(',')

            with suppress(ValueError):
                # Remove `lang` from the HTTP_ACCEPT_LANGUAGE to avoid duplicates
                accept.remove(f'{language}-in')

            accept = [f'{language}-in'] + accept
            request.META['HTTP_ACCEPT_LANGUAGE'] = f"""{','.join(accept)}"""

        response = self.get_response(request)

        return response
