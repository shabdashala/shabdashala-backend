from django import forms

from apps.questions import models as questions_models


class QuizQuestionForm(forms.ModelForm):
    choices = forms.ModelChoiceField(queryset=questions_models.Choice.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        self.fields['choices'].queryset = questions_models.Choice.objects.filter(
            language=instance.language,
            question=instance)

    class Meta:
        model = questions_models.Choice
        fields = ['choices']
