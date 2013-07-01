from __future__ import division
import re
try:
	import json
except:
	import simplejson as json
from jinja2 import Environment, FileSystemLoader

from solid.core import settings
from solid.web.settings import TEMPLATES_DIR
from solid import __version__
from datetime import datetime, time
from solid.utils.dates import ( 
	utc_unixtime_to_localtime,
	utc_now_to_localtime,
	dateformat_local,
	dateformat,
	timeformat,
	timeformat_local,
	datestring_to_utc_datetime,
)

from solid.web.libs.jinja2htmlcompress import SelectiveHTMLCompress


def age(from_date, since_date = None, target_tz=None, include_seconds=False):
	'''
	Returns the age as a string
	'''
	since_date =  utc_now_to_localtime()
	from_date =  datestring_to_utc_datetime(from_date)



	distance_in_time = since_date - from_date
	distance_in_seconds = int(round(abs(distance_in_time.days * 86400 + distance_in_time.seconds)))
	distance_in_minutes = int(round(distance_in_seconds/60))

	if distance_in_minutes <= 1:
		if include_seconds:
			for remainder in [5, 10, 20]:
				if distance_in_seconds < remainder:
					return "less than %s seconds" % remainder
			if distance_in_seconds < 40:
				return "half a minute"
			elif distance_in_seconds < 60:
				return "less than a minute"
			else:
				return "1 minute"
		else:
			if distance_in_minutes == 0:
				return "less than a minute"
			else:
				return "1 minute"
	elif distance_in_minutes < 45:
		return "%s minutes" % distance_in_minutes
	elif distance_in_minutes < 90:
		return "about 1 hour"
	elif distance_in_minutes < 1440:
		return "about %d hours" % (round(distance_in_minutes / 60.0))
	elif distance_in_minutes < 2880:
		return "1 day"
	elif distance_in_minutes < 43220:
		return "%d days" % (round(distance_in_minutes / 1440))
	elif distance_in_minutes < 86400:
		return "about 1 month"
	elif distance_in_minutes < 525600:
		return "%d months" % (round(distance_in_minutes / 43200))
	elif distance_in_minutes < 1051200:
		return "about 1 year"
	else:
		return "over %d years" % (round(distance_in_minutes / 525600))


# Custom filters
def time_in_words(value):
	'''
	Usage: {{ my_date_variable|time_in_words }}
	'''
	time_ago = age(value)

	return time_ago


def date_to_js(value, format='%Y, %m, %d, %H, %M'):
	# Converts unixtime to a javascript Date list
	_ = datetime.utcfromtimestamp(value)
	js_time_list = _.strftime(format).split(',')
	# Substract one month in js January is 0, February is 1, etc.
	js_time_list[1] = str(int(js_time_list[1])-1) 

	return ",".join(js_time_list) 

def to_int(value):
	number = re.compile('(\d+)')

	try:
		_int = number.search(value).group(1)
	except:
		_int = 0

	return int(_int)

# TODO - write tests
def extract_days_from_unixdate(value, days):
	day = 86400 # 1 day in seconds

	return value-(day*days)

# Removes the letters from a string
# From 24.5MB -> 24.5 -> used in the progress width
def clean_string(variable):

	if isinstance(variable, int)\
	or isinstance(variable, float)\
	or isinstance(variable, long):
		
		variable = float(variable) if not isinstance(variable, float) else variable

		return variable

	else:

		value_regex = re.compile(r'\d+[\.,]\d+') 
		extracted_value = value_regex.findall(variable)

		if len(extracted_value) > 0:
			extracted_value = extracted_value[0]
			extracted_value.replace(",",".")
			extracted_value = float(extracted_value)
		else:
			extracted_value = 0

		return extracted_value


# Used in the charts, where a disk drive could be with several slashes
def clean_slashes(string):
	return re.sub('[^A-Za-z0-9]+', '', string).strip().lower()

