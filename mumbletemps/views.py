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


from .models import TempLink
import datetime

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

    tl_list = TempLink.objects.filter(expires__gte=datetime.datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

    context = {
        'tl': tl,
        'text': 'Make Links',
        'tl_list': tl_list
    }    
    return render(request, 'mumbletemps/index.html', context)

@single_use_token(scopes=['publicData'])
def link(request, token, link_ref):
    link = None
    connect_url = None
    try:
        link = TempLink.objects.get(link_ref=link_ref)
    except:
        pass # crappy link
    
    try:
        char = EveCharacter.objects.get(character_id=token.character_id)
    except ObjectDoesNotExist: 
        try: #create a new character, we should not get here.
            char = EveCharacter.objects.update_character(token.character_id)
        except:
            pass ## yeah... aint gonna happen
    except MultipleObjectsReturned:
        pass # authenticator woont care... but the DB will be unhappy.

    connect_url = "{}:{}@{}".format(urllib.parse.quote(str(token.character_id), safe=""), link_ref, settings.MUMBLE_URL)

    context = {
        'char': char,
        'link': link,
        'connect_url': connect_url,
    }    

    return render(request, 'mumbletemps/link.html', context)

@login_required
@permission_required('mumbletemps.create_new_links')
def nuke(request, link_ref):
    try:
        link = TempLink.objects.get(link_ref=link_ref).delete()
        messages.success(request, "Deleted Token {}".format(link_ref))

    except:
        messages.error(request, "Deleted Token {}".format(link_ref))
        pass # crappy link
    
    return redirect('mumbletemps:index')



