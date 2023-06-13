from django.urls import path
from allauth.account.views import ConfirmEmailView, LoginView, LogoutView, SignupView, PasswordResetView, PasswordChangeView, EmailVerificationSentView, EmailView, PasswordResetFromKeyView, PasswordResetDoneView, PasswordResetFromKeyDoneView

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/password/reset/key/<uidb36>/<key>/', PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/email-verification-sent/', EmailVerificationSentView.as_view(), name='account_email_verification_sent'),
    path('accounts/email/', EmailView.as_view(), name='account_email'),
    path('accounts/password/reset/done/', PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('accounts/password/reset/key/done/', PasswordResetFromKeyDoneView.as_view(), name='account_reset_password_from_key_done'),




]
