from allauth.socialaccount.providers.facebook.provider import FacebookProvider


class MyFacebookProvider(FacebookProvider):
    pass


provider_classes = [MyFacebookProvider]
