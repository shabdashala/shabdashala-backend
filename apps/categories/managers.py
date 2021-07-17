from treebeard.mp_tree import MP_NodeQuerySet


class CategoryQuerySet(MP_NodeQuerySet):

    def browsable(self):
        """
        Excludes non-public categories
        """
        return self.filter(is_public=True, ancestors_are_public=True)
