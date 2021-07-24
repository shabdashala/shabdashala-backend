from apps.languages import models as languages_models

from . import models as categories_models


def create_from_sequence(language, bits):
    """
    Create categories from an iterable
    """
    if len(bits) == 1:
        # Get or create root node
        name = bits[0]
        try:
            # Category names should be unique at the depth=1
            root = categories_models.Category.objects.get(depth=1, language=language, name=name)
        except categories_models.Category.DoesNotExist:
            root = categories_models.Category.add_root(language=language, name=name)
        except categories_models.Category.MultipleObjectsReturned:
            raise ValueError((
                "There are more than one categories with name "
                "%s at depth=1") % name)
        return [root]
    else:
        parents = create_from_sequence(language, bits[:-1])
        parent, name = parents[-1], bits[-1]
        try:
            child = parent.get_children().get(language=language, name=name)
        except categories_models.Category.DoesNotExist:
            child = parent.add_child(language=language, name=name)
        except categories_models.Category.MultipleObjectsReturned:
            raise ValueError((
                "There are more than one categories with name "
                "%s which are children of %s") % (name, parent))
        parents.append(child)
        return parents


def create_from_breadcrumbs(language_code, breadcrumb_str, separator='>'):
    """
    Create categories from a breadcrumb string
    """
    language = languages_models.Language.objects.get(two_letter_code=language_code)
    category_names = [x.strip() for x in breadcrumb_str.split(separator)]
    categories = create_from_sequence(language, category_names)
    return categories[-1]
