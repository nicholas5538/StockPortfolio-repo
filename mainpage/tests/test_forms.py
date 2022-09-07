from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from mainpage.forms import UpdatePortfolioForm, EditProfileForm, ClosePositionForm
from mainpage.models import Transaction, Portfolio
from mainpage.API.tickersymbols import company_quote
from decimal import Decimal

class UserTestSetUp(TestCase):

    def setUp(self):
        self.username = "weiwei123"
        self.email = "weiwei123@gmail.com"
        self.password1 = "123Frivolous"
        self.password2 = "123Frivolous"
        self.first_name = "Wei"
        self.last_name = "Xuan"
        self.new_user = User.objects.create_user(
            self.username, self.email, self.password1,
            first_name = self.first_name,
            last_name = self.last_name,
            pk = 999
            )
        return super(UserTestSetUp, self).setUp()


class UpdatePortfolioFormTest(UserTestSetUp):

    def setUp(self):
        self.transaction = {
            'transaction': 'BUY',
            'transaction_date': '2022-01-01',
            'symbol': 'AAPL',
            'share': 1,
            'avg_price': 1,
            'commission_fee': 1,
            'cost_basis': 2 
            }
        self.invalid_ticker= {
            'transaction': 'BUY',
            'transaction_date': '2022-01-01',
            'symbol': '123456789',
            'share': 1,
            'avg_price': 1,
            'commission_fee': 1,
            'cost_basis': 2 
            }
        self.invalid_date = {
            'transaction': 'BUY',
            'transaction_date': '2122-01-01',
            'symbol': 'AAPL',
            'share': 1,
            'avg_price': 1,
            'commission_fee': 1,
            'cost_basis': 2 
            }
        self.negative_number = {
            'transaction': 'BUY',
            'transaction_date': '2022-01-01',
            'symbol': 'AAPL',
            'share': 0,
            'avg_price': 0,
            'commission_fee': -1,
            'cost_basis': 2,
            }
        return super(UpdatePortfolioFormTest, self).setUp()

    def test_valid_form(self):
        form = UpdatePortfolioForm(data=self.transaction)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = UpdatePortfolioForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)

    def test_invalid_ticker(self):
        form = UpdatePortfolioForm(data=self.invalid_ticker)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_invalid_date(self):
        form = UpdatePortfolioForm(data=self.invalid_date)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_negative_number(self):
        form = UpdatePortfolioForm(data=self.negative_number)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
    

class EditProfileFormTest(UserTestSetUp):

    def setUp(self):
        self.user = {
            'username': 'weiwei123', 'password': '123Frivolous',
            'password1':'456Frivolous', 'password2':'456Frivolous',
            }
        self.incorrect_password = {
            'username': 'weiwei123', 'password': '456Frivolous',
            'password1':'789Frivolous', 'password2':'789Frivolous',
            }
        self.passwords_unmatched = {
            'username': 'weiwei123', 'password': '123Frivolous',
            'password1':'789Frivolous', 'password2':'456Frivolous',
            }
        self.same_password = {
            'username': 'weiwei123', 'password': '123Frivolous',
            'password1': '123Frivolous', 'password2': '123Frivolous',
            }
        return super(EditProfileFormTest, self).setUp()

    def test_valid_form(self):
        form = EditProfileForm(data=self.user)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = EditProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
    
    def test_incorrect_password_form(self):
        form = EditProfileForm(data=self.incorrect_password)
        self.assertFalse(form.is_valid())
        self.assertEqual([error for error in form.errors][0], 'password')

    def test_passwords_unmatched_form(self):
        form = EditProfileForm(data=self.passwords_unmatched)
        self.assertFalse(form.is_valid())
        self.assertEqual([error for error in form.errors][0], 'password2')

    def test_same_password_form(self):
        form = EditProfileForm(data=self.same_password)
        self.assertFalse(form.is_valid())
        self.assertEqual([error for error in form.errors][0], 'password2')

class ClosePositionFormTest(TestCase):

    def setUp(self):
        self.close_position = {
            'transaction': 'SELL',
            'transaction_date': '2022-01-01',
            'symbol': 'AAPL',
            'share': 1,
            'avg_price': 1,
            'commission_fee': 1,
            'cost_basis': 2 
            }
        self.invalid_date = {
            'transaction': 'SELL',
            'transaction_date': '2100-01-01',
            'symbol': 'AAPL',
            'share': 1,
            'avg_price': 1,
            'commission_fee': 1,
            'cost_basis': 2 
            }
        self.negative_number = {
            'transaction': 'SELL',
            'transaction_date': '2022-01-01',
            'symbol': 'AAPL',
            'share': 1,
            'avg_price': 0,
            'commission_fee': -1,
            'cost_basis': 2,
            }
        return super(ClosePositionFormTest, self).setUp()

    def test_valid_form(self):
        form = ClosePositionForm(data=self.close_position)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = ClosePositionForm(data={})
        self.assertFalse(form.is_valid())
        for message in form.errors.values():
            self.assertEqual(message, ['This field is required.'])
        self.assertEqual(len(form.errors), 7)

    def test_invalid_date(self):
        form = ClosePositionForm(data=self.invalid_date)
        self.assertFalse(form.is_valid())
        error = form.errors
        self.assertEqual(error['transaction_date'], ['The date cannot be in the future'])
        self.assertEqual(len(error), 1)

    def test_negative_number(self):
        form = ClosePositionForm(data=self.negative_number)
        self.assertFalse(form.is_valid())
        error = form.errors
        self.assertEqual(error['avg_price'], ['Average price must be more than 0'])
        self.assertEqual(error['commission_fee'], ['Ensure this value is greater than or equal to 0.'])
        self.assertEqual(len(error), 2)