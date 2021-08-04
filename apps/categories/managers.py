from django.utils import timezone
from treebeard.mp_tree import MP_NodeQuerySet, MP_NodeManager


class CategoryQuerySet(MP_NodeQuerySet):

    def delete(self):
        self.deactivate()

    def deactivate(self):
        date_removed = timezone.now()
        self.update(is_deleted=True, date_removed=date_removed)

    def active(self):
        return self.filter(is_deleted=False)

    def browsable(self):
        """
        Excludes non-public categories
        """
        return self.filter(is_public=True, ancestors_are_public=True)


class CategoryManager(MP_NodeManager):
    """Custom manager for nodes in a Materialized Path tree."""

    def get_queryset(self):
        """Sets the custom queryset as the default."""
        return CategoryQuerySet(self.model).order_by('path')
