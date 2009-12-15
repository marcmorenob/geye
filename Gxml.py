#!/usr/bin/env python

"""
Geye setting load/save file 
"""
__author__ = 'moluxs@gmail.com (Marc Moreno)'

from xml.etree import ElementTree as ET
import os

class Gxml:

 def __init__(self):
  xml_file = os.path.abspath(__file__)
  xml_file = os.path.dirname(xml_file)
  self.xml_file = os.path.join(xml_file, "settings.xml")
  try :
   tree0 = ET.parse(self.xml_file)
  except Exception, inst:
    print "Unexpected error opening %s: %s" % (self.xml_file, inst)

  self.tree=tree0
  self.Cal_instance=self.tree.getroot().find("Calendar")
  self.Talarm=self.Cal_instance.find("Talarm")
  self.Trefresh=self.Cal_instance.find("Trefresh")
  self.Tdays=self.Cal_instance.find("Tdays")
  self.Mail_instance=self.tree.getroot().find("Mail")
  self.MEnable=self.Mail_instance.find("MEnable")
  self.MTrefresh=self.Mail_instance.find("MTrefresh")

 def get_Talarm(self):
  return self.Talarm.text

 def set_Talarm(self,NewTalarm):
  self.Talarm.text=NewTalarm

 def get_Tdays(self):
  return self.Tdays.text

 def set_Tdays(self,NewTdays):
  self.Tdays.text=NewTdays

 def get_Trefresh(self):
  return self.Trefresh.text

 def set_Trefresh(self,NewTrefresh):
  self.Trefresh.text=NewTrefresh

 def set_MTrefresh(self,NewMTrefresh):
  self.MTrefresh.text=NewMTrefresh

 def get_MTrefresh(self):
  return self.MTrefresh.text

 def set_MEnable(self,NewMEnable):
  self.MEnable.text=NewMEnable

 def get_MEnable(self):
  return self.MEnable.text

 def save_config(self):
  self.tree.write(self.xml_file)


