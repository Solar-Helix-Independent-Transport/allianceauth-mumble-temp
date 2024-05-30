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
  - [Alliance Auth Plugin](#alliance-auth-plugin)
    - [Step 1: Install the Package](#step-1-install-the-package)
    - [Step 2: Configure Alliance Auth](#step-2-configure-alliance-auth)
    - [Step 3: Finalizing the Installation](#step-3-finalizing-the-installation)
  - [Mumble Authenticator](#mumble-authenticator)
  - [Settings](#settings)
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

### Alliance Auth Plugin<a name="alliance-auth-plugin"></a>

#### Step 1: Install the Package<a name="step-1-install-the-package"></a>

Make sure you're in the virtual environment (venv) of your Alliance Auth installation. Then install the latest release directly from PyPi.

```shell
pip install allianceauth-mumbletemps
```

#### Step 2: Configure Alliance Auth<a name="step-2-configure-alliance-auth"></a>

You need to add `'mumbletemps',` to your `INSTALLED_APPS` and `APPS_WITH_PUBLIC_VIEWS` in the `local.py` file of your Alliance Auth installation.

This is fairly simple, configure your AA settings (`local.py`) as follows:

```python
INSTALLED_APPS += [
    # Your other apps are here as well
    "mumbletemps",
]

APPS_WITH_PUBLIC_VIEWS += [
    # Other apps with public views might live here
    "mumbletemps",
]

CELERYBEAT_SCHEDULE["mumbletemps_tidy_up_temp_links"] = {
    "task": "mumbletemps.tasks.tidy_up_temp_links",
    "schedule": crontab(minute="*/5"),
}
```

> \[!NOTE\]
>
> If you don't have a list for `APPS_WITH_PUBLIC_VIEWS` yet, then add the whole block
> from here. This feature has been added in Alliance Auth v3.6.0, so you might not yet
> have this list in your `local.py`.

#### Step 3: Finalizing the Installation<a name="step-3-finalizing-the-installation"></a>

Run static files collection and migrations.

```shell
python manage.py collectstatic --noinput
python manage.py migrate
```

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

### Settings<a name="settings"></a>

| Setting                   | Default   | Description                                                              |
| ------------------------- | --------- | ------------------------------------------------------------------------ |
| MUMBLE_TEMPS_FORCE_SSO    | `True`    | Setting this to `False` will allow users to auth with the non-sso method |
| MUMBLE_TEMPS_SSO_PREFIX   | `[TEMP]`  | Display Name Prefix for an SSO'd temp user in mumble                     |
| MUMBLE_TEMPS_LOGIN_PREFIX | `[*TEMP]` | Display Name Prefix for a non-SSO'd temp user in mumble                  |

### Restart services and you're done.<a name="restart-services-and-youre-done"></a>

Restart your Alliance Auth instance to apply the changes.

```shell
sudo systemctl restart supervisor.service
```

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
