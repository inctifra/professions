from django import template

from professions.plans.services import get_plans_with_images

register = template.Library()

@register.inclusion_tag("dashboard/snippets/plans/plan.html", takes_context=True)
def load_available_plans(context):
    return {
        "plans": get_plans_with_images(context.get("plans")),
        "features": context.get("features")
        }
