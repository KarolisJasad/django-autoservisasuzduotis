from django import forms
from . import models


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = models.OrderComment
        fields = ('content', 'order', 'commentator')
        widgets = {
            'order': forms.HiddenInput(),
            'commentator': forms.HiddenInput(),
        }