from tornado.web import authenticated

from solid.web.apps.core.baseview import BaseView


class NotificationsView(BaseView):

	def initialize(self):
		self.current_page='settings'
		super(NotificationsView, self).initialize()

	@authenticated
	def get(self):
		self.render("settings/notifications.html")