import tornado.web
from solid.web.api.models import api_exception_model

class ApiException(tornado.web.RequestHandler):

	def post(self, secret_key=None):		
		content_type_dict = self.request.headers['Content-Type'].split(';') # Split only the fist part and leave the charset
		content_type = content_type_dict[0] if len(content_type_dict) > 0 else ''	

		if str(content_type) in ['application/json', 'text/javascript', 'application/x-www-form-urlencoded']:
			try:
				json_dict = tornado.escape.json_decode(self.request.body)
			except:
				json_dict = None

			if json_dict != None:
				api_exception_model.save(json_dict)

	def get(self):
		 self.write('Only POST requests containing the following json dictionary - data = {\
					"exception_class": "",\
					"message": "",\
					"url": "",\
					"backtrace": "",\
					"enviroment": "",\
					"data": ""}')


