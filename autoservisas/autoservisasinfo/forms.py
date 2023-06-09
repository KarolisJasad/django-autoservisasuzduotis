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

class CarAssignmentForm(forms.Form):
    car = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CarAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['car'].queryset = models.Automobilis.objects.filter(user=None)
        self.user = user

    def save(self):
        car = self.cleaned_data['car']
        car.user = self.user
        car.save()

    def label_from_instance(self, car):
        return f'{car.car_number} - {car.vin_number}'

class CarUpdateForm(forms.ModelForm):
    car_description = forms.CharField(widget=forms.Textarea)
    car_image = forms.ImageField(required=False)

    class Meta:
        model = models.AutomobilioModelis
        fields = ['car_description', 'car_image']

class ConfirmDeleteForm(forms.Form):
    pass