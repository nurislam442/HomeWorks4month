from django import forms
from django.contrib.auth.models import User

class Registerform(forms.ModelForm):
    password_confirm = forms.CharField(required=True)
    age = forms.IntegerField()
    image = forms.ImageField()
    class Meta:
        model = User
        fields = ["image", "username", "age", "password", "password_confirm"]
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if (password and password_confirm) and (password != password_confirm):
            raise forms.ValidationError("пароли не совподают")
        return cleaned_data
    
class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput)
        