from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import password_validation, authenticate
from .models import Transaction
from .API.tickersymbols import us_equities

class UpdatePortfolioForm(forms.ModelForm):

    transaction_type = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]

    transaction = forms.ChoiceField(
        choices=transaction_type,
    )

    transaction_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'name': 'transaction_date',
            })
    )

    symbol = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'symbol',
                'id': 'floatingSymbol',
                'list': 'tickers',
                'placeholder': 'AAPL, AMZN, GOOG, META, MSFT',
            })
    )

    share = forms.DecimalField(
        min_value= 0,
        widget = forms.NumberInput(
            attrs={
                'class': 'form-control',
                'name': 'share',
                'id': 'sharenumber',
                'step': '0.0001',
                'oninput': 'total_calculation();',
            })
    )

    avg_price = forms.DecimalField(
        min_value = 0,
        widget = forms.NumberInput(
            attrs={
                'class': 'form-control',
                'name': 'avg_price',
                'id': 'avgp',
                'oninput': 'total_calculation();',
            })
    )

    commission_fee = forms.DecimalField(
        min_value = 0,
        widget = forms.NumberInput(
            attrs={
                'class': 'form-control',
                'name': 'commission_fee',
                'id': 'commission',
                'value': '0',
                'step': '0.01',
                'oninput': 'total_calculation();',
            })
    )

    cost_basis = forms.DecimalField(
        min_value = 0,
        widget = forms.NumberInput(
            attrs={
                'class': 'form-control',
                'name': 'cost_basis',
                'id': 'costb',
            })
    )

    class Meta:
        model = Transaction
        fields = ['transaction', 'transaction_date', 'symbol', 'share', 'avg_price', 'commission_fee', 'cost_basis']

    def clean_symbol(self):
        symbol = self.cleaned_data.get('symbol').upper()
        if symbol not in us_equities():
            raise forms.ValidationError(f'{symbol} is not a valid ticker symbol')
        return symbol

    def clean_transaction_date(self):
        date = self.cleaned_data.get('transaction_date')
        if date > date.today():
            raise forms.ValidationError('The date cannot be in the future')
        return date
    
    def clean_share(self):
        share = self.cleaned_data.get('share')
        if share <= 0:
            raise forms.ValidationError('Quantity of shares must be more than 0')
        return share

    def clean_avg_price(self):
        avg_price = self.cleaned_data.get('avg_price')
        if avg_price <= 0:
            raise forms.ValidationError('Average price must be more than 0')
        return avg_price
    
    def clean_commission_fee(self):
        commission_fee = self.cleaned_data.get('commission_fee')
        if commission_fee < 0:
            raise forms.ValidationError('Commission fee must be at least 0')
        return commission_fee

class EditProfileForm(forms.Form):

    username = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'username',
            'placeholder': 'Username',
            'readonly': 'readonly',
        }),
    )

    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'name': 'email',
            'id': 'email',
            'placeholder': 'Email Address',
            'type': 'email',
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password',
            'id': 'password',
            'placeholder':'Enter current password',
        }),
    )

    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password1',
            'id': 'password1',
            'placeholder':'Enter new password',
        }),
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password2',
            'id': 'password2',
            'placeholder':'Confirm new password',
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password1', 'password2']

    def clean_password(self):
        """Check whether password is the same as the one in the DB"""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if User.objects.filter(username__exact=username).exists():
            if authenticate(username=username, password=password) is None:
                raise forms.ValidationError("Incorrect password, please try again")
        return password

    def clean_password2(self):
        username = self.cleaned_data['username']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('New passwords do not match')
        if authenticate(username=username, password=password2):
            raise forms.ValidationError("New password cannot be the same as your current password")
        password_validation.validate_password(password2)
        return password2

class ClosePositionForm(UpdatePortfolioForm):
    
    transaction_type = [
        ('SELL', 'Sell')
        ]

    transaction = forms.ChoiceField(
        choices=[('SELL', 'Sell')]
        )

    symbol = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'readonly': 'readonly',
                'class': 'form-control',
                'name': 'symbol',
                'id': 'floatingSymbol',
            })
    )

    share = forms.DecimalField(
        widget = forms.NumberInput(
            attrs={
                'readonly': 'readonly',
                'class': 'form-control',
                'name': 'share',
                'id': 'sharenumber',
                'step': '0.0001',
                'oninput': 'close_total_calculation();',
            })
    )

# class EditTransactionForm(UpdatePortfolioForm):
#     def __init__(self,*args,**kwargs):
#         forms.Form.__init__(self,*args,**kwargs)