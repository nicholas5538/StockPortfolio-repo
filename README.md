<p align="center">
    <img src="/assets/stockstracker.png"/>
</p>

# 💪 Motivation #
During the pandemic, it has spurred a flood of new retail investors into the stock market and I was one of them. Upon using Interactive Brokers, I wasn't satisifed with the amount of clicks I needed to access my investment transactions, the performance of my portfolio and many more. __Hence, I created this project to not only learn more about web development, but to gain a quick insight of my stock portfolio with relative ease and elevated convenience.__

# 📝 About The Project #
### Website URL: **<a href="https://stockstracker-app.herokuapp.com/user/login/" target="_blank">💹 StocksTracker</a>** ###
### Video Demostration: **<a href="https://youtu.be/T_cgG668pf4" target="_blank">StocksTracker Website Demostration</a>** ###
**[StocksTracker](https://stockstracker-app.herokuapp.com/user/login/ "StocksTracker url")** is a web application that allows user to gain a quick insight into the performance of their stock portfolio and investment transactions.

***Note:*** 
1. __Website can only be used in Desktop Fullscreen mode__ since it is not responsive.
2. Heroku will preserve dyno hours from wasting, resulting in __slow loading time for the first hit only__.

#### Tech used: ####

<img align="left" alt="Python" width="40px" src="https://cdn.jsdelivr.net/npm/devicon-2.2@2.2.0/icons/python/python-original.svg" style="padding-right:10px;"/>
<img align="left" alt="django" width="40px" src="https://cdn.jsdelivr.net/npm/devicon-2.2@2.2.0/icons/django/django-original.svg" style="padding-right:10px;"/>
<img align="left" alt="HTML5" width="40px" src="https://cdn.jsdelivr.net/npm/devicon-2.2@2.2.0/icons/html5/html5-original.svg" style="padding-right:10px;"/>
<img align="left" alt="CSS3" width="40px" src="https://cdn.jsdelivr.net/npm/devicon-2.2@2.2.0/icons/css3/css3-original.svg" style="padding-right:10px;" />
<img align="left" alt="JavaScript" width="40px" src="https://cdn.jsdelivr.net/npm/devicon-2.2@2.2.0/icons/javascript/javascript-original.svg" style="padding-right:10px;" />
<img align="left" alt="Bootstrap" width="40px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" style="padding-right:10px;" />
<img align="left" alt="PostgreSQL" width="40px" src="https://cdn.jsdelivr.net/npm/devicon-2.2@2.2.0/icons/postgresql/postgresql-original.svg" style="padding-right:10px;"/>
<img align="left" alt="VScode" width="40px" src="https://cdn.jsdelivr.net/npm/devicon-2.2@2.2.0/icons/visualstudio/visualstudio-plain.svg" style="padding-right:10px;"/> 
<img align="left" alt="Heroku" width="40px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/heroku/heroku-plain-wordmark.svg"/>&nbsp;&nbsp;


### [StocksTracker](https://stockstracker-app.herokuapp.com/user/login/ "StocksTracker url") is split into the following: ###

1. User page

  | Features | Description |
  | --- | --- |
  | Registration | Allows user to create account with unique username and email address |
  | Login | Username and Password input, login authentication is performed with [Django user authentication system](https://docs.djangoproject.com/en/4.1/topics/auth/default/ "Django user authentication system") |
  | Logout | Allows user to logout of web application |
  | Reset Password | Reset password URL will be sent by Email, this is achieved by [Django's SMTP backend](https://docs.djangoproject.com/en/4.1/topics/email/ "Django's SMTP backend") |

<p align="middle">
  <img src="/assets/registration.png" width="49%"/>
  <img src="/assets/login.png" width="49%"/> 
</p>

2. Main page

  | Features | Description |
  | --- | --- |
  | Summary view of portfolio | Display top allocations and holdings of portfolio, most recent transactions, and indices performance |
  | Overall view of portfolio | List all positions in users' portfolio, and other details such as cost basis, average price and net loss/profit |
  | Update investment transaction | Record any buy/sell order of a valid ticker symbol (EX: AAPL, MSFT, META), and delete incorrect orders |
  | Edit Profile | Change user's first name, last name and password |

<p align="middle">
  <img src="/assets/homepage.png" width="32.667%"/>
  <img src="/assets/updateportfolio.png" width="32.667%"/> 
  <img src="/assets/transactionlistview.png" width="32.667%"/> 
</p>

## 💻 Configuration ##
Take note of the following before you runserver:
1. Create an account at [IEX Cloud](https://iexcloud.io/ "IEX Cloud") and [marketstack](https://marketstack.com/ "marketstack")

2. You will only be using these API token:
    - [IEX Cloud](https://iexcloud.io/ "IEX Cloud") public API token ➡️ Live Data
    - [IEX Cloud](https://iexcloud.io/ "IEX Cloud") sandbox API token ➡️ Simulated Data
    - [marketstack](https://marketstack.com/ "marketstack") API token ➡️ Live Data

3. If you choose to utilise another database other than Heroku-PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': # Enter your own database engine,
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT':  # Enter your own database port,
    }
}
```

4. ***Please create a .env file under your root project***

```python
# Input all of these into the .env file
# Enter the relevant values without any quotations!

SECRET_KEY = Enter your own key here
DATABASE_NAME = Enter database name
DATABASE_USER = Enter database user
DATABASE_PASSWORD = Enter database password
DATABASE_HOST = Enter database host
EMAIL_USER = Enter email address
EMAIL_PASSWORD = Enter email password
IEX_TOKEN = Enter IEX token
IEX_SANDBOX_TOKEN = Enter IEX sandbox token
MARKETSTACK_TOKEN = Enter marketstack token
```

5. ***It is advisable to create a virtual environment to test program***

  **Type all of these into the terminal only**

- To create a virtual environment under the root directory:
```
python -m venv venv
```

- To activate virtual environment:
```
venv\Scripts\activate
```

- To deactivate virtual environment:
```
deactivate
```

- To install Python libraries in requirements.txt (Adviseable to do this under virtual environment):
```
pip install -r requirements.txt
```

6. Run project locally

![Virtual Environment codes](https://github.com/nicholas5538/StockPortfolio-repo/blob/main/assets/runlocal.png?raw=true)

## 😔 Challenges faced ##
- Web application is not responsive yet, it can only be used in desktop fullscreen mode
- Loading time exceeds 10 seconds for 2 of the web pages due to lack of knowledge in DSA for optimizing my codes
- Having difficulties applying DOM and CSS properties
- UI of the application need a lot of room for improvement

## 📔 To-do list ##
- [x] Deploy web page to Heroku
- [ ] Make the web page more responsive
- [ ] Implement edit transaction feature