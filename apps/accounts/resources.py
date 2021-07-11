from import_export import resources

from . import models as accounts_models


class UserResource(resources.ModelResource):

    class Meta:
        model = accounts_models.User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'mobile', 'is_active', 'date_joined']
