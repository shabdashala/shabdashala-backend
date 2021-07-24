import csv
import os

from django.conf import settings

from apps.categories.utils import create_from_breadcrumbs
from apps.languages import models as languages_models
from apps.questions import constants as questions_constants
from apps.questions import models as questions_models
from apps.sentences import models as sentences_models

from .create_languages import seed_languages_data
from .telugu_sandhulu_data import SANDHI_CATEGORY_MAPPING, SANDHI_CATEGORY_NAMES, TELUGU_SANDHULU_DATA


def load_sandhulu_questions_data():
    data = []
    with open(os.path.abspath(f"{settings.DATA_DIR}/telugu_sandhulu_data.tsv")) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            if len(line) >= 3:
                data.append({
                    'sandhi_padam': line[0].strip(),
                    'visandhi': line[1].strip(),
                    'sandhi_peru': line[2].strip(),
                })
    return data


def seed_sandhulu_categories():
    for TELUGU_SANDHI_DATA in TELUGU_SANDHULU_DATA:
        category = create_from_breadcrumbs(
            language_code='te',
            breadcrumb_str=TELUGU_SANDHI_DATA['name'])
        category.description = TELUGU_SANDHI_DATA['description']
        category.is_active = True
        category.save()


def seed_sandhulu_questions():
    sandhulu_questions_data = load_sandhulu_questions_data()
    language = languages_models.Language.objects.get(two_letter_code='te')
    for sandhi_question_data in sandhulu_questions_data:
        category = create_from_breadcrumbs(
            language_code='te',
            breadcrumb_str=SANDHI_CATEGORY_MAPPING[sandhi_question_data['sandhi_peru']])
        sentence_text = f"\"{sandhi_question_data['sandhi_padam']}\" ఏం సంధి?"
        sentence = sentences_models.Sentence.objects.filter(
            language=language,
            text=sentence_text,
            is_active=True,
        ).first()
        if not sentence:
            sentence = sentences_models.Sentence.objects.create(
                language=language,
                text=sentence_text,
                is_active=True,
            )
        sentence.categories.add(category)

        hint_text = f"విసంధి: {sandhi_question_data['visandhi']}"
        success_text = f"""
<p>సంధి పదం: <b>{sandhi_question_data['sandhi_padam']}</b></p>
<p>విసంధి: <b>{sandhi_question_data['visandhi']}</p>
<p>సంధి పేరు: <b>{sandhi_question_data['sandhi_peru']}</p>
        """
        question = questions_models.Question.objects.filter(
            language=language,
            category=category,
            question_type=questions_constants.MCQ,
            sentence=sentence,
            is_published=True,
        ).first()
        if not question:
            question = questions_models.Question.objects.create(
                language=language,
                category=category,
                question_type=questions_constants.MCQ,
                sentence=sentence,
                is_published=True,
                maximum_marks=1,
            )

        question.description = ''
        question.hint_text = hint_text
        question.success_text = success_text
        question.save()

        if question.choices.exists():
            question.choices.all().delete()

        correct_sadhi_name = sandhi_question_data['sandhi_peru']
        correct_choice_sentence = sentences_models.Sentence.objects.filter(
            language=language,
            text=correct_sadhi_name,
            is_active=True,
        ).first()
        if not correct_choice_sentence:
            correct_choice_sentence = sentences_models.Sentence.objects.create(
                language=language,
                text=correct_sadhi_name,
                is_active=True)

        question.choices.create(
            language=question.language,
            sentence=correct_choice_sentence,
            is_correct=True
        )

        other_sadhi_names = [sandhi_name for sandhi_name in SANDHI_CATEGORY_NAMES
                             if sandhi_name is not correct_sadhi_name]

        for other_sadhi_name in other_sadhi_names:
            other_choice_sentence = sentences_models.Sentence.objects.filter(
                language=language,
                text=other_sadhi_name,
                is_active=True,
            ).first()
            if not other_choice_sentence:
                other_choice_sentence = sentences_models.Sentence.objects.create(
                    language=language,
                    text=other_sadhi_name,
                    is_active=True)
            question.choices.create(
                language=question.language,
                sentence=other_choice_sentence,
                is_correct=False
            )


def seed_initial_data():
    seed_languages_data()
    seed_sandhulu_categories()
    seed_sandhulu_questions()

