from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from mainpage.models import Transaction, Portfolio
from mainpage.API.tickersymbols import company_quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from decimal import Decimal

# Create your tests here
class UserTestCase(StaticLiveServerTestCase):

    def setUp(self):
        # self.browser = webdriver.Chrome(executable_path="C:/Users/nicho/Desktop/Python/python_work/Portfolio/stockstracker/chromedriver.exe")
        self.browser = webdriver.Edge(executable_path="C:/Users/nicho/Desktop/Python/python_work/Portfolio/stockstracker/msedgedriver.exe")
        self.username = "weiwei123"
        self.email = "weiwei123@gmail.com"
        self.password1 = "123Frivolous"
        self.password2 = "123Frivolous"
        self.first_name = "Wei"
        self.last_name = "Xuan"
        self.pk = 999
        self.user = {
            'username': self.username,
            'password': self.password1,
            }
        User.objects.create_user(
            self.username, self.email, self.password1,
            first_name = self.first_name,
            last_name = self.last_name,
            pk = self.pk
            )
        Transaction.objects.create(
            id=self.pk, transaction='BUY', symbol='AAPL', 
            transaction_date='2021-01-01', share=1, avg_price=1,
            cost_basis=1, user_id=self.pk, commission_fee=0.37
            )
        aapl_quote = company_quote('AAPL')
        Portfolio.objects.create(
            id=self.pk, total_shares=1, user_id=self.pk,
            symbol='AAPL', company_name=aapl_quote['companyName'], avg_price=1,
            cost_basis=1.37, current_value=Decimal(aapl_quote['latestPrice']), profit_loss=Decimal(aapl_quote['latestPrice'] - 1.37)
            )

        self.login_url = reverse('users:login')
        return super(UserTestCase, self).setUp()

    def tearDown(self):
        self.browser.quit()

class HomeViewTestCase(UserTestCase):

    def setUp(self):
        self.home_url = reverse('mainpage:home', args=['999'])
        return super(HomeViewTestCase, self).setUp()

    def test_home_view(self):
        response = self.client.post(self.login_url, self.user, format='text/html')
        login_status = self.client.login(username=self.username, password=self.password1)
        self.assertTrue(login_status)
        self.assertRedirects(response, self.home_url, status_code=302, target_status_code=200)

    def test_noaccess_redirect(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
                response, f'{self.login_url}?next={self.home_url}', 
                status_code=302, target_status_code=200
                )
    
