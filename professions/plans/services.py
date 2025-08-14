PLAN_IMAGES = {
    "b": "dashboard/images/plans/basic.svg",
    "s": "dashboard/images/plans/standard.svg",
    "p": "dashboard/images/plans/premium.svg",
}


def get_plans_with_images(plans):
    for plan in plans:
        plan.image_url = PLAN_IMAGES.get(plan.name.lower(), "assets/images/default.svg")
    return plans
