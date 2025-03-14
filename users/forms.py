from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput)

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if not CustomUser.objects.filter(email=email).exists():
    #         raise ValidationError(f'That {email} not found.')
    #     return email
    #
    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if not CustomUser.objects.filter(password=password).exists():
    #         raise ValidationError(f'Password did not match')
    #
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get("email")
    #     password = cleaned_data.get("password")
    #
    #     if not email or not password:
    #         raise forms.ValidationError("Username or password invalid")
    #
    #     return cleaned_data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Parollar mos kelmadi!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
