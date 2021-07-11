from django.apps import apps

from rest_framework.authentication import TokenAuthentication as RestFrameworkTokenAuthentication


class TokenAuthentication(RestFrameworkTokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Token'
    model = apps.get_model('accounts', 'DeviceToken')
