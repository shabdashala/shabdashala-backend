import copy

from apps.languages import models as languages_models


LANGUAGES_DATA = [
    {
        'name': 'తెలుగు',
        'english_name': 'Telugu',
        'two_letter_code': 'te',
        'three_letter_code': 'tel',
        'display_order': 0,
        'is_active': True,
    }
]


def seed_languages_data():
    for _LANGUAGE_DATA in LANGUAGES_DATA:
        LANGUAGE_DATA = copy.deepcopy(_LANGUAGE_DATA)
        languages_models.Language.objects.update_or_create(
            name=LANGUAGE_DATA['name'],
            defaults={
                'english_name': LANGUAGE_DATA['english_name'],
                'two_letter_code': LANGUAGE_DATA['two_letter_code'],
                'three_letter_code': LANGUAGE_DATA['three_letter_code'],
                'display_order': LANGUAGE_DATA['display_order'],
                'is_active': True,
                'is_deleted': False,
                'date_removed': None,
            }
        )


def seed_initial_data():
    seed_languages_data()
