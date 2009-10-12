#!/usr/bin/env python
from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document
import logging

def test_added(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("I'm alive!")

class RobotListener(object):
  def __init__(self):
    self.wavelets = []
    
  def on_wavelet_self_added(properties, context):
    for wavelet in context.GetWavelets():
      logging.info("Added to wave %s" % wavelet.GetId())
      self.wavelets.append(wavelet.GetId())
      
  def on_wavelet_self_removed(properties, context):
    for wavelet in context.GetWavelets():
      if wavelet.GetId() in self.wavelets:
        logging.info("Removed from wave %s" % wavelet.GetId())
        self.wavelets.remove(wavelet.GetId())

  def send_blips():
    for wavelet in self.wavelets:
      logging.info("Pinging %s" % wavelet.GetId())
      wavelet.CreateBlip().GetDocument().SetText("Ping!")

if __name__ == '__main__':
  logging.info("Robot called")
  event_handler = RobotListener()
  myRobot = robot.Robot('sa-auto-adder', 
      image_url='http://sa-auto-adder.appspot.com/assets/icon.png',
      version='2',
      profile_url='http://sa-auto-adder.appspot.com/')
  myRobot.RegisterCronJob(event_handler.send_blips, 30)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, test_added)
  myRobot.RegisterListener(event_handler)
  myRobot.Run()
