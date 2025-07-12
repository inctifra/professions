from rest_framework.throttling import SimpleRateThrottle


class PharmacyThrottle(SimpleRateThrottle):
    scope = "pharmacy"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }


class PharmtechThrottle(SimpleRateThrottle):
    scope = "pharmtech"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }
