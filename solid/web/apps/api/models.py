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
		backtrace = exception.get('backtrace', '')
		
		message= exception.get('message', '')

		request = exception.get('request', '')
		context = exception.get('context', '')
				
		exception_string = "{0}{1}".format(exception_class, backtrace)
		exception_id = md5(exception_string).hexdigest()

		additional_data = {'occurrence': now}

		exception_in_db = self.collection.find_one({"exception_id" : exception_id})

		if exception_in_db is not None:
			exception_in_db['last_occurrence'] = now
			exception_in_db['total_occurrences']  = exception_in_db['total_occurrences']+1

			self.collection.update({'_id' : exception_in_db['_id']}, exception_in_db)
		else:
			entry = {'last_occurrence': now,
					 'exception_id': exception_id,
					 'exception_class': exception_class,
					 'backtrace' : backtrace,
					 'request': request,
					 'context': context,
					 'message': message
					 }

			entry['additional_data'] = [additional_data]
			entry['total_occurrences'] = 1

			self.collection.save(entry)
			self.collection.ensure_index('message')

api_exception_model = ApiExceptionModel()