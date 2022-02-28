# Mumble Temp Links

> ⚠️ This does nothing on it's own you also need to update your authenticator! [To my fork found here](https://gitlab.com/aaronkable/mumble-authenticator). More on that in the setup instructions below!

This [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) module lets you give temp access to your mumble service with ease.

# Usage
A user with the create permission creates a link and copies it to the people who need access,
TempLink users will be given the group `Guest`, mumble ACL's can be setup to restrict access as required.
The mumble chat command `!kicktemps` will purge the mumble server of all temp users, if they still have a valid Templink they will be able to reconnect until it either expires or is removed from the tool. Only members who have the `Kick User` permission can use the command.

# Setup
> ⚠️This is assuming you already have configured a fully functioning mumble service.
## Auth Plugin
1. `pip install allianceauth-mumbletemps`
2. add `'mumbletemps',` to your `INSTALLED_APPS` in the local.py, I recommend it is at the top for menu ordering.
3. run migrations
4. restart auth

## Settings
Setting | Default	 | Description 
 --- | --- | --- 
MUMBLE_TEMPS_FORCE_SSO | `True` | Setting this to `False` will allow users to auth with the non-sso method
MUMBLE_TEMPS_SSO_PREFIX | `[TEMP]` | Display Name Prefix for an SSO'd temp user in mumble
MUMBLE_TEMPS_LOGIN_PREFIX | `[*TEMP]` | Display Name Prefix for a non-SSO'd temp user in mumble


## Mumble Authenticator
To update your mumble authenticator if you git cloned the original repo we will add my branch as a remote and checkout the updated code.
> ⚠️It is a good idea to backup your `authenticator.ini` file before starting
1. `cd` into the folder you have the authenticator code in.
2. `git status` to confirm it is a git repo and the correct place
3. `git remote add upstream git@gitlab.com:aaronkable/mumble-authenticator.git` to add the remote
4. `git fetch upstream` to grab the updates
5. `git checkout upstream/master` to roll over to my code
6. restart your authenticator with supervisor
> ℹ️ The authenticator.log should show something like 
> `Starting AllianceAuth mumble authenticator V:1.0.0 - TempLinks` 
> If you are on the correct branch and version, if not you may still be running the default auth version and will need to investigate why. Users will get prompted for passwords when they try to connect with a temp link and you are not running this version. The Authenticator version needs to match this version!

If you did not use the git clone method of installing the authenticator, simply copy the contents of [my fork found here](https://gitlab.com/aaronkable/mumble-authenticator) on top of your current install, **BE SURE TO BACKUP YOUR `authenticator.ini` BEFORE YOU START!**

## Auth Login Bypass
To enable people to not have to register on auth, ensure you have fully updated `django-esi`
1. Edit your projects `urls.py` file:

> It should look something like this, if yours is different only add the parts outlined below:
```python
from django.urls import re_path
from django.conf.urls import include
from allianceauth import urls

urlpatterns = [
    re_path(r'', include(urls)),
]

handler500 = 'allianceauth.views.Generic500Redirect'
handler404 = 'allianceauth.views.Generic404Redirect'
handler403 = 'allianceauth.views.Generic403Redirect'
handler400 = 'allianceauth.views.Generic400Redirect' 
```
> Edit it to add a new import and a new url
```python
from django.urls import re_path
from django.conf.urls import include
from allianceauth import urls
from mumbletemps.views import link  # *** New Import 

urlpatterns = [
    re_path(r'^mumbletemps/join/(?P<link_ref>[\w\-]+)/$', link, name='join'),  # *** New URL override BEFORE THE MAIN IMPORT
    re_path(r'', include(urls)),
]

handler500 = 'allianceauth.views.Generic500Redirect' 
handler404 = 'allianceauth.views.Generic404Redirect'
handler403 = 'allianceauth.views.Generic403Redirect'
handler400 = 'allianceauth.views.Generic400Redirect' 
```
2. Restart services and you're done.

# Permissions
Perm | Admin Site	 | Auth Site 
 --- | --- | --- 
mumbletemps.create_new_links | None | Can create and delete Temp Links.

# Preview
## Management and Creation
![image](https://i.imgur.com/Jl2ihH2.png)
## OPTIONAL Login Screen ( Non SSO mode )
![Login](https://i.imgur.com/BIRLFmq.png)
## Templink User View
![Demo](https://i.imgur.com/G86qAb8.png)
