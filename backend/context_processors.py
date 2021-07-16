from django.conf import settings

IS_PRODUCTION = getattr(settings, 'IS_PRODUCTION', False)


__all__ = [
    'site_context',
]


def site_context(request):
    context = {
        'is_production': IS_PRODUCTION,
    }
    return context
