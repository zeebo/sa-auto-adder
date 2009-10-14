from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import ops
from google.appengine.ext import db

class WaveInfo(db.Model):
  wave_id = db.StringProperty(required=True)
  users_added = db.StringListProperty()
  wavelet_ids = db.StringListProperty()

class EventListener(object):    
  def on_wavelet_self_removed(self, properties, context):
    for wavelet in context.GetWavelets():
      query = db.Query(WaveletInfo)
      query.filter('wavelet_ids =', wavelet.GetId())
      for data in query:
        data.wavelet_ids.remove(wavelet.GetId())
        if data.wavelet_ids == []:
          data.delete()

  def on_wavelet_self_added(self, properties, context):
    for wavelet in context.GetWavelets():
      query = db.Query(WaveInfo)
      query.filter('wave_id =', wavelet.waveId)
      data = query.get()
      if data is None:
        data = WaveInfo(wave_id=wavelet.waveId)
      
      if wavelet.waveletId not in data.wavelet_ids:
        data.wavelet_ids.append(wavelet.waveletId)
      
      data.put()

  def on_blip_submitted(self, properties, context):
    for blip in context.GetBlips():
      if blip.GetDocument().GetText().find("list") != -1:
        self.find_all_waves(context)
        #self.notify(context.GetRootWavelet())
        
  def on_cron_event(self, properties, context):
    import logging
    logging.error("GOT A CRON EVENT!")
  
  def notify_text(self):
      return 'Participating in %d waves' % WaveInfo.all().count()
  
  def notify_all(self, context):
    text = self.notify_text()
    builder = ops.OpBuilder(context)
    for wave in WaveInfo.all():
      for wavelet_id in wave.wavelet_ids:
        blip = builder.WaveletAppendBlip(wave.wave_id, wavelet_id)

if __name__ == '__main__':
  myRobot = robot.Robot('SA Auto Adder', 
      image_url='http://sa-auto-adder.appspot.com/icon.png',
      version='2.10',
      profile_url='http://sa-auto-adder.appspot.com/')
  myRobot.RegisterListener(EventListener())
  myRobot.RegisterCronJob('http://sa-auto-adder.appspot.com/_wave/cron', 60)
  myRobot.Run(debug=True)