from django.utils.deprecation import MiddlewareMixin

from raporty_siecobywatelska_pl.exploration.models import Exploration


class CurrentExplorationMiddleware(MiddlewareMixin):
    """
    Middleware that sets `exploration` attribute to request object.
    """
    def process_view(self, request, callback, callback_args, callback_kwargs):
        request.exploration = Exploration.objects.get_current(request)
