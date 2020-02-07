from django import forms
from django.contrib.auth.models import User
# from phonenumber_field.formfields import PhoneNumberField
class PhonLoginForm(forms.Form):
    phone=forms.CharField(max_length=12)
    def clean_phone(self):
        phone=User.objects.filter(username=self.cleaned_data['phone'])
        if not phone.exists():
            raise forms.ValidationError('this phone dose not exists')
        return self.cleaned_data['phone']

class verifyCodeForm(forms.Form):
    code=forms.IntegerField()