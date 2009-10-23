from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import ops
from google.appengine.ext import db
from model.models import WaveletInfo, User, TaskQueue
import logging

class TaskHandler(object):
  def __init__(self, context):
    self._context = context
  
  def do(self, task):
    getattr(self, "do_%s" % task.op_type)(task, self._context)
  
  def do_add_participant(self, task, context):
    builder = ops.OpBuilder(context)
    builder.WaveletAddParticipant(task.wave_id,
                                  task.wavelet_id,
                                  task.participant_id)
    logging.debug("Added participant %s" % task.participant_id)
  

class EventListener(object):    
  def on_wavelet_self_removed(self, properties, context):
    #this isnt implemented on googles end yet unfortunatley
    #im leaving it in the code for when they do though!
    
    #of course this code entirely fails when run so its only
    #here for reference as to how it might work
    
    #for wavelet in context.GetWavelets():
    #  query = db.Query(WaveletInfo)
    #  query.filter('wavelet_ids =', wavelet.GetId())
    #  for data in query:
    #    data.wavelet_ids.remove(wavelet.GetId())
    #    if data.wavelet_ids == []:
    #      data.delete()
    logging.error('HOLY FUCK IT WAS REMOVED')
  
  def on_wavelet_self_added(self, properties, context):
    self.on_cron_event(properties, context)
    for wavelet in context.GetWavelets():
      query = db.Query(WaveletInfo)
      query.filter('wave_id =', wavelet.waveId)
      query.filter('wavelet_id =', wavelet.waveletId)
      data = query.get()
      if data is None:
        user_query = db.Query(User)
        user_query.filter('wave_address =', wavelet.creator)
        admin = user_query.get()
        if admin is None:
          #Not in our users db!
          #Option 1. Leave the wave (Not implemented yet)
          #Option 2. Add a blip saying hey register here
          #Option 3. Show the wave on the website as a non-goon wave
          #Option 4. Do nothing (easiest to code!)
          logging.debug('Added to a wave with no matching admin')
        else:
          while True:
            short_url = hashlib.sha1(str(random.random())).hexdigest()[:10]
            url_query = db.Query(WaveletInfo)
            query.filter('short_url =', short_url)
            if query.get() is None:
              break
          
          data = WaveletInfo(wave_id=wavelet.waveId,
                             wavelet_id=wavelet.waveletId,
                             admin=admin,
                             root_blip=wavelet.rootBlipId,
                             title=wavelet.title,
                             short_url=short_url)
          data.put()
      else:
        logging.debug("Added to a wavelet I was supposed to be in already!")
  
  def on_blip_submitted(self, properties, context):
    self.on_cron_event(properties, context)
    for blip in context.GetBlips():
      blip_wavelet = context.GetWaveletById(blip.waveletId)
      if blip.IsRoot() and blip_wavelet is not None:
        query = db.Query(WaveletInfo)
        query.filter('root_blip =', blip.blipId)
        wavelet = query.get()
        if wavelet is not None:
          if blip.waveletId == wavelet.wavelet_id:
            if wavelet.title != blip_wavelet.title:
              wavelet.title = blip_wavelet.title
              wavelet.put()
  
  def on_cron_event(self, properties, context):
    handler = TaskHandler(context)
    for task in TaskQueue.all():
      handler.do(task)
      task.delete()

if __name__ == '__main__':
  myRobot = robot.Robot('SA Auto Adder', 
      image_url='http://sa-auto-adder.appspot.com/icon.png',
      version='2.18',
      profile_url='http://sa-auto-adder.appspot.com/')
  myRobot.RegisterListener(EventListener())
  myRobot.RegisterCronJob('http://sa-auto-adder.appspot.com/_wave/cron', 60)
  myRobot.Run(debug=True)