from pickle import NONE
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView
from django.urls import reverse
from urllib.parse import urlencode
from .forms import RegisterForm, LoginForm
from string import capwords

class RegistrationView(FormView):

    form_class = RegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # Capitalize full name before saving
            new_user.first_name = request.POST['first_name'].capitalize()
            new_user.last_name = capwords(request.POST['last_name'])
            new_user.save()
            return redirect('users:login')
        return render(request, self.template_name, {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        next = request.POST.get('next') or None
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if next is None:
                    return redirect(reverse('mainpage:home', kwargs={'pk': request.user.id}))
                return redirect(request.POST.get('next'))
        login_url = reverse('users:login') # get the login url
        query_string =  urlencode({'next': next})
        url = '{}?{}'.format(login_url, query_string) # create the url
        return redirect(url)
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')