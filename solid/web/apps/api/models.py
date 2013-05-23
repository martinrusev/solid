from solid.web.apps.core.basemodel import BaseModel
from solid.utils.dates import unix_utc_now
from hashlib import md5

class ApiExceptionModel(BaseModel):

	def __init__(self):
		super(ApiExceptionModel, self).__init__()
		self.collection = self.mongo.get_collection('exceptions')

	def save(self, exception):
		now = unix_utc_now()

		exception_class = exception.get('exception_class', '')
		url = exception.get('url', '')
		backtrace = exception.get('backtrace', '')
		
		message= exception.get('message', '')
		enviroment = exception.get('enviroment', '')
		data = exception.get('data', '')
		
		
		exception_string = "{0}{1}{2}".format(exception_class, url, backtrace)
		exception_id = md5(exception_string).hexdigest()

		additional_data = {'occurrence': now}

		if message: additional_data['message'] = message
		if enviroment: additional_data['enviroment'] = enviroment
		if data: additional_data['data'] = data

		exception_in_db = self.collection.find_one({"exception_id" : exception_id})

		if exception_in_db is not None:
			exception_in_db['last_occurrence'] = now
			exception_in_db['additional_data'].insert(0, additional_data)
			exception_in_db['total_occurrences']  = exception_in_db['total_occurrences']+1

			self.collection.update({'_id' : exception_in_db['_id']}, exception_in_db)
		else:
			entry = {'last_occurrence': now,
					 'exception_id': exception_id,
					 'exception_class': exception_class,
					 'url': url,
					 'backtrace' : backtrace,
					 }

			entry['additional_data'] = [additional_data]
			entry['total_occurrences'] = 1

			self.collection.save(entry)
			self.collection.ensure_index('message')

api_exception_model = ApiExceptionModel()