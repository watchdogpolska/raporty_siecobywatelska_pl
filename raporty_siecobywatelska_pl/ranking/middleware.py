from django.utils.deprecation import MiddlewareMixin

from raporty_siecobywatelska_pl.ranking.models import Ranking


class CurrentRankingMiddleware(MiddlewareMixin):
    """
    Middleware that sets `ranking` attribute to request object.
    """

    def process_view(self, request, callback, callback_args, callback_kwargs):
        request.ranking = Ranking.objects.get_current(request)
