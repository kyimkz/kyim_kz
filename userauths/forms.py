from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from userauths.models import User, Profile
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={ "placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    captcha = ReCaptchaField()

    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={ "placeholder": "Full Name"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={ "placeholder": "Phone"}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'phone']

class SetNewPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))

    captcha = ReCaptchaField()