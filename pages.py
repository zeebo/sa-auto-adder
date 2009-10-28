from modules.request import AuthenticatedBuilder, NotAuthenticatedBuilder
import logging
#this shit is so meta
NotAuthenticatedHandler = NotAuthenticatedBuilder('/panel')
AuthenticatedHandler = AuthenticatedBuilder('/')

class LoginPage(NotAuthenticatedHandler):
  def get(self):
    self.render('main.html', {'login_failed': self.auth.error})

class LoginAction(NotAuthenticatedHandler):
  def post(self):
    try:
      self.auth.login(self.request.get('username'),
                      self.request.get('password'))
      if self.request.get('remember'):
        self.auth.add_cookies(self.response)
      self.redirect('/panel')
    except Exception, error:
      self.flash.add_error(error)
      self.redirect('/')

class CreatePage(NotAuthenticatedHandler):
  def get(self):
    if self.request.get('newtoken'):
      self.user_maker.generate_token()
      self.redirect(self.request.path)
    else:
      self.render('create.html', {
                                  'token' : self.user_maker.token,
                                  'error' : self.user_maker.error
                                 })

class CreateAction(NotAuthenticatedHandler):
  def post(self):
    try:
      self.auth.login_as(self.user_maker.make_user(self.request))
    except Exception, error:
      self.flash.add_error(error)
    
    self.redirect('/create')
  
####################################

class JoinAction(AuthenticatedHandler):
  def get(self, short_url):
    try:
      self.wavelets.add_user_to_wavelet(self.auth.user, short_url)
      self.flash.add_info('added to wavelet')
    except Exception, error:
      self.flash.add_error(error)
    self.redirect('/panel/waves')
  
class AdminAction(AuthenticatedHandler):
  def get(self, short_url):
    try:
      self.wavelets.toggle_visibility(self.auth.user, short_url)
      self.flash.add_info('toggled wavelet')
    except Exception, error:
      self.flash.add_error(error)
    self.redirect('/panel/admin')

class LeaveAction(AuthenticatedHandler):
  def get(self, short_url):
    try:
      self.wavelets.remove_user_from_wavelet(self.auth.user, short_url)
      self.flash.add_info('removed from wavelet')
    except Exception, error:
      self.flash.add_error(error)
    self.redirect('/panel/queue')

class DeleteEventAction(AuthenticatedHandler):
  def get(self, key):
    try:
      self.events.delete_event(self.auth.user, key)
    except Exception, error:
      self.flash.add_error(error)
    self.redirect('/panel/events')

class PanelPage(AuthenticatedHandler):
  def get(self):
    self.redirect('/panel/events')
  
class PanelEventHandler(AuthenticatedHandler):
  def get(self):
    data = {
      'events': self.events.get_events(for_user=self.auth.user)
    }
    self.render('events.html', data)

class PanelQueueHandler(AuthenticatedHandler):
  def get(self):
    data = {
      'wavelets': self.wavelets.queued_wavelets(for_user=self.auth.user),
    }
    self.render('queue.html', data)

class PanelAdminHandler(AuthenticatedHandler):
  def get(self):
    data = {
      'wavelets': self.wavelets.admin_wavelets(for_user=self.auth.user),
    }
    self.render('admin.html', data)

class PanelWavesHandler(AuthenticatedHandler):
  def get(self):
    #must filter by:
      #1. not in task queue
      #2. admin != self.auth.user
    data = {
      'wavelets': self.wavelets.visible_wavelets(for_user=self.auth.user),
    }
    self.render('waves.html', data)

class EditUserHandler(AuthenticatedHandler):
  def get(self):
    self.render('edit.html', {})

class PanelHandler(AuthenticatedHandler):
  def get(self):
    self.render('panel.html', {})

class LogoutAction(AuthenticatedHandler):
  def get(self):
    self.auth.logout()
    self.auth.del_cookies(self.response)
    self.destory_session()
    self.render('logout.html', {})