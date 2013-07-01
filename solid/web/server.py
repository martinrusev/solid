import os.path
import tornado.web
from tornado.web import url

from solid.web.settings import PROJECT_ROOT
from solid.core import settings

from solid.web.apps.dashboard.views import DashboardView
from solid.web.apps.auth.views import LoginView, CreateInitialUserView, LogoutView
from solid.web.apps.api.views import ApiException

from solid.web.apps.settings.views.notifications import NotificationsView
from solid.web.apps.settings.views.settings import SettingsView

app_settings = {
	"static_path": os.path.join(PROJECT_ROOT, "media"),
	"cookie_secret": settings.SECRET_KEY,
	"login_url" : "{0}:{1}/login".format(settings.WEB_APP['host'], settings.WEB_APP['port']),
	"session": {"duration": 3600, "regeneration_interval": 240, "domain": settings.WEB_APP['host']}
}

handlers = [
	# App
	url(r"/", DashboardView, name='dashboard'),
	# Auth
	url(r"/login", LoginView, name='login'),
	url(r"/logout", LogoutView, name='logout'),
	url(r"/create_user", CreateInitialUserView, name='create_user'),
	# Settings
	url(r"/settings", SettingsView, name='settings'),
	url(r"/settings/notifications", NotificationsView, name='notifications'),
	# API
	(r"/api/exception/{0}".format(settings.SECRET_KEY), ApiException),
	# Static
	(r"/media/(.*)", tornado.web.StaticFileHandler, {"path": app_settings['static_path']}),
]
application = tornado.web.Application(handlers, **app_settings)
