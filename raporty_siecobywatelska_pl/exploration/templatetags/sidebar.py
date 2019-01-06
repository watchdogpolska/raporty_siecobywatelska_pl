from django import template
from django.urls import reverse

from raporty_siecobywatelska_pl.exploration.models import Exploration

register = template.Library()


@register.simple_tag(takes_context=True)
def sidenav_item_active(context, viewname, *args, **kwargs):
    url = reverse(viewname=viewname, args=args, kwargs=kwargs)
    request = context['request']
    if viewname == "exploration:detail":
        current_viewname = request.resolver_match.namespace + ':' + request.resolver_match.url_name
        if current_viewname != viewname:
            return ''

    if request.path.startswith(url):
        return ' sidenav__item--active'
    return ''


@register.inclusion_tag("partials/_exploration_dropdown.html", takes_context=True)
def exploration_dropdown(context):
    request = context['request']
    explorations = Exploration.objects.values("pk", 'name', 'slug')
    return {
        "explorations": explorations,
        "current_exploration": request.exploration
    }
