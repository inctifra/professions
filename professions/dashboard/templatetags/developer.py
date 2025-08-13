from django import template

from professions.projects.models import Project

register = template.Library()


@register.inclusion_tag("snippets/projects/stats.html", takes_context=True)
def developer_project_stats(context):
    profile = context["request"].user.profile
    projects = Project.objects.filter(user=profile)
    context.update({
        "projects": projects
    })
    return context
