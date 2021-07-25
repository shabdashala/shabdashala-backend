import csv
import os
import random

from django.conf import settings

from apps.categories.utils import create_from_breadcrumbs
from apps.languages import models as languages_models
from apps.questions import constants as questions_constants
from apps.questions import models as questions_models
from apps.quizzes import constants as quizzes_constants
from apps.quizzes import models as quizzes_models
from apps.sentences import models as sentences_models

from .create_languages import seed_languages_data
from .telugu_sandhulu_data import (
    SANDHI_CATEGORY_MAPPING,
    SANDHI_CATEGORY_NAMES,
    SANDHULU,
    TELUGU_SANDHULU_DATA
)


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
        correct_sandhi_category_name = SANDHI_CATEGORY_MAPPING[sandhi_question_data['sandhi_peru']]
        correct_sandh_category = create_from_breadcrumbs(
            language_code='te',
            breadcrumb_str=correct_sandhi_category_name)
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
        sentence.categories.add(correct_sandh_category)

        hint_text = f"విసంధి: {sandhi_question_data['visandhi']}"
        success_text = f"""
<p>సంధి పదం: <b>{sandhi_question_data['sandhi_padam']}</b></p>
<p>విసంధి: <b>{sandhi_question_data['visandhi']}</p>
<p>సంధి పేరు: <b>{sandhi_question_data['sandhi_peru']}</p>
        """
        question = questions_models.Question.objects.filter(
            language=language,
            category=correct_sandh_category,
            question_type=questions_constants.MCQ,
            sentence=sentence,
            is_published=True,
        ).first()
        if not question:
            question = questions_models.Question.objects.create(
                language=language,
                category=correct_sandh_category,
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

        number_of_other_choices = random.randint(1, 5)
        other_sadhi_names = random.sample([
            sandhi_name for sandhi_name in SANDHI_CATEGORY_NAMES
            if sandhi_name is not correct_sadhi_name
        ], number_of_other_choices)

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


def seed_question_sets_data():
    language = languages_models.Language.objects.get(two_letter_code='te')
    category = create_from_breadcrumbs(language_code=language.two_letter_code, breadcrumb_str=SANDHULU)

    question_set_title = 'సంధులు ప్రశ్నలు'
    question_set = questions_models.QuestionSet.objects.filter(
        title=question_set_title,
        description='',
        display_order=0,
    ).first()
    if not question_set:
        question_set = questions_models.QuestionSet.objects.create(
            title=question_set_title,
            description='',
            display_order=0,
        )
    question_set.categories.add(category)


def seed_quizzes_data():
    quiz_title = 'సంధుల పరీక్ష'
    question_set_title = 'సంధులు ప్రశ్నలు'

    language = languages_models.Language.objects.get(two_letter_code='te')
    category = create_from_breadcrumbs(language_code=language.two_letter_code, breadcrumb_str=SANDHULU)
    question_set = questions_models.QuestionSet.objects.filter(title=question_set_title).first()

    quiz = quizzes_models.Quiz.objects.filter(
        title=quiz_title,
        language=language,
        category=category,
    ).first()
    if not quiz:
        quiz = quizzes_models.Quiz.objects.create(
            title=quiz_title,
            language=language,
            category=category,
            quiz_type=quizzes_constants.DYNAMIC,
            maximum_number_of_questions=5,
            maximum_marks=5,
            maximum_bonus_marks=5,
            is_published=True,
            random_order=True,
            pass_mark=3,
            success_text='',
            fail_text='',
        )
    quiz.question_sets.add(question_set)


def seed_initial_data():
    seed_languages_data()
    seed_sandhulu_categories()
    seed_sandhulu_questions()
    seed_question_sets_data()
    seed_quizzes_data()

