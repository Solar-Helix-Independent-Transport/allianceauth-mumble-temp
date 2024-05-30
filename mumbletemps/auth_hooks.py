from django.utils.translation import gettext_lazy as _

from allianceauth.services.hooks import MenuItemHook, UrlHook
from allianceauth import hooks

from . import urls


class ExampleMenuItem(MenuItemHook):
    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self=self,
            text=_("Mumble Temp Links"),
            classes="fa-solid fa-microphone",
            url_name="mumbletemps:index",
            navactive=["mumbletemps:index"],
        )

    def render(self, request):
        if request.user.has_perm("mumbletemps.create_new_links"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return ExampleMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(
        urls=urls,
        namespace="mumbletemps",
        base_url=r"^mumbletemps/",
        excluded_views=[
            "mumbletemps.views.link",
            "mumbletemps.views.link_username",
            "mumbletemps.views.link_sso",
        ],
    )
