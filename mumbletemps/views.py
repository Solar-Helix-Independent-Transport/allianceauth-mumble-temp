from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.crypto import get_random_string
from django.contrib import messages
from allianceauth.eveonline.models import EveCharacter

from allianceauth.services.modules.mumble.auth_hooks import MumbleService
from allianceauth.services.hooks import NameFormatter
from allianceauth.authentication.models import get_guest_state

from django.http import Http404

from . import app_settings
from .models import TempLink, TempUser
from esi.views import sso_redirect
from esi.decorators import _check_callback
import datetime


class PseudoProfile:
    def __init__(self, main):
        self.main_character = main
        self.state = get_guest_state()


class PseudoUser:
    def __init__(self, main, username):
        self.username = username
        self.profile = PseudoProfile(main)


@login_required
@permission_required("mumbletemps.create_new_links")
def index(request):
    tl = None

    if request.method == "POST":
        duration = request.POST.get("time")

        if duration in ["3", "6", "12", "24"]:
            expiry = datetime.datetime.utcnow().replace(
                tzinfo=datetime.timezone.utc
            ) + datetime.timedelta(hours=int(duration))
            tl = TempLink.objects.create(
                creator=request.user.profile.main_character,
                link_ref=get_random_string(15),
                expires=expiry.timestamp(),
            )
            tl.save()

    tl_list = TempLink.objects.prefetch_related("creator").filter(
        expires__gte=datetime.datetime.utcnow()
        .replace(tzinfo=datetime.timezone.utc)
        .timestamp()
    )
    ex_tl_list = TempLink.objects.prefetch_related("creator").filter(
        expires__lt=datetime.datetime.utcnow()
        .replace(tzinfo=datetime.timezone.utc)
        .timestamp()
    )

    context = {
        "tl": tl,
        "text": "Make Links",
        "tl_list": tl_list,
        "ex_tl_list": ex_tl_list,
    }

    return render(
        request=request, template_name="mumbletemps/index.html", context=context
    )


def link(request, link_ref):
    try:
        templink = TempLink.objects.get(link_ref=link_ref)
    except ObjectDoesNotExist:
        raise Http404("Temp Link Does not Exist")

    token = _check_callback(request=request)
    if token:
        return link_sso(request=request, token=token, link=templink)

    if app_settings.MUMBLE_TEMPS_FORCE_SSO:  # default always SSO
        # prompt the user to log in for a new token
        return sso_redirect(request=request, scopes=["publicData"])

    if request.method == "POST":  # ok so maybe we want to let some other people in too.
        if request.POST.get("sso", False) == "False":  # they picked user
            name = request.POST.get("name", False)
            association = request.POST.get("association", False)

            return link_username(
                request=request, name=name, association=association, link=templink
            )
        elif request.POST.get("sso", False) == "True":  # they picked SSO
            # prompt the user to log in for a new token
            return sso_redirect(request=request, scopes=["publicData"])

    context = {"link": templink}

    return render(
        request=request, template_name="mumbletemps/login.html", context=context
    )


def link_username(request, name, association, link):
    username = get_random_string(length=10)

    while TempUser.objects.filter(username=username).exists():  # force unique
        username = get_random_string(length=10)

    password = get_random_string(length=15)

    display_name = "{}[{}] {}".format(
        app_settings.MUMBLE_TEMPS_LOGIN_PREFIX, association, name
    )

    temp_user = TempUser.objects.create(
        username=username,
        password=password,
        name=display_name,
        expires=link.expires,
        templink=link,
    )

    connect_url = f"{username}:{password}@{settings.MUMBLE_URL}"

    context = {
        "temp_user": temp_user,
        "link": link,
        "connect_url": connect_url,
        "mumble": settings.MUMBLE_URL,
    }

    return render(
        request=request, template_name="mumbletemps/link.html", context=context
    )


def link_sso(request, token, link):
    try:
        char = EveCharacter.objects.get(character_id=token.character_id)
    except ObjectDoesNotExist:
        try:  # create a new character, we should not get here.
            char = EveCharacter.objects.update_character(
                character_id=token.character_id
            )
        except:  # noqa: E722
            pass  # Yeah… ain't gonna happen
    except MultipleObjectsReturned:
        pass  # authenticator won't care…, but the DB will be unhappy.

    username = get_random_string(length=10)

    while TempUser.objects.filter(username=username).exists():  # force unique
        username = get_random_string(length=10)

    password = get_random_string(length=15)

    display_name = "{}{}".format(
        app_settings.MUMBLE_TEMPS_SSO_PREFIX,
        NameFormatter(
            service=MumbleService(), user=PseudoUser(main=char, username=username)
        ).format_name(),
    )

    temp_user = TempUser.objects.create(
        username=username,
        password=password,
        name=display_name,
        expires=link.expires,
        templink=link,
        character_id=char.character_id,
    )

    connect_url = f"{username}:{password}@{settings.MUMBLE_URL}"

    context = {
        "temp_user": temp_user,
        "link": link,
        "connect_url": connect_url,
        "mumble": settings.MUMBLE_URL,
    }

    return render(
        request=request, template_name="mumbletemps/link.html", context=context
    )


@login_required
@permission_required("mumbletemps.create_new_links")
def nuke(request, link_ref):
    try:
        TempLink.objects.get(link_ref=link_ref).delete()
        TempUser.objects.filter(templink__isnull=True).delete()

        messages.success(request=request, message=f"Deleted Token {link_ref}")
    except:  # noqa: E722
        messages.error(request=request, message=f"Deleted Token {link_ref}")
        pass  # Crappy link

    return redirect(to="mumbletemps:index")