class PortfolioViewTestCase(UserTestCase):
    
    def setUp(self):
        self.portfolio_url = f'{self.live_server_url}/main/999/portfolio/'
        super(PortfolioViewTestCase, self).setUp()

    def test_portfolio_view(self):
        self.browser.get(self.portfolio_url)
        self.browser.find_element(By.ID, 'floatingUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'floatingPassword').send_keys(self.password1)
        self.browser.find_element(By.ID, 'loginBtn').click()
        position = self.browser.find_element(By.TAG_NAME, 'td').text
        self.assertEqual(self.browser.current_url, self.portfolio_url)
        self.assertEqual(float(position), 1.0000)

    def test_noaccess_redirect(self):
        self.browser.get(self.portfolio_url)
        redirect_url = f'{self.live_server_url}/user/login/?next=/main/999/portfolio/'
        no_access = self.browser.find_element(By.CLASS_NAME, 'noaccess').text
        self.assertEqual(self.browser.current_url, redirect_url)
        self.assertEqual(no_access, 'You do not have access to this page, login to proceed')


class UpdatePortfolioViewTestCase(UserTestCase):

    def setUp(self):
        self.updateportfolio_url = f'{self.live_server_url}/main/999/update-portfolio/'
        super(UpdatePortfolioViewTestCase, self).setUp()

    def test_updateportfolio_view(self):
        self.browser.get(self.updateportfolio_url)
        self.browser.find_element(By.ID, 'floatingUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'floatingPassword').send_keys(self.password1)
        self.browser.find_element(By.ID, 'loginBtn').click()
        self.assertEqual(self.browser.current_url, self.updateportfolio_url)

    def test_noaccess_redirect(self):
        self.browser.get(self.updateportfolio_url)
        redirect_url = f'{self.live_server_url}/user/login/?next=/main/{self.pk}/update-portfolio/'
        no_access = self.browser.find_element(By.CLASS_NAME, 'noaccess').text
        self.assertEqual(self.browser.current_url, redirect_url)
        self.assertEqual(no_access, 'You do not have access to this page, login to proceed')


class TransactionsViewTestCase(UserTestCase):
    
    def setUp(self):
        self.transactions_url = f'{self.live_server_url}/main/999/transactions/'
        return super(TransactionsViewTestCase, self).setUp()

    def test_transactions_view(self):
        self.browser.get(self.transactions_url)
        self.browser.find_element(By.ID, 'floatingUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'floatingPassword').send_keys(self.password1)
        self.browser.find_element(By.ID, 'loginBtn').click()
        self.assertEqual(self.browser.current_url, self.transactions_url)

    def test_noaccess_redirect(self):
        self.browser.get(self.transactions_url)
        redirect_url = f'{self.live_server_url}/user/login/?next=/main/999/transactions/'
        no_access = self.browser.find_element(By.CLASS_NAME, 'noaccess').text
        self.assertEqual(self.browser.current_url, redirect_url)
        self.assertEqual(no_access, 'You do not have access to this page, login to proceed')


class EditProfileViewTestCase(UserTestCase):
    
    def setUp(self):
        self.edit_profile_url = f'{self.live_server_url}/main/999/edit-profile/'
        return super(EditProfileViewTestCase, self).setUp()

    def test_edit_profile_view(self):
        self.browser.get(self.edit_profile_url)
        self.browser.find_element(By.ID, 'floatingUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'floatingPassword').send_keys(self.password1)
        self.browser.find_element(By.ID, 'loginBtn').click()
        self.assertEqual(self.browser.current_url, self.edit_profile_url)

    def test_noaccess_redirect(self):
        self.browser.get(self.edit_profile_url)
        redirect_url = f'{self.live_server_url}/user/login/?next=/main/999/edit-profile/'
        no_access = self.browser.find_element(By.CLASS_NAME, 'noaccess').text
        self.assertEqual(self.browser.current_url, redirect_url)
        self.assertEqual(no_access, 'You do not have access to this page, login to proceed')


class DeleteTransactionViewTestCase(UserTestCase):

    def setUp(self):
        self.delete_transaction_url = f'{self.live_server_url}/main/999/delete-transaction/'
        return super(DeleteTransactionViewTestCase, self).setUp()

    def test_delete_transaction_view(self):
        self.browser.get(self.delete_transaction_url)
        self.browser.find_element(By.ID, 'floatingUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'floatingPassword').send_keys(self.password1)
        self.browser.find_element(By.ID, 'loginBtn').click()
        transaction_type = self.browser.find_element(By.TAG_NAME, 'td').text
        transaction_model = Transaction.objects.get(id__exact=self.pk).transaction
        self.assertEqual(self.browser.current_url, self.delete_transaction_url)
        self.assertEqual(transaction_type, transaction_model)

    def test_noaccess_redirect(self):
        self.browser.get(self.delete_transaction_url)
        redirect_url = f'{self.live_server_url}/user/login/?next=/main/999/delete-transaction/'
        no_access = self.browser.find_element(By.CLASS_NAME, 'noaccess').text
        self.assertEqual(self.browser.current_url, redirect_url)
        self.assertEqual(no_access, 'You do not have access to this page, login to proceed')


class ClosePositionViewTestCase(UserTestCase):
    
    def setUp(self):
        self.close_position_url = f'{self.live_server_url}/main/999/close-position/'
        return super(ClosePositionViewTestCase, self).setUp()

    def test_close_position_view(self):
        self.browser.get(self.close_position_url)
        self.browser.find_element(By.ID, 'floatingUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'floatingPassword').send_keys(self.password1)
        self.browser.find_element(By.ID, 'loginBtn').click()
        transaction_type = self.browser.find_element(By.CSS_SELECTOR, 'option#sell').text
        self.assertEqual(self.browser.current_url, self.close_position_url)
        self.assertEqual(transaction_type, 'Sell')

    def test_noaccess_redirect(self):
        self.browser.get(self.close_position_url)
        redirect_url = f'{self.live_server_url}/user/login/?next=/main/999/close-position/'
        no_access = self.browser.find_element(By.CLASS_NAME, 'noaccess').text
        self.assertEqual(self.browser.current_url, redirect_url)
        self.assertEqual(no_access, 'You do not have access to this page, login to proceed')