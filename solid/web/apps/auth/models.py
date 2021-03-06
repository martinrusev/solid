import hashlib
from solid.web.apps.core.basemodel import BaseModel

class UserModel(BaseModel):

	def __init__(self):
		super(UserModel, self).__init__()
		self.collection = self.mongo.get_collection('users')


	def create_user(self, userdata):
		userdata['password'] = hashlib.sha1(userdata['password']).hexdigest()
		self.collection.save(userdata)

	def check_user(self, userdata):
		userdata['password'] = hashlib.sha1(userdata['password']).hexdigest()
		result = self.collection.find_one({"username": userdata['username'],
			"password": userdata['password']})


		return result if result else {}


	def count_users(self):
		return self.collection.count()	

	def username_exists(self, username):
		result = self.collection.find({"username": username}).count()

		return result


	def update(self, data, id):
		id = self.mongo.get_object_id(id)

		servers = data.get('servers', None)
		if servers is not None:
			self.collection.update({"_id": id},{"$set": {"servers": data['servers']}} )

		password = data.get('password', None)
		if password is not None:
			data['password'] = hashlib.sha1(data['password']).hexdigest()
			self.collection.update({"_id": id},{"$set": {"password": data['password']}})

user_model = UserModel()