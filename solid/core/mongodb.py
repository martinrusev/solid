import os
try:
	import pymongo
except ImportError:
	pymongo = None

try:
	import bson
except ImportError:
	bson = None
import re 

from solid.core.exceptions import ImproperlyConfigured
from solid.core import settings

class MongoBackend():


	internal_collections = ['sessions','users',]

	database = 'solid'

	try: 
		if os.environ['SOLID_TEST_ENV'] == 'True':
			database = 'solid_test' # For the test suite
	except: 
		pass
	

	def __init__(self):
		if not pymongo:
			raise ImproperlyConfigured(
					"You need to install the pymongo library to use the "
					"MongoDB backend.")

		self.pymongo = pymongo
		self.url = settings.MONGO
		self._database = None
		self._connection = None

	def get_connection(self):
		"""Connect to the MongoDB server."""
		from pymongo import MongoClient

		if self._connection is None:
			self._connection = MongoClient(host=self.url, max_pool_size=10)

		return self._connection


	def get_database(self, database=None):
		""""Get or create database  """
		database = database if database !=None else self.database
		
		if self._database is None:
			conn = self.get_connection()
			db = conn[database]
			self._database = db
		
		return self._database


	def get_collection(self, collection, append=None, prefix=''):
		db = self.get_database()

		if collection in self.internal_collections or append is False:
			collection = "{0}".format(collection) # protect the collection that Amon uses internally
		else:
			collection = "amon_{0}{1}".format(prefix, collection)

		collection = db[collection]

		return collection


	def index(self, collection):
		collection = self.get_collection(collection)
		collection.ensure_index([('time', pymongo.DESCENDING)])


	def get_object_id(self,id):
		return bson.objectid.ObjectId(id)

	def string_to_valid_collection_name(self, string):
		return re.sub(r'[^\w]', '', str(string)).strip().lower()


backend = MongoBackend()
