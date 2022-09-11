![alt text](https://github.com/nicholas5538/StockPortfolio-repo/blob/main/stockstracker.png?raw=true)
# Introduction #
****StocksTracker**** is a web application that allows user to gain a quick insight into the performance of their stock portfolio and investment transaction

The application is split into the following:
- User page
  1. Registration
  2. Login
  3. Logout
  4. Reset Password
- Main page
  1. Summary view of stock portfolio
  2. Overall view of stock portfolio
  3. Insert / Update / Delete investment transaction
  4. Edit Profile -> Password and name

## Configuration ##
Take note of the following before you runserver:
1. Create an account at [IEX Cloud](https://iexcloud.io/ "IEX Cloud title") and [marketstack](https://marketstack.com/ "marketstack title")
2. You will only be using these API token:
    - IEX Cloud public API token
    - IEX Cloud sandbox API token (Simulation and unlimited calls)
    - marketstack API token
3. ***Please change/enter the following codes as shown below***

![alt text](https://github.com/nicholas5538/StockPortfolio-repo/blob/main/code.png?raw=true)

4. It is adviseable to run the application in virtual environment:

![alt text](https://github.com/nicholas5538/StockPortfolio-repo/blob/main/venv.png?raw=true)

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