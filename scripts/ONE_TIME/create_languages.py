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
    for LANGUAGE_DATA in LANGUAGES_DATA:
        languages_models.Language.objects.get_or_create(
            name=LANGUAGE_DATA['name'],
            defaults={
                'english_name': LANGUAGE_DATA['english_name'],
                'two_letter_code': LANGUAGE_DATA['two_letter_code'],
                'three_letter_code': LANGUAGE_DATA['three_letter_code'],
                'display_order': LANGUAGE_DATA['display_order'],
                'is_active': LANGUAGE_DATA['is_active'],
            }
        )


def seed_initial_data():
    seed_languages_data()
