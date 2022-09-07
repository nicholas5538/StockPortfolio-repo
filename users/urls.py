from audioop import reverse
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from users import views as user_view
from .forms import UserPasswordResetForm, UserSetPasswordForm

app_name = 'users'
urlpatterns = [
    path('register/', user_view.RegistrationView.as_view(), name='register'),
    path('login/', user_view.login_view, name='login'),
    path('logout/', user_view.logout_view, name='logout'),
    path(
        'reset-password/', 
        auth_views.PasswordResetView.as_view(
            form_class=UserPasswordResetForm,
            template_name="users/reset_password.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:reset_password_sent")), 
        name='reset_password'
        ),
    path(
        'reset-password-sent/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/reset_password_sent.html",
            ), 
        name='reset_password_sent'),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            form_class=UserSetPasswordForm,
            template_name="users/password_reset_form.html",
            success_url=reverse_lazy("users:password_reset_complete")
            ), 
        name='password_reset_confirm'),
    path(
        'reset-password-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"), 
        name='password_reset_complete'),
]