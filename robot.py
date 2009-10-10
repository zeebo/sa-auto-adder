#!/usr/bin/env python
from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document

if __name__ == '__main__':
  myRobot = robot.Robot('sa-auto-adder', 
      image_url='http://sa-auto-adder.appspot.com/assets/icon.png',
      version='1',
      profile_url='http://sa-auto-adder.appspot.com/')
  myRobot.Run()
