import unittest
from nose.tools import eq_

from solid.web.apps.core.acl import check_permissions

class TestACL(unittest.TestCase):

	def test_admin_user(self):
		user = {"type": "admin"}
		result = check_permissions(False,'/something', user)
		eq_(True, result)

		# Page with id
		result = check_permissions('1234','/something', user)
		eq_(True, result)

		# Settings
		result = check_permissions('/settings','/settings', user)
		eq_(True, result)

	def test_readonly_user(self):
		user = {"type": "readonly", "apps":["app1", "app2"], "servers":["server1", "server2"]}
		result = check_permissions(False,'/system', user) # Parent pages - id is False
		eq_(True, result)

		result = check_permissions(False,'/', user) # Parent pages - id is False
		eq_(True, result)

	



