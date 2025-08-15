from rest_framework.throttling import SimpleRateThrottle


class ProjectPlanThrottle(SimpleRateThrottle):
    scope = "project_plan"

    def get_cache_key(self, request, view):
        # This determines the unique key per API key
        if not hasattr(request, "user") or request.user is None:
            return None  # skip throttling if no user
        # Use API key or project ID as unique cache key
        api_key = getattr(request.user, "api_key", None)
        project_id = getattr(request.user, "project", None)
        return f"throttle_{api_key}_{project_id}"

    def get_rate(self):
        """
        Return the rate string based on project plan.
        This method does NOT use self.request
        """
        # Provide a default rate
        return "5/minute"

    def allow_request(self, request, view):
        """
        Dynamically override rate per project plan.
        """
        project = getattr(request.user, "project", None)
        if project:
            plan = getattr(project, "plan", "basic")
            if plan == "basic":
                self.rate = "3/sec"
            elif plan == "pro":
                self.rate = "10/min"
            else:
                self.rate = "5/min"
        else:
            # fallback rate if no project
            self.rate = "1/min"
        return super().allow_request(request, view)
