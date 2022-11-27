from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, TemplateView
from mainpage.models import Portfolio, Transaction, TickerSymbols
from .forms import UpdatePortfolioForm, EditProfileForm, ClosePositionForm
from .API.tickersymbols import *
from datetime import datetime
from decimal import Decimal

class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'mainpage/home.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id
        tickers = TickerSymbols.objects.all()
        portfolio = Portfolio.objects.filter(user_id=current_user).order_by('-current_value')
        buy_transactions = Transaction.objects.filter(user_id=current_user, transaction='BUY').order_by('-transaction_date')
        sell_transactions = Transaction.objects.filter(user_id=current_user, transaction='SELL').order_by('-transaction_date')
        indices = indices_performance()

        positions = portfolio.count()    
        if positions > 0:
            if positions >= 5:
                positions = 5
            top_tickers = []
            top_shares = []
            for position in portfolio[:positions]:
                top_tickers.append(position.symbol)
                top_shares.append(position.total_shares)
            latest_prices = get_latest_price(top_tickers)
            current_value = [shares * latest_price for shares, latest_price in zip(top_shares, latest_prices)]
            net_liquidity = sum(current_value)
            allocation_percentages = [(value/net_liquidity * 100) for value in current_value]
            top_holdings = zip(top_tickers, latest_prices, current_value)
            allocation = zip(top_tickers, allocation_percentages)
        else:
            top_holdings, net_liquidity, allocation = ([] for i in range(3))

        fields = [
                'tickers', 'buy_transactions', 'sell_transactions', 
                'top_holdings', 'net_liquidity', 'spy', 
                'nasdaq', 'djia', 'allocation'
                ]
        values = [
            tickers, buy_transactions, sell_transactions, 
            top_holdings, net_liquidity, indices['SPY'], 
            indices['QQQ'], indices['DIA'], allocation
            ]
        for field, value in zip(fields, values):
            context[field] = value
        return context


class PortfolioView(LoginRequiredMixin, TemplateView):
    
    template_name = 'mainpage/portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user.id
        tickers = TickerSymbols.objects.all()
        portfolio = Portfolio.objects.filter(user_id=current_user).order_by('company_name')
        date = datetime.today().strftime('%d %b %Y %I:%M:%S %p')
        daily_percentage_changes, latest_prices = [], []
        daily_profit_loss = net_liquidity = net_profit_loss = 0
        positions = [position.symbol for position in portfolio]
        company_infos = company_quotes(positions)            
        for index, company in enumerate(company_infos):
            position = Portfolio.objects.filter(user_id=current_user, company_name__exact=company[0])
            previous_close = Decimal(company[2])
            latest_prices.append(Decimal(company[1]))
            total_shares = position.values('total_shares')[0].get('total_shares')
            current_value = latest_prices[index] * total_shares
            profit_loss = latest_prices[index] - previous_close
            daily_percentage_changes.append(profit_loss/previous_close * 100)
            daily_profit_loss += profit_loss * total_shares
            net_profit_loss += position.values('profit_loss')[0].get('profit_loss')
            net_liquidity += current_value
            position.update(current_value=current_value, profit_loss=current_value-position.values('cost_basis')[0].get('cost_basis'))

        context_fields = [
            'tickers', 
            'portfolio', 
            'portfolio_details', 
            'date', 
            'daily_profit_loss', 
            'net_liquidity', 
            'net_profit_loss'
            ]
        values = [
            tickers, 
            portfolio, 
            zip(daily_percentage_changes, latest_prices, portfolio), 
            date, 
            daily_profit_loss, 
            net_liquidity, 
            net_profit_loss
            ]

        for field, value in zip(context_fields, values):
            context[field] = value
        return context


