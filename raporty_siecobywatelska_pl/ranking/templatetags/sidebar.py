from django import template
from django.urls import reverse

from raporty_siecobywatelska_pl.ranking.models import Ranking

register = template.Library()

@register.simple_tag(takes_context=True)
def sidenav_item_active(context, viewname, *args, **kwargs):
    url = reverse(viewname=viewname, args=args, kwargs=kwargs)
    request = context['request']
    if viewname == "rankings:detail":
        current_viewname = request.resolver_match.namespace + ':' + request.resolver_match.url_name
        if current_viewname != viewname:
            return ''

    if request.path.startswith(url):
        return ' sidenav__item--active'
    return ''


@register.inclusion_tag("partials/_ranking_dropdown.html", takes_context=True)
def ranking_dropdown(context):
    request = context['request']
    rankings = Ranking.objects.values("pk", 'name', 'slug')
    return {
        "rankings": rankings,
        "current_ranking": request.ranking
    }
