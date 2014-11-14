from django import forms
from submission.models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'
        exclude = ('status', 'type')
