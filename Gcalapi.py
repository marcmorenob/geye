#!/usr/bin/python
"""
Google Calendar bar tool for ubuntu
based on CalendarExample from Google code 
"""
__author__ = 'moluxs@gmail.com (Marc Moreno)'

#Code based on Ryan Boyd(api.rboyd@gmail.com) sample implementation
#Web: http://code.google.com/apis/calendar/


import pygtk
pygtk.require('2.0')
import gtk
import pynotify


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
from gdata.service import BadAuthentication
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time

class Authentications_fail(Exception):
  pass

class Internet_connection_lost(Exception):
  pass

class Calendarapi:

  def __init__(self, email, password,Talarm,Tdays,Sicon):

    self.cal_client = gdata.calendar.service.CalendarService()
    self.cal_client.email = email
    self.cal_client.password = password
    self.cal_client.source = 'Google-Calendar_Python_Sample-1.0'
    try:
     self.cal_client.ProgrammaticLogin() # Login on Google Calendar Server
     self.alert_minuts=60*int(Talarm)
     self.until_days=86400*int(Tdays)
     self.Sicon=Sicon # Geye icon in top panel
     pynotify.init("Cal") 
     self.no=0 #Calendar notify variable
    except BadAuthentication:
	raise Authentications_fail
    except IOError:
	raise Internet_connection_lost
    
  def _List_events(self):

	# Window of List event
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(500, 500)
        window.set_title("Calendars events")
        window.connect("delete_event", lambda w,e: gtk.main_quit())
	window.set_icon_from_file("img/iris.png")
	window.set_position(gtk.WIN_POS_CENTER)

	vbox = gtk.VBox(spacing=15)
	vbox.set_homogeneous(False)
        vbox.set_spacing(5)
        vbox.show()
        treestore = gtk.TreeStore(str)
	
	feed=0
        try:
	 feed = self.cal_client.GetAllCalendarsFeed() #Get all Calendar of the user
	except IOError:
	    raise Internet_connection_lost
	    return 

	for i, a_calendar in zip(xrange(len(feed.entry)), feed.entry):
	 Gcal_name='%s' % (a_calendar.title.text,)
	 piter = treestore.append(None, [Gcal_name])
	 gcal = '%s' % a_calendar.GetEditLink().href.split('/')[8]
	 gcal = gcal.replace("%40","@")
	 gcal = gcal.replace("%23","#")
         query = gdata.calendar.service.CalendarEventQuery(gcal, 'private','full')
	 query.start_min = time.strftime('%Y-%m-%dT%H:%M:%S.000+01:00', time.gmtime(time.time()))
	 query.start_max = time.strftime('%Y-%m-%d', time.gmtime(time.time()+self.until_days)) # Until X days
         query.orderby= "starttime"
         query.sortorder="ascending"
         feedd = self.cal_client.CalendarQuery(query) #Get all events between two dates, for each calendar
         for j, an_event in zip(xrange(len(feedd.entry)), feedd.entry): 
	  piterB = treestore.append(piter, ['%s' % (an_event.title.text,)])
	  for a_when in an_event.when:
	   if(len(a_when.start_time.split('T')) > 1):  #Distinge between all day events or events with start and end time
	    treestore.append(piterB, ['Start time: %s %s' % (a_when.start_time.split('T')[0],a_when.start_time.split('T')[1].split('.')[0])])
	    treestore.append(piterB, ['End time:   %s %s' % (a_when.end_time.split('T')[0],a_when.end_time.split('T')[1].split('.')[0])])
	   else:
	    treestore.append(piterB, ['Start time: %s' % a_when.start_time])
	    treestore.append(piterB, ['End time:   %s' % a_when.end_time])

        # create the TreeView using treestore
        treeview = gtk.TreeView(treestore)
	treeview.set_model(treestore) 
        tvcolumn = gtk.TreeViewColumn('Events')
        treeview.append_column(tvcolumn)
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 0)
        treeview.set_reorderable(True) 

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_vadjustment(gtk.Adjustment(300))
        scrolled_window.add_with_viewport(treeview) 

        vbox.pack_start(scrolled_window,True,True,0)
        closebtn = gtk.Button(stock=gtk.STOCK_CLOSE)
        closebtn.connect("clicked", lambda w: window.destroy())
	closebtn.set_border_width(10)
	closebtn.set_size_request(100, 70);
	hbox = gtk.HBox();
        hbox.pack_end(closebtn,False,True,0)
        vbox.pack_start(hbox,False,True,0)
        window.add(vbox)
	window.show_all()

  def _User_notify(self,mss):
	#Show notify message
	self.no = pynotify.Notification("Calendar notifier", mss)
	self.no.set_timeout(5000)
	self.no.show()

  def _close(self):
	if(self.no != 0):
         self.no.close()

  def _Find_alert(self): #Analise all events in all calendars looking for an event to notify
	feed=0
	try:
	 feed = self.cal_client.GetAllCalendarsFeed()
	except IOError:
	    raise Internet_connection_lost
	    return
	for i, b_calendar in zip(xrange(len(feed.entry)), feed.entry):
	 Gcal_name='%s' % (b_calendar.title.text,)
	 gcal = '%s' % b_calendar.GetEditLink().href.split('/')[8]
	 gcal = gcal.replace("%40","@")
	 gcal = gcal.replace("%23","#")
         query = gdata.calendar.service.CalendarEventQuery(gcal, 'private','full')
	 current = time.time()
	 Talert = time.strftime('%Y-%m-%dT%H:%M:00.000+01:00', time.gmtime((current+3600+self.alert_minuts)))#Looking for events
	 query.start_min = Talert
	 query.start_max = time.strftime('%Y-%m-%dT%H:%M:00.000+01:00', time.gmtime((current+3660+self.alert_minuts)))
         Afeed = self.cal_client.CalendarQuery(query) 
         for j, bn_event in zip(xrange(len(Afeed.entry)), Afeed.entry):
 	  for b_when in bn_event.when:
	   if(len(b_when.start_time.split('T')) > 1):
	    if(b_when.start_time == Talert):
	     self._User_notify('%s: %s' %(b_calendar.title.text,bn_event.title.text)) #Show event to user from calendar
	  
	 #Time until the next meeting. 
	 query.start_min = time.strftime('%Y-%m-%dT%H:%M:%S.000+01:00', time.gmtime(current+3600))
	 query.start_max = time.strftime('%Y-%m-%d', time.gmtime(current+self.until_days)) # Until 1 month after
         query.orderby= "starttime"
         query.sortorder="ascending"
         Afeed = self.cal_client.CalendarQuery(query) 
	 if(i==0):
	  nextmeeting_time=""
	  nextmeeting_calendar = b_calendar.title.text
	  nextmeeting_event=""
	 for j, an_event in zip(xrange(len(Afeed.entry)), Afeed.entry): 
	  for a_when in an_event.when:
	   if(len(a_when.start_time.split('T')) > 1):  #Distinge between all day events or events with start and end time
	    if( nextmeeting_time=="" or time.mktime(time.strptime(a_when.start_time,"%Y-%m-%dT%H:%M:%S.000+01:00")) < nextmeeting_time):
	      nextmeeting_time= time.mktime(time.strptime(a_when.start_time,"%Y-%m-%dT%H:%M:%S.000+01:00"))
	      nextmeeting_calendar = b_calendar.title.text
	      nextmeeting_event=an_event.title.text

	self.Sicon.set_tooltip("Next Meeting\n-----------------------\n %s \n %s: %s " %(time.strftime('%H hours %M minutes', time.gmtime(nextmeeting_time-current)),nextmeeting_calendar,nextmeeting_event)) #The text is shown when you put your mouse over top-panel Geye icon
	return True
  
  def _Find_calendars(self): #Find all my calendars
	feed=0
	try:
	 feed = self.cal_client.GetAllCalendarsFeed()
	except IOError:
	    raise Internet_connection_lost
	    return 
	Gcal_name= list()
	for i, b_calendar in zip(xrange(len(feed.entry)), feed.entry):
	 Gcal_name.insert(i,b_calendar.title.text)
	return Gcal_name
  
  def _InsertEvent(self, calendar='Default', title='Event', 
      start_time=None, end_time=None,content=None, where=None,recurrence_data=None): #Insert event in one calendar

    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.when.append(gdata.calendar.When(start_time,end_time))
    
    try:
     feed = self.cal_client.GetAllCalendarsFeed() #Get all Calendar of the user
    except IOError:
      raise Internet_connection_lost
      return 
    for i, a_calendar in zip(xrange(len(feed.entry)), feed.entry):
	if(a_calendar.title.text == calendar ):
	 gcal = '%s' % a_calendar.GetEditLink().href.split('/')[8]
	 gcal = gcal.replace("%40","@")
	 gcal = gcal.replace("%23","#")
	 break

    new_event = self.cal_client.InsertEvent(event, 
        '/calendar/feeds/%s/private/full' % gcal)
    

    


