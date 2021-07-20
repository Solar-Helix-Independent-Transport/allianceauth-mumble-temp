from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
import urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib import messages
from esi.decorators import single_use_token
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

class psudo_profile:
    def __init__(self, main):
        self.main_character = main
        self.state = get_guest_state()

class psudo_user:
    def __init__(self, main, username):
        self.username = username
        self.profile = psudo_profile(main)

@login_required
@permission_required('mumbletemps.create_new_links')
def index(request):
    tl = None
    if request.method == 'POST':
        duration = request.POST.get('time')
        if duration in ['3', '6', '12', '24']:
            expiry = datetime.datetime.utcnow().replace(tzinfo=timezone.utc) + datetime.timedelta(hours=int(duration))
            tl = TempLink.objects.create(
                                            creator=request.user.profile.main_character,
                                            link_ref=get_random_string(15),
                                            expires=expiry.timestamp()
                                        )
            tl.save()

    tl_list = TempLink.objects.prefetch_related("creator").filter(
        expires__gte=datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    )
    ex_tl_list = TempLink.objects.prefetch_related("creator").filter(
        expires__lt=datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()
    )

    context = {
        'tl': tl,
        'text': 'Make Links',
        'tl_list': tl_list,
        'ex_tl_list': ex_tl_list
    }    
    return render(request, 'mumbletemps/index.html', context)

def link(request, link_ref):
    link = None
    try:
        link = TempLink.objects.get(link_ref=link_ref)
    except:
        raise Http404("Temp Link Does not Exist") 
    
    token = _check_callback(request)
    if token:
        return link_sso(request, token, link)


    if app_settings.MUMBLE_TEMPS_FORCE_SSO:  #default always SSO
        # prompt the user to login for a new token
        return sso_redirect(request, scopes=['publicData'])

    if request.method == 'POST':  # ok so maybe we want to let some other people in too.
        if request.POST.get('sso', False) == "False": # they picked user
            name = request.POST.get('name', False)
            association = request.POST.get('association', False)
            return link_username(request, name, association, link)
        elif request.POST.get('sso', False) == "True": # they picked SSO
            # prompt the user to login for a new token
            return sso_redirect(request, scopes=['publicData'])

    context = {
        'link': link,
    }    
    return render(request, 'mumbletemps/login.html', context)

def link_username(request, name, association, link):
    connect_url = None
    
    username = get_random_string(10)
    while TempUser.objects.filter(username=username).exists():  # force unique
        username = get_random_string(10)

    password = get_random_string(15)

    display_name = "{}[{}] {}".format(app_settings.MUMBLE_TEMPS_LOGIN_PREFIX, association, name)

    temp_user = TempUser.objects.create(username=username, password=password, name=display_name, expires=link.expires, templink=link)

    connect_url = "{}:{}@{}".format(username, password, settings.MUMBLE_URL)

    context = {
        'temp_user': temp_user,
        'link': link,
        'connect_url': connect_url,
        'mumble': settings.MUMBLE_URL,
    }    

    return render(request, 'mumbletemps/link.html', context)

def link_sso(request, token, link):
    connect_url = None

    try:
        char = EveCharacter.objects.get(character_id=token.character_id)
    except ObjectDoesNotExist: 
        try: #create a new character, we should not get here.
            char = EveCharacter.objects.update_character(token.character_id)
        except:
            pass ## yeah... aint gonna happen
    except MultipleObjectsReturned:
        pass # authenticator woont care... but the DB will be unhappy.
    
    username = get_random_string(10)
    while TempUser.objects.filter(username=username).exists():  # force unique
        username = get_random_string(10)

    password = get_random_string(15)

    display_name = "{}{}".format(app_settings.MUMBLE_TEMPS_SSO_PREFIX, NameFormatter(MumbleService(), psudo_user(char, username)).format_name())

    temp_user = TempUser.objects.create(username=username, password=password, name=display_name, expires=link.expires, templink=link, character_id=char.character_id)

    connect_url = "{}:{}@{}".format(username, password, settings.MUMBLE_URL)

    context = {
        'temp_user': temp_user,
        'link': link,
        'connect_url': connect_url,
        'mumble': settings.MUMBLE_URL,
    }

    return render(request, 'mumbletemps/link.html', context)

@login_required
@permission_required('mumbletemps.create_new_links')
def nuke(request, link_ref):
    try:
        link = TempLink.objects.get(link_ref=link_ref).delete()
        users = TempUser.objects.filter(templink__isnull=True).delete()
        messages.success(request, "Deleted Token {}".format(link_ref))

    except:
        messages.error(request, "Deleted Token {}".format(link_ref))
        pass # crappy link
    
    return redirect('mumbletemps:index')

