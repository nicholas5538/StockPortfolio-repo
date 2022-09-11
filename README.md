<p align="center">
    <img src="/webimages/stockstracker.png"/>
</p>

# Introduction #
****StocksTracker**** is a web application that allows user to gain a quick insight into the performance of their stock portfolio and investment transaction

The application is split into the following:
- User page
  1. Registration
  2. Login
  3. Logout
  4. Reset Password

<p align="middle">
  <img src="/webimages/registration.png" width="48%"/>
  <img src="/webimages/login.png" width="48%"/> 
</p>

- Main page
  1. Summary view of stock portfolio
  2. Overall view of stock portfolio
  3. Insert / Update / Delete investment transaction
  4. Edit Profile -> Password and name

<p align="middle">
  <img src="/webimages/homepage.png" width="32%"/>
  <img src="/webimages/updateportfolio.png" width="32%"/> 
  <img src="/webimages/transactionlistview.png" width="32%"/> 
</p>

## Configuration ##
Take note of the following before you runserver:
1. Create an account at [IEX Cloud](https://iexcloud.io/ "IEX Cloud title") and [marketstack](https://marketstack.com/ "marketstack title")
2. You will only be using these API token:
    - IEX Cloud public API token
    - IEX Cloud sandbox API token (Simulation and unlimited calls)
    - marketstack API token
3. ***Please change/enter the following codes as shown below***

![Codes](https://github.com/nicholas5538/StockPortfolio-repo/blob/main/webimages/pseudocode.png?raw=true)

4. It is adviseable to run the application in virtual environment:

![Virtual Environment codes](https://github.com/nicholas5538/StockPortfolio-repo/blob/main/webimages/venv.png?raw=true)

## Challenges faced ##
- Web application is not responsive yet, it can only be used in desktop fullscreen mode
- Loading time exceeds 10 seconds for 2 of the web pages due to lack of knowledge in DSA for optimizing my codes
- Having difficulties applying DOM and CSS properties
- UI of the application need a lot of room for improvement

### To-do list ###
- [ ] Deploy web page to Heroku
- [ ] Make the web page more responsive
- [ ] Implement modal forms
- [ ] Implement edit transaction feature