class UpdatePortfolioView(LoginRequiredMixin, FormView):
    
    form_class = UpdatePortfolioForm
    template_name = 'mainpage/update_portfolio.html'

    def message(self, text):
        return messages.add_message(self.request, messages.INFO, text)

    def get_success_url(self):
        return reverse('mainpage:transactions', kwargs={'pk': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickers'] = TickerSymbols.objects.all()
        return context

    def form_invalid(self, form):
        name_list = [
            'transaction', 'symbol', 'transaction_date', 
            'share', 'avg_price', 'cost_basis'
            ]
        # Print all applicable form fields
        [print(f"{name}: {form.cleaned_data.get(name)}") for name in name_list]
        # Print error(s) 
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        transaction_form = form.save(commit=False)
        symbol = form.cleaned_data.get('symbol').upper()
        share = form.cleaned_data.get('share')
        average_price = form.cleaned_data.get('avg_price')
        total_cost = form.cleaned_data.get('cost_basis')
        transaction = form.cleaned_data.get('transaction')
        transaction_form.user_id = self.request.user.id
        transaction_form.symbol = symbol

        # API requests to extract appropriate data
        company_info = company_quotes(symbol)
        existing_position = Portfolio.objects.filter(user_id=self.request.user.id, symbol__exact=symbol)
        latest_price = Decimal(company_info[1])
        new_entry = {
            'avg_price': average_price,
            'company_name': company_info[0],
            'cost_basis': total_cost,
            'current_value': share * latest_price,
            'profit_loss': share * latest_price - total_cost,
            'symbol': symbol,
            'total_shares': share,
        }

        # Check if there is any existing position before selling
        if transaction == 'SELL' and not existing_position.exists():
            self.message(f'Fail to sell, you currently do not have any position in {symbol}')
            return super().form_invalid(form)

        position, created = Portfolio.objects.get_or_create(
                                            symbol__exact=symbol, 
                                            user_id=self.request.user.id,
                                            defaults=new_entry
                                            )

        if created:
            message = f"Successfully opened a new position in {symbol}"
        
        while not created:
            current_shares = position.total_shares
            current_cost_basis = position.cost_basis
            # Check whether selling position is bigger than existing position
            if transaction == 'SELL':
                updated_shares = current_shares - share
                if updated_shares < 0:
                    self.message(f'Fail to sell, do not exceed {current_shares} {symbol} shares')
                    return super().form_invalid(form)
                elif updated_shares > 0:
                    updated_cost_basis = current_cost_basis - total_cost
                    message = f"Sale of {share} {symbol} share(s) has been updated to your portfolio"
                else:
                    position.delete()
                    break
            else:
                updated_shares = current_shares + share
                updated_cost_basis = current_cost_basis + total_cost
                message = f"Purchase of {share} {symbol} share(s) has been updated to your portfolio"

            updated_avg_price = updated_cost_basis / updated_shares
            updated_current_value = updated_shares * latest_price
            updated_pl = updated_current_value - updated_cost_basis
            # Update Portfolio database
            position.total_shares=updated_shares,
            position.cost_basis=updated_cost_basis,
            position.avg_price=updated_avg_price,
            position.current_value=updated_current_value,
            position.profit_loss=updated_pl
            position.save()
            break
            
        transaction_form.save()
        self.message(message)
        if 'confirm' in self.request.POST:
            # Redirect to URL under get_success_url
            return super().form_valid(form)
        # if 'Submit and add another' button is clicked
        return redirect(reverse('mainpage:update', kwargs={'pk': self.request.user.id}))


class TransactionsListView(LoginRequiredMixin, ListView):
    
    model = Transaction
    template_name = 'mainpage/transactions.html'
        
    def get_queryset(self):
        queryset = super().get_queryset()
        # Get data from the correct user
        transaction_queryset = queryset.filter(user_id=self.request.user.id).order_by('-transaction_date')
        return transaction_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()
        # Extract first 5 transactions for 'BUY' & 'SELL'
        context['username'] = get_object_or_404(User, pk=self.request.user.id)
        context['tickers'] = TickerSymbols.objects.all()
        context['buy_transactions'] = transactions.filter(transaction='BUY').order_by('-transaction_date')
        context['sell_transactions'] = transactions.filter(transaction='SELL').order_by('-transaction_date')
        return context


class EditProfileView(LoginRequiredMixin, FormView):
    
    form_class = EditProfileForm
    template_name = 'mainpage/edit_profile.html'

    def default_data(self, form):
        current_user = User.objects.get(id__exact=self.request.user.id)
        context = {
            'form': form,
            'tickers': TickerSymbols.objects.all(),
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name
        }
        return context

    def get(self, request, pk):
        form = self.form_class(initial={'username': User.objects.get(id__exact=pk).username})
        return render(request, self.template_name, self.default_data(form))

    def post(self, request, pk):
        form = self.form_class(request.POST)
        current_user = User.objects.get(id__exact=pk)
        old_credentials = [current_user.email, current_user.first_name, current_user.last_name]
        new_credentials = [request.POST.get('email'), request.POST.get('firstname').capitalize(), request.POST.get('lastname').capitalize()]
        for old_credential, new_credential in zip(old_credentials, new_credentials):
            if new_credential != '' and new_credential != old_credential:
                current_user.old_credential = new_credential
        current_user.save()

        if form.is_valid():
            new_password = request.POST['password2']
            if new_password != 'None':
                current_user.set_password(request.POST['password2'])
                current_user.save()
                update_session_auth_hash(request, current_user)
            messages.add_message(request, messages.SUCCESS, 'Profile details updated!')
        else:
            print(form.errors)
        return render(request, self.template_name, self.default_data(form))


class ClosePositionView(LoginRequiredMixin, FormView):

    form_class = ClosePositionForm
    template_name = 'mainpage/close_position.html'

    def get_success_url(self):
        return reverse('mainpage:portfolio', kwargs={'pk': self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        tickers = TickerSymbols.objects.all()
        position = Portfolio.objects.get(user_id=user_id, id=self.kwargs['pk'])
        shares = position.total_shares
        #input initial data to form
        initial_data = {
            'transaction': 'Sell',
            'symbol': position.symbol,
            'share': shares,
            }
        form = self.form_class(initial=initial_data)
        context['position'] = position
        context['tickers'] = tickers
        context['form'] = form
        return context

    def form_invalid(self, form):
        fields = [
            'transaction', 'symbol', 'transaction_date', 
            'share', 'avg_price', 'commission_fee', 
            'cost_basis', 
            ]
        # Print all applicable form fields
        [print(f'{field}: {form.cleaned_data.get(field)}') for field in fields]
        # Print error(s) 
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        current_user = self.request.user.id
        close_position = form.save(commit=False)
        close_position.user_id = current_user
        close_position.save()
        symbol = form.cleaned_data.get('symbol')
        Portfolio.objects.get(user_id=current_user, symbol__exact=symbol).delete()
        messages.add_message(self.request, messages.INFO, f'Your {symbol} position has been fully closed')
        return super().form_valid(form)


class DeleteTransactionView(LoginRequiredMixin, TemplateView):

    template_name = 'mainpage/delete_transaction.html'

    def message(self, texts):
        return messages.add_message(self.request, messages.INFO, texts)

    def get(self, request, **kwargs):
        tickers = TickerSymbols.objects.all()
        transaction = Transaction.objects.get(id=kwargs['pk'])
        context = {'tickers': tickers, 'transaction': transaction}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        current_user = request.user.id
        transaction = Transaction.objects.get(id=kwargs['pk'])
        transaction_type = transaction.transaction
        symbol = transaction.symbol
        share = transaction.share
        # Condition 1: Delete 'Sell' with no current position
        try:
            position = Portfolio.objects.get(symbol__exact=symbol, user_id=current_user)
            position_shares = position.total_shares
            if transaction_type == 'SELL':
                update_shares = position_shares + share
            else: 
                update_shares = position_shares - share
        except Portfolio.DoesNotExist:
            if transaction_type == 'SELL':
                self.message(f'Please open a new position on {symbol} with this form')
                return redirect(reverse('mainpage:update', kwargs={'pk': current_user}))
            self.message('You do not have any existing position to sell')
            return redirect(reverse('mainpage:transactions', kwargs={'pk': current_user}))
        else:
            # Condition 2: Delete 'Sell' or 'BUY' with existing position
            message = 'Transaction has been deleted'
            if update_shares > 0:
                total_shares = cost_basis = 0
                transaction.delete()
                transaction_queryset = Transaction.objects.filter(user_id=current_user, symbol__exact=symbol)
                for query in transaction_queryset.values('transaction', 'share', 'avg_price'):
                    shares = query['share']
                    if query['transaction'] == 'BUY':
                        total_shares += shares
                        cost_basis += shares * query['avg_price']
                    else:
                        total_shares -= shares
                        cost_basis -= shares * query['avg_price']
                
                current_value = get_latest_price(symbol) * total_shares
                position.total_shares = total_shares
                position.avg_price = cost_basis / total_shares
                position.cost_basis = cost_basis
                position.current_value = current_value
                position.profit_loss = current_value - cost_basis 
                position.save()

            # Condition 3: Delete 'BUY' and new shares is 0
            elif update_shares == 0: 
                transaction.delete()
                position.delete()
            # Condition 4: Delete 'BUY' but new shares < 0
            else:
                message = f'Fail to delete, you do not have enough {symbol} shares'

        self.message(message)
        return redirect(reverse('mainpage:transactions', kwargs={'pk': current_user}))