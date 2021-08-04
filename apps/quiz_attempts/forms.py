from django import forms

from apps.questions import models as questions_models


class QuizQuestionForm(forms.ModelForm):
    choices = forms.ModelChoiceField(queryset=questions_models.Choice.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['choices'].queryset = questions_models.Choice.objects.filter(
                language=instance.language,
                question=instance)

    def clean(self):
        cleaned_data = super().clean()
        choices = cleaned_data.get("choices")
        is_choice_question = self.instance and self.instance.is_choice_question()
        is_text_question = self.instance and self.instance.is_text_question()
        if is_choice_question and not choices == self.instance.get_correct_choice():
            self.add_error('choices', 'Invalid choice selected')
        if is_text_question and not choices == self.instance.get_correct_text():
            self.add_error('choices', 'Invalid text entered')

    class Meta:
        model = questions_models.Choice
        fields = ['choices']
