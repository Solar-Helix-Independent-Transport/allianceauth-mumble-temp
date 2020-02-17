# Mumble Temp Links

> ⚠️ This does nothing on it's own you also need to update your authenticator! [To my fork found here](https://gitlab.com/aaronkable/mumble-authenticator). More on that in the setup instructions below!

This [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) module lets you give temp access to your mumble service with ease.

# Usage
A user with the create permission crates a link and copy's it to the people who need access,
TempLink users will be given the group `Guest`, mumble ACL's can be setup to restrict access as required.
The mumble chat command `!kicktemps` will purge the mumble server of all temp users, if they still have a valid Templink they will be able to reconect untill it either expires or is removed from the tool. Only members who have thw `Kick User` permission can use the command.

# Setup
> ⚠️This is assuming you already have configured a fully functioning mumbke service.
## Auth Plugin
1. `pip install allianceauth-mumbletemps`
2. add `'mumbletemps',` to your `INSTALLED_APPS` in the local.py, i recomend it is at the top for menu ordering.
3. run migrations
4. restart auth

## Mumble Authenticator
to update your mumble authenticator if you git cloned the original repo we will add my branch as a remote and checkout the updated code.
> ⚠️It is a good idea to backup your `authenticator.ini` file before starting
1. `cd` into the folder you have the authenticator code in.
2. `git status` to confirm it is a git repo and the correct place
3. `git remote add upstream git@gitlab.com:aaronkable/mumble-authenticator.git` to add the remote
4. `git fetch upstream` to grab the updates
5. `git checkout upstream/master` to roll over to my code
6. restart your authenticator with supervisor
> ℹ️ The authenticator.log should show something like 
> `Starting AllianceAuth mumble authenticator V:1.0.0 - TempLinks` 
> if you are on the correct branch and version, if not you may still be running the default auth verssion and will need to investigate why. Users will get propted for passwords when they try to connect with a temp link and you are not running this version. the Authenticator version needs to match this version!

If you did not use the git clone method of installing the authenticator, simply copy the contents of this repo over the top of your current install, **BE SURE TO BACKUP YOUR `authenticator.ini` BEFORE YOU START!**

# Permissions
Perm | Admin Site	 | Auth Site 
 --- | --- | --- 
mumbletemps.create_new_links | None | Can create and delete Temp Links.

# todo
* format name with service name config
* optional prefix

# Preview
## Managemrnt and Creatiom
![image](https://i.imgur.com/Jl2ihH2.png)
## Templink User View
![Demo](https://i.imgur.com/zLC9ZPu.png)

