from django.db import models
from django.utils import timezone


class DeactivateQuerySet(models.query.QuerySet):
    """
    QuerySet whose delete() does not delete items, but instead marks the
    rows as not active, and updates the timestamps
    """

    def delete(self):
        self.deactivate()

    def deactivate(self):
        date_removed = timezone.now()
        return super().update(is_deleted=True, date_removed=date_removed)

    def active(self):
        return super().filter(is_deleted=False)


class DeactivateManager(models.Manager):
    """
    Manager that returns a DeactivateQuerySet,
    to prevent object deletion.
    """

    def get_query_set(self):
        return DeactivateQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_query_set().active()

    def all(self):
        return super().all()
