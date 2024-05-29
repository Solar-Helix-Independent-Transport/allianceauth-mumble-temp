# Mumble Temp Links<a name="mumble-temp-links"></a>

> \[!IMPORTANT\]
>
> This does nothing on its own you also need to update your authenticator [to my
> fork found here](https://gitlab.com/aaronkable/mumble-authenticator).
>
> More on that in the setup instructions below!

This [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) module lets you give temp access to your mumble service with ease.

______________________________________________________________________

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Usage](#usage)
- [Setup](#setup)
  - [Auth Plugin](#auth-plugin)
  - [Settings](#settings)
  - [Mumble Authenticator](#mumble-authenticator)
  - [Auth Login Bypass](#auth-login-bypass)
    - [Edit your projects `urls.py` file:](#edit-your-projects-urlspy-file)
    - [Restart services and you're done.](#restart-services-and-youre-done)
  - [Permissions](#permissions)
- [Preview](#preview)
  - [Management and Creation](#management-and-creation)
  - [OPTIONAL Login Screen (Non SSO mode)](#optional-login-screen-non-sso-mode)
  - [Templink User View](#templink-user-view)

<!-- mdformat-toc end -->

______________________________________________________________________

## Usage<a name="usage"></a>

A user with the `create` permission creates a link and copies it to the people who need access,
TempLink users will be given the group `Guest`, mumble ACL's can be setup to restrict access as required.
The mumble chat command `!kicktemps` will purge the mumble server of all temp users, if they still have a valid Templink they will be able to reconnect until it either expires or is removed from the tool. Only members who have the `Kick User` permission can use the command.

## Setup<a name="setup"></a>

> \[!NOTE\]
>
> ️This is assuming you already have configured a fully functioning mumble service.

### Auth Plugin<a name="auth-plugin"></a>

1. Install with `pip install allianceauth-mumbletemps`
1. Add `'mumbletemps',` to your `INSTALLED_APPS` in the local.py, I recommend it is at the top for menu ordering.
1. Run migrations
1. Restart auth

### Settings<a name="settings"></a>

| Setting                   | Default   | Description                                                              |
| ------------------------- | --------- | ------------------------------------------------------------------------ |
| MUMBLE_TEMPS_FORCE_SSO    | `True`    | Setting this to `False` will allow users to auth with the non-sso method |
| MUMBLE_TEMPS_SSO_PREFIX   | `[TEMP]`  | Display Name Prefix for an SSO'd temp user in mumble                     |
| MUMBLE_TEMPS_LOGIN_PREFIX | `[*TEMP]` | Display Name Prefix for a non-SSO'd temp user in mumble                  |

### Mumble Authenticator<a name="mumble-authenticator"></a>

To update your mumble authenticator if you git cloned the original repo, we will add my branch as a remote and check out the updated code.

> \[!IMPORTANT\]
>
> ️It is a good idea to back up your `authenticator.ini` file before starting.

1. `cd` into the folder you have the authenticator code in.
1. `git status` to confirm it is a git repo, and the correct place.
1. `git remote add upstream git@gitlab.com:aaronkable/mumble-authenticator.git` to add the remote.
1. `git fetch upstream` to grab the updates.
1. `git checkout upstream/master` to roll over to my code.
1. Restart your authenticator with supervisor.

> \[!NOTE\]
>
> The authenticator.log should show something like:
>
> ```
> Starting AllianceAuth mumble authenticator V:1.0.0 - TempLinks
> ```
>
> If you are on the correct branch and version, if not, you may still be running the default auth version and will need to investigate why. Users will get prompted for passwords when they try to connect with a temp link, and you are not running this version. The Authenticator version needs to match this version!

If you did not use the git clone method of installing the authenticator,
copy the contents of [my forkfound here](https://gitlab.com/aaronkable/mumble-authenticator)
on top of your current installation.

**BE SURE TO BACK UP YOUR `authenticator.ini` BEFORE YOU START!**

### Auth Login Bypass<a name="auth-login-bypass"></a>

To enable people to not have to register on auth, ensure you have fully updated `django-esi`

#### Edit your projects `urls.py` file:<a name="edit-your-projects-urlspy-file"></a>

It should look something like this, if yours is different, only add the parts outlined below:

```python
from django.urls import re_path
from django.conf.urls import include
from allianceauth import urls

urlpatterns = [
    re_path(r"", include(urls)),
]

handler500 = "allianceauth.views.Generic500Redirect"
handler404 = "allianceauth.views.Generic404Redirect"
handler403 = "allianceauth.views.Generic403Redirect"
handler400 = "allianceauth.views.Generic400Redirect"
```

Edit it to add a new import and a new URL:

```python
from django.urls import re_path
from django.conf.urls import include
from allianceauth import urls
from mumbletemps.views import link  # *** New Import

urlpatterns = [
    re_path(
        r"^mumbletemps/join/(?P<link_ref>[\w\-]+)/$", link, name="join"
    ),  # *** New URL override BEFORE THE MAIN IMPORT
    re_path(r"", include(urls)),
]

handler500 = "allianceauth.views.Generic500Redirect"
handler404 = "allianceauth.views.Generic404Redirect"
handler403 = "allianceauth.views.Generic403Redirect"
handler400 = "allianceauth.views.Generic400Redirect"
```

#### Restart services and you're done.<a name="restart-services-and-youre-done"></a>

### Permissions<a name="permissions"></a>

| Perm                         | Admin Site | Auth Site                         |
| ---------------------------- | ---------- | --------------------------------- |
| mumbletemps.create_new_links | None       | Can create and delete Temp Links. |

## Preview<a name="preview"></a>

### Management and Creation<a name="management-and-creation"></a>

![image](https://i.imgur.com/Jl2ihH2.png)

### OPTIONAL Login Screen (Non SSO mode)<a name="optional-login-screen-non-sso-mode"></a>

![Login](https://i.imgur.com/BIRLFmq.png)

### Templink User View<a name="templink-user-view"></a>

![Demo](https://i.imgur.com/G86qAb8.png)
