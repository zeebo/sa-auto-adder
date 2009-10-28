import urllib, urllib2, Cookie
from modules.appengine_utilities import cache
from google.appengine.api import urlfetch
import logging

class SAProfile(object):
  def __init__(self, username):
    self.__username = urllib.quote(username, '')
    self.__uid = None
    self.__profile_data = ''
    
  @property
  def profile(self):
    if self.__profile_data is '':
      self.__download_profile_data()
    return self.__profile_data
    
  @property
  def uid(self):
    if self.__uid is not None:
      return self.__uid
      
    search_string = '<input type="hidden" name="userid" value="'
    start = self.profile.find(search_string) + len(search_string)
    end = self.profile.find('">', start)
    try:
      self.__uid = int(self.profile[start:end])
    except (IndexError, ValueError):
      pass
    
    return self.__uid
  
  def has_token(self, token):
    return token in self.profile
  
  def get_cookies(self):
    from sa_settings import SA_INFO
    username, password = SA_INFO['username'], SA_INFO['password']
    cookie_cache = cache.Cache()
    if 'data' in cookie_cache:
      return cookie_cache['data']
    
    data = {
      "username": username,
      "password": password,
      "action": 'login',
    }
    try:
      handle = urllib2.urlopen('http://forums.somethingawful.com/account.php', 
                                urllib.urlencode(data))
    except urllib2.HTTPError:
      return ''
    jar = Cookie.BaseCookie(handle.info().get('set-cookie', ''))
    cookie_string = ' '.join(["%s=%s;" % (key, jar[key].value) \
                              for key in jar \
                              if key[0:2] == 'bb'])
                              
    cookie_cache['data'] = cookie_string
    return cookie_string
    
  def __download_profile_data(self):
    from sa_settings import SA_INFO
    url = 'http://forums.somethingawful.com/member.php?s=&action=getinfo' + \
          '&username=%s' % urllib.quote(self.__username, '')
    cookies = self.get_cookies()

    try:
      result = urlfetch.fetch(url=url, headers={'Cookie': cookies})
      if result.status_code == 200:
        self.__profile_data = result.content
    except urlfetch.DownloadError:
      pass