from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from raporty_siecobywatelska_pl.users.forms import UserForm, WelcomeSettingForm
from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class WelcomeSettingFormView(LoginRequiredMixin, FormView):
    form_class = WelcomeSettingForm
    template_name = 'users/user_welcome.html'

    def dispatch(self, request, *args, **kwargs):
        self.mark_users_as_introducted()
        return super().dispatch(request, *args, **kwargs)

    def mark_users_as_introducted(self):
        user = self.request.user
        if not user.is_initially_introduced:
            user.is_initially_introduced = True
            user.save(update_fields=['is_initially_introduced'])



