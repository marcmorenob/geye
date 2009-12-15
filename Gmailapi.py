#!/usr/bin/python
"""
Geye Gmail api file
"""
__author__ = 'moluxs@gmail.com (Marc Moreno)'


import pygtk
pygtk.require('2.0')
import gtk
import pynotify

import imaplib
import time

class Account_acces_fail(Exception):
  def __init__(self,message):
    self.mss=message
  
  def getMss(self):
   return self.mss


class mailapi:

  def __init__(self, email, password):
    self.IMAPlink = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    self.IMAPlink.login(email, password)
    self.IMAPlink.select(readonly=1)
    self.lastDate=0 #Save last e-mail date notified
    pynotify.init("Mail")
    self.p=0 #Mail notify variable

  def _close(self):
   self.IMAPlink.logout()
   if (self.p != 0):
    self.p.close()

  def _user_notify(self,mss,Nmails):
    #Show notify message
    print "%s new Mails -- Mail num: %s \n%s" %(Nmails,Nmails,mss)
    self.p = pynotify.Notification("Mail notifier", mss)
    self.p.set_timeout(5000)
    self.p.show()

  def _find_newmail(self): #Analise all events in all calendars looking for an event to notify
     self.IMAPlink.check() #Check looking for new e-mails in the inbox
     (retcode, messages) = self.IMAPlink.search(None, '(UNSEEN)') 
     if retcode == 'OK' and messages != ['']: 
	Nmails=0
        for mID in messages[0].split(' '): 
           (ret, mesginfo) = self.IMAPlink.fetch(mID, '(BODY[HEADER.FIELDS (SUBJECT FROM DATE)])') 
	   MDate=str(mesginfo).split("Date:")[1]
	   MDate=MDate.split("\\")[0]
	   MDate=MDate.split(",")[1]
	   MDate=MDate.split("+")[0]
	   if(self.lastDate < MDate):
	    self.lastDate=MDate
	    Msubject=str(mesginfo).split("Subject:")[1]
	    Msubject=Msubject.split("\\")[0]
	    Mfrom=str(mesginfo).split("From:")[1]
	    Mfrom=Mfrom.split("\\")[0]
	    MSS="Subject: %s\nFrom: %s" %(Msubject,Mfrom)
	    Nmails+=1

	if(Nmails > 0):
         self._user_notify(MSS,Nmails)

    
  
