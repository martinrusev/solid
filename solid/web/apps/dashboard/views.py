from tornado.web import authenticated
from solid.web.apps.core.baseview import BaseView


class DashboardView(BaseView):

	def initialize(self):
		self.current_page='dashboard'
		super(DashboardView, self).initialize()

	@authenticated
	def get(self):
		self.render("dashboard.html",)
