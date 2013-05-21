import unittest
from nose.tools import eq_
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from solid.core.mongodb import backend

class TestMongoBackend(unittest.TestCase):
	
	def test_get_database(self):
		db = backend.get_database()
		eq_(db, Database(MongoClient(u'127.0.0.1', 27017), u'amon_test'))

	def test_get_connection(self):
		connection = backend.get_connection()
		eq_(connection, MongoClient(u'127.0.0.1', 27017))



		)


	def test_string_to_valid_collection_name(self):
		name = 'TEST123456'
		valid_name = backend.string_to_valid_collection_name(name)
		eq_(valid_name, 'test123456')



