from django.http.request import HttpRequest


def website_context_processors(request: HttpRequest):
    return {"documentation": "https://docs.pkenya.makelaw.ke"}
