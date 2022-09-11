from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class UserTestSetUp(StaticLiveServerTestCase):

    def setUp(self):
        # self.browser = webdriver.Chrome(executable_path=""C:/Users/nicho/Desktop/Python/StocksTracker/StockPortfolio-repo/chromedriver.exe")
        self.browser = webdriver.Edge(executable_path="C:/Users/nicho/Desktop/Python/StocksTracker/StockPortfolio-repo/msedgedriver.exe")
        self.username = "weiwei123"
        self.email = "weiwei123@gmail.com"
        self.password1 = "123Frivolous"
        self.password2 = "123Frivolous"
        self.first_name = "Wei"
        self.last_name = "Xuan"
        self.new_user = User.objects.create_user(
            self.username, self.email, self.password1,
            first_name = self.first_name,
            last_name = self.last_name
        )
        self.pk = self.new_user.id
        return super(UserTestSetUp, self).setUp()

    def tearDown(self):
        # self.browser.close()
        self.browser.quit()
        

class TestLoginPage(UserTestSetUp):

    def setUp(self):
        self.login_url = f'{self.live_server_url}/user/login/'
        return super(TestLoginPage, self).setUp()

    def test_login_valid(self):
        self.browser.get(self.login_url)
        self.browser.find_element(By.ID, 'floatingUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'floatingPassword').send_keys(self.password1)
        redirect_url = f'{self.live_server_url}/main/{self.pk}/home/'
        self.browser.find_element(By.ID, 'loginBtn').click()
        self.assertEqual(self.browser.current_url, redirect_url)

    def test_login_invalid(self):
        self.browser.get(self.login_url)
        self.browser.find_element(By.ID, 'floatingUsername').send_keys(self.username)
        self.browser.find_element(By.ID, 'floatingPassword').send_keys('123456789')
        invalid_url = f'{self.live_server_url}/user/login/?next=None'
        self.browser.find_element(By.ID, 'loginBtn').click()
        invalid_detail = self.browser.find_element(By.CLASS_NAME, 'noaccess').text
        self.assertEqual(self.browser.current_url, invalid_url)
        self.assertEqual(invalid_detail, 'You do not have access to this page, login to proceed')

    def test_forget_password_link(self):
        self.browser.get(self.login_url)
        forget_pw_url = f'{self.live_server_url}/user/reset-password/'
        self.browser.find_element(By.LINK_TEXT, 'Forgotten password?').click()
        self.assertEqual(self.browser.current_url, forget_pw_url)

    def test_create_account_link(self):
        self.browser.get(self.login_url)
        register_url = f'{self.live_server_url}/user/register/'
        self.browser.find_element(By.LINK_TEXT, 'Create New Account').click()
        self.assertEqual(self.browser.current_url, register_url)
           

class TestResetPasswordPage(UserTestSetUp):

    def setUp(self):
        self.reset_url = f'{self.live_server_url}/user/reset-password/'
        return super(TestResetPasswordPage, self).setUp()   

    def test_reset_password_valid_email(self):
        self.browser.get(self.reset_url)
        self.browser.find_element(By.ID, 'floatingEmail').send_keys(self.email)
        redirect_url = f'{self.live_server_url}/user/reset-password-sent/'
        self.browser.find_element(By.CSS_SELECTOR, 'button').click()
        self.assertEqual(self.browser.current_url, redirect_url)

    def test_reset_password_invalid_email(self):
        self.browser.get(self.reset_url)
        self.browser.find_element(By.ID, "floatingEmail").send_keys("123456@gmail.com")
        self.browser.find_element(By.CSS_SELECTOR, 'button').click()
        error = self.browser.find_element(By.CSS_SELECTOR, 'li').text
        self.assertEqual(error, 'This email is not registered')