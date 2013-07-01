from tornado.web import authenticated

from solid.web.apps.core.baseview import BaseView


class SettingsView(BaseView):

	def initialize(self):
		self.current_page='settings'
		super(SettingsView, self).initialize()

	@authenticated
	def get(self):
		self.render("settings/settings.html")