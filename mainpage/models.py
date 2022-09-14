from django.db import models
from django.contrib.auth.models import User

class TickerSymbols(models.Model):
    tickersymbol = models.CharField(max_length=10)

    def __str__(self):
        return self.tickersymbol

class Transaction(models.Model):
    buy = 'BUY'
    sell = 'SELL'
    transaction_type = [
        (buy, 'Buy'),
        (sell, 'Sell'),
    ]

    transaction = models.CharField(
        max_length=200,
        choices=transaction_type,
        default=buy,
    )

    symbol = models.CharField(max_length=10)
    transaction_date = models.DateField()
    share = models.DecimalField(decimal_places=4, max_digits=20)
    avg_price = models.DecimalField(decimal_places=8, max_digits=20)
    commission_fee = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    cost_basis = models.DecimalField(decimal_places=8, max_digits=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    company_name = models.CharField(max_length=100)
    total_shares = models.DecimalField(decimal_places=4, max_digits=20)
    avg_price = models.DecimalField(decimal_places=8, max_digits=20)
    cost_basis = models.DecimalField(decimal_places=8, max_digits=20)
    current_value = models.DecimalField(decimal_places=8, max_digits=20)
    profit_loss = models.DecimalField(decimal_places=8, max_digits=20)

# To run under py manage.py shell:

# from mainpage.models import TickerSymbols
# from mainpage.API.tickersymbols import us_equities
# tickers = us_equities()
# objs = [TickerSymbols(tickersymbol=ticker) for ticker in tickers]
# TickerSymbols.objects.bulk_create(objs)