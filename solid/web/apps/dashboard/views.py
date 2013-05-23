from tornado.web import authenticated

from solid.web.apps.core.baseview import BaseView
from solid.web.apps.dashboard.models import exception_model


class DashboardView(BaseView):

	def initialize(self):
		self.current_page='dashboard'
		super(DashboardView, self).initialize()

	@authenticated
	def get(self):

		exceptions = exception_model.get_all()

		self.render("dashboard.html",
			exceptions=exceptions)
