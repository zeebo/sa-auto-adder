from modules.request_object import RequestObject
from models.user import User
from models.waveletinfo import WaveletInfo
from models.taskqueue import TaskQueue
from google.appengine.ext import db
import hashlib, random
import logging

class WaveletHandler(RequestObject):
  def do_init(self):
    pass
  
  def get_wavelet_from_shorturl(self, short_url):
    query = db.Query(WaveletInfo)
    query.filter('short_url', short_url)
    wavelet = query.get()
    if wavelet is None:
      raise Exception, "invalid short url"
    return wavelet
  
  def toggle_visibility(self, admin, short_url):
    wavelet = self.get_wavelet_from_shorturl(short_url)
    
    if wavelet.admin.key() != admin.key():
      raise Exception, 'you aren\'t the admin of that wavelet'
    
    wavelet.visible = not wavelet.visible
    wavelet.put()
  
  def remove_user_from_wavelet(self, for_user, short_url):
    wavelet = self.get_wavelet_from_shorturl(short_url)
    
    task_query = db.Query(TaskQueue)
    task_query.filter('user', for_user)
    task_query.filter('wavelet_key', wavelet.key())
    task = task_query.get()
    
    if task is None:
      raise Exception, 'no matching task'
    
    if for_user.username not in wavelet.users_added:
      raise Exception, 'username not in wavelet list'
    
    wavelet.users_added.remove(for_user.username)
    wavelet.put()
    task.delete()
  
  def queued_wavelets(self, for_user):
    task_query = db.Query(TaskQueue)
    task_query.filter('op_type', 'add_participant')
    task_query.filter('user', for_user)
    keys = [task.wavelet_key for task in task_query]
    logging.error(keys)
    wave_query = db.Query(WaveletInfo)
    wave_query.filter('__key__ IN', keys)
    return list(wave_query)
  
  def add_user_to_wavelet(self, user, short_url):
    wavelet = self.get_wavelet_from_shorturl(short_url)
    
    if not wavelet.visible:
      raise Exception, 'unable to join that wavelet'
    
    if user.username in wavelet.users_added:
      raise Exception, 'already in that wavelet (check queue)'
    
    task = TaskQueue(user=user, op_type='add_participant')
    task.wavelet_key = wavelet.key()
    task.wavelet_id = wavelet.wavelet_id
    task.wave_id = wavelet.wave_id
    task.wavelet_title = wavelet.title
    task.participant_id = user.wave_address
    task.put()
    
    wavelet.users_added.append(user.username)
    wavelet.put()
  
  def visible_wavelets(self, for_user=None):
    query = db.Query(WaveletInfo)
    query.filter('visible', True)
    query.filter('admin !=', for_user)
    def wavelet_filter(wavelet):
      try:
        return for_user.username not in wavelet.users_added
      except AttributeError:
        return True
    return filter(wavelet_filter, query)
  
  def admin_wavelets(self, for_user=None):
    query = db.Query(WaveletInfo)
    query.filter('admin', for_user)
    return query