class RecursiveDict(object):

	def __init__(self):
		self.html = ''

	def walk_dict_exception(self, d,depth=0):
		for k,v in sorted(d.items(),key=lambda x: x[0]):
			if isinstance(v, dict):
				# Continue the recursion only if the dictionary is not empty
				if v:
					self.html += u'<ul class="level-{0}">'.format(depth)
					# strip the mongo variable
					if k != 'data':
						self.html += u'<li><span class="key">{0}</span>'.format(k)
					self.walk_dict_exception(v,depth+1)
					self.html += '</li>'
					self.html += '</ul>'
			else:
				if v and k != 'occurrence':
					self.html += u'<li><span class="key_inner">{0}:</span><span class="value_inner">{1}</span></li>'.format(k,v)

def recursive_dict(dict):
	dict_recursion = RecursiveDict()
	dict_recursion.walk_dict_exception(dict)

	return dict_recursion.html


def check_additional_data(list_with_dicts):
	valid_keys = ['occurrence']

	for dict in list_with_dicts:
		for key in dict.keys():
			if key not in valid_keys:
				return True


# Combine several parameters with /
# Used in the base_url -> {{ base_url|url('system',) -> http://host/system
def url(*args):
	http_slash = '/'
	url = http_slash.join(args)

	return url


def beautify_json(value):
	if isinstance(value, dict):
		return json.dumps(value, indent=4) # Remove the unicode symbol
	else:
		return value

# Used in the log page. Displays the expand button if the value is dictionary
def is_dict(value):
	if isinstance(value, dict):
		return True
	else:
		return False

# Used in the log page. Checks the log tag
def is_str(value):
	if isinstance(value, str) or isinstance(value, unicode):
		return True
	else:
		return False

def get_active_page(value, key):
	elements = value.split(':')

	try:
		return elements[key]
	except:
		return None


# url -> usually the base url -> http://something.com
# params_dict -> dict {"tags": ['test', 'some'], "other_param": ['test']}
def query_dict(url, params_dict, page=None):

	query_lists = []
	for dict in params_dict:
		dict_items = []
		values_list = params_dict[dict]
		if values_list:
			for value in values_list:
				dict_items.append("{0}={1}".format(dict, value))
			# Join all the values
			query_lists.append("&".join(dict_items))

	# Finally separate the different params with ?
	query_string = url

	if len(query_lists) > 0:
		query_string+='?'
		query_string+= "?".join(query_lists)
		if page != None:
			query_string+="&page={0}".format(page)
	# No params - only the page number
	else:
		if page != None:
			query_string+="?page={0}".format(page)

	return query_string


def base_url():

	if settings.PROXY is None:
		host = settings.WEB_APP['host']
		port = settings.WEB_APP['port']

		base_url = "{0}:{1}".format(host, port)

		return base_url
	else:
		return ''

# Removes the scientific notation and displays floats normally
def format_float(value):
	return format(float(value), "g")


# Gets the key from a dictionary, doesn't break the template
def get_key(dict, key):
	value = dict.get(key, None)
	
	return value

def render(template, *args, **kwargs):

	env = Environment(loader=FileSystemLoader(TEMPLATES_DIR),
		extensions=[SelectiveHTMLCompress])

	env.globals['base_url'] = base_url()
	env.globals['version'] = __version__

	env.filters['url'] = url

	# Used everywhere
	env.filters['time'] = timeformat
	env.filters['time_local'] = timeformat_local
	env.filters['date_to_js'] = date_to_js
	env.filters['date'] = dateformat
	env.filters['date_local'] = dateformat_local
	env.filters['to_int'] =  to_int
	# env.filters['time_in_words'] = time_in_words 
	env.filters['recursive_dict'] = recursive_dict
	env.filters['check_additional_data'] = check_additional_data
	env.filters['clean_slashes'] = clean_slashes
	env.filters['beautify_json'] = beautify_json
	env.filters['get_active_page'] = get_active_page # Used to mark links as active
	env.filters['extract_days_from_unixdate'] = extract_days_from_unixdate
	env.filters['format_float'] = format_float

	# Log filters
	env.filters['is_dict'] = is_dict
	env.filters['is_str'] = is_str
	env.filters['query_dict'] = query_dict

	# Utilities
	env.filters['get_key'] = get_key

	try:
		template = env.get_template(template)
	except Exception, e:
		raise

	# Global variables
	env.globals['acl'] = settings.ACL

	return template.render(*args, **kwargs)

