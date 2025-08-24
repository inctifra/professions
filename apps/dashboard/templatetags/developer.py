from django import template
from django.template.defaultfilters import urlize

register = template.Library()


@register.inclusion_tag("dashboard/snippets/projects/stats.html", takes_context=True)
def developer_project_stats(context):
    return context


@register.inclusion_tag("dashboard/snippets/projects/none.html", takes_context=True)
def developer_none_projects(context):
    return context


@register.inclusion_tag(
    "dashboard/snippets/profile/user_image.html",
    takes_context=True,
)
def developer_avatar(context):
    return context


@register.filter
def urlize_blank(value):
    linked = urlize(value, autoescape=True)
    return linked.replace("<a ", '<a target="_blank" rel="noopener noreferrer" ')
