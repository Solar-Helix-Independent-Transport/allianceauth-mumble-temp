from django.conf import settings

MUMBLE_TEMPS_FORCE_SSO = getattr(settings, "MUMBLE_TEMPS_FORCE_SSO", True)