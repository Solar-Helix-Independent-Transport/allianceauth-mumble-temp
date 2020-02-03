from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
import urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib import messages

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

@login_required
def link(request, link_ref):
    link = None
    connect_url = None
    try:
        link = TempLink.objects.get(link_ref=link_ref)
    except:
        pass # crappy link
    
    connect_url = "{}:{}@{}".format(urllib.parse.quote(request.user.username, safe=""), link_ref, settings.MUMBLE_URL)
    context = {
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



