import urllib, urllib2, Cookie, sys, logging, pickle
from modules.appengine_utilities import cache
from webinterface.sa_settings import SA_INFO
  
def valid_cookies(jar):
  valid = False
  if isinstance(jar,Cookie.BaseCookie):
    valid = 'bbpassword' in jar and 'bbuserid' in jar
  return valid

def download_cookies():
  logging.info('Attempting to log into SA')
  data = {
    "username": SA_INFO['username'],
    "password": SA_INFO['password'],
    "action": 'login',
  }
  try:
      handle = urllib2.urlopen('http://forums.somethingawful.com/account.php', urllib.urlencode(data))
  except urllib2.HTTPError:
    logging.info('Unable to get data from Something Awful')
    return None
  info = handle.info()
  jar = Cookie.BaseCookie()
  jar.load(info['set-cookie'])
  if valid_cookies(jar):
    return jar
  logging.error('Invalid SA username/password. Check sa_settings.py')
  return None

def get_cookies(cached=True, clear_cache=False):
  picklejar = cache.Cache()
  
  #horrible hack
  in_cache = False
  try:
    throw_away = picklejar['jar']
    in_cache = True
  except KeyError:
    pass
  
  if in_cache and clear_cache:
    del picklejar['jar']
    in_cache = False
  if in_cache and cached:
    jar = pickle.loads(picklejar['jar'])
  else:
    jar = download_cookies()
    if valid_cookies(jar):
      picklejar['jar'] = pickle.dumps(jar)
  
  return jar

def get_profile(username):
  jar = get_cookies()
  
  if jar is None:
    logging.error('Unable to retrieve profile for %s.' % username)
    return None
  
  header = ' '.join(["%s=%s;" % (key, jar[key].value) for key in jar if key[0:2] == 'bb'])
  request = urllib2.Request('http://forums.somethingawful.com/member.php?s=&action=getinfo&username=%s' % urllib.quote(username, ''))
  request.add_header('Cookie', header)
  try:
    return urllib2.urlopen(request)
  except urllib2.DownloadError:
    return None

def get_user_id(profile):
  search_string = '<input type="hidden" name="userid" value="'
  start = profile.find(search_string) + len(search_string)
  end = profile.find('">', start)
  uid = None
  try:
    uid = int(profile[start:end])
  except (IndexError, ValueError):
    pass
  return uid
