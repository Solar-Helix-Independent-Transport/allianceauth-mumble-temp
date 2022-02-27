from django.utils.translation import gettext_lazy as _

from allianceauth.services.hooks import MenuItemHook, UrlHook
from allianceauth import hooks

from . import urls


class ExampleMenuItem(MenuItemHook):
    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _('Mumble Temp Links'),
            'fas fa-microphone fa-fw',
            'mumbletemps:index',
            navactive=['mumbletemps:index']
        )

    def render(self, request):
        if request.user.has_perm('mumbletemps.create_new_links'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu():
    return ExampleMenuItem()


@hooks.register('url_hook')
def register_urls():
    return UrlHook(urls, 'mumbletemps', r'^mumbletemps/')
