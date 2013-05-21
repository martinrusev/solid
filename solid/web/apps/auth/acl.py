def check_permissions(id, url, user):
	if user['type'] == 'admin':
		return True

	return False






