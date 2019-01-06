from django import template

register = template.Library()


@register.inclusion_tag("partials/_icons_providers.html")
def provider_icon(provider):
    return {
        "provider": provider,
    }
