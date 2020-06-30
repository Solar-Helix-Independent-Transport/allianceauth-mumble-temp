from django.conf import settings

MUMBLE_TEMPS_FORCE_SSO = getattr(settings, "MUMBLE_TEMPS_FORCE_SSO", True)
MUMBLE_TEMPS_SSO_PREFIX = getattr(settings, "MUMBLE_TEMPS_SSO_PREFIX", "[TEMP]")
MUMBLE_TEMPS_LOGIN_PREFIX = getattr(settings, "MUMBLE_TEMPS_LOGIN_PREFIX", "[*TEMP]")
