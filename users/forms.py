from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation, authenticate

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'email',
            'id': 'floatingInput',
            'placeholder': 'Email address',
        }),
    )

    username = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'floatingUsername',
            'placeholder': 'Username'
        }),
    )

    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'first_name',
            'id': 'floatingFirstName',
            'placeholder': 'First name'
        }),
    )

    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'last_name',
            'id': 'floatingLastName',
            'placeholder': 'Surname'
        }),
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password1',
            'id': 'floatingPassword',
            'placeholder':'Password',
        }),
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password2',
            'id': 'floatingConfirmPassword',
            'placeholder':'Confirm password',
        }),
    )

    class Meta:
        model = User
        fields = [
            'email',
            'username', 
            'first_name', 
            'last_name',
            'password1',
            'password2',
            ]

    def clean_email(self):
        """Email validation"""
        email = self.cleaned_data.get('email')
        email_check = User.objects.filter(email__exact=email)
        if email_check.exists():
            raise forms.ValidationError("Email address already exists")
        return email

    def clean_username(self):
        """Username validation"""
        username = self.cleaned_data.get('username')
        username_check = User.objects.filter(username__exact=username)
        if username_check.exists():
            raise forms.ValidationError("Username already exists")
        return username

    # Password validation errors
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        password_validation.validate_password(password2)
        return password2

class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'floatingUsername',
            'placeholder': 'Username'
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password',
            'id': 'floatingPassword',
            'placeholder':'Password',
        }),
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'password',
            ]

    def get_current_user(self, username):
        return User.objects.filter(username__exact=username)

    def clean_username(self):
        """Username validation"""
        username = self.cleaned_data.get('username')
        if not self.get_current_user(username).exists():
            raise forms.ValidationError("User does not exist")
        return username

    def clean_password(self):
        """Check whether password is the same as the one in the DB"""
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if self.get_current_user(username).exists():
            if authenticate(username=username, password=password) is None:
                raise forms.ValidationError("Incorrect password, please try again")
        return password

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'name': 'email',
            'id': 'floatingEmail',
            'placeholder': 'Email Address',
            'type': 'email',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__exact=email).exists():
            raise forms.ValidationError("This email is not registered")
        return email

class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password1',
            'id': 'floatingPassword1',
            'placeholder':'New Password',
        }),
    )

    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password2',
            'id': 'floatingPassword2',
            'placeholder':'Confirm Password',
        }),
    )

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match, please try again")
        password_validation.validate_password(new_password2)
        return new_password2