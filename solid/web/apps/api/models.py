from solid.web.apps.core.models import BaseModel
from solid.utils.dates import unix_utc_now

class ApiExceptionModel(BaseModel):

	def __init__(self):
		super(ApiExceptionModel, self).__init__()

	
api_exception_model = ApiExceptionModel()
