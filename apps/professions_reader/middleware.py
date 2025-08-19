import time


class RequestTimerMiddleware:
    """
    Records the start time of the request for later use in views.
    This is needed for the API response time calculation
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._start_time = time.time()  # noqa: SLF001
        return self.get_response(request)
