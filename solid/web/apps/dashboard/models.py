from solid.web.apps.core.basemodel import BaseModel

class ExceptionModel(BaseModel):
	
	def __init__(self):
		super(ExceptionModel, self).__init__()
		self.collection = self.mongo.get_collection('exceptions') 

	def get_all(self):
		exceptions = self.collection.find().sort('last_occurrence', self.desc)

		return exceptions


exception_model = ExceptionModel()