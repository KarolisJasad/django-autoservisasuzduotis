from django import forms
from . import models

class DateInput(forms.DateInput):
    input_type = 'date'


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = models.OrderComment
        fields = ('content', 'order', 'commentator')
        widgets = {
            'order': forms.HiddenInput(),
            'commentator': forms.HiddenInput(),
        }

class OrderReserveForm(forms.ModelForm):
    class Meta:
        model = models.Uzsakymas
        fields = {'car', 'order_date', 'status'}
        widgets = {
            'car': forms.HiddenInput(),
            'order_date': DateInput(),
            'status': forms.HiddenInput(),
        }

class ServiceForm(forms.Form):
    service = forms.ModelChoiceField(queryset=models.Paslauga.objects.all(), label='Service')
    count = forms.IntegerField(label='Count')