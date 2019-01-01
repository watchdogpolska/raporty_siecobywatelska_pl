from allauth.compat import is_authenticated
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def get_login_redirect_url(self, request):
        if is_authenticated(request.user) and not self.request.user.is_initially_introduced:
            return reverse("users:welcome")
        return super().get_login_redirect_url(request)

    def get_email_confirmation_url(self, request, emailconfirmation):
        return super().get_email_confirmation_url(request, emailconfirmation)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
