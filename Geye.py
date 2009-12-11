#!/usr/bin/python
"""
Geye is a gnome top panel tool with a basic interaction with Google Calendar.
Geye notifies new calendar events, X minutes before, inserts new events in your google calendars, list all events for each calendar and shows the time for the next meeting

"""
__author__ = 'moluxs@gmail.com (Marc Moreno)'

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pynotify
import time

# My class
import Gapi
from Gapi import Authentications_fail
from Gapi import Internet_connection_lost
import Gxml


class Geye:

    def __init__(self):
	#Load settings
	self.Gsettings=Gxml.Gxml()

	#Create Loggin window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(320, 240)
        self.window.set_title("Geye Login")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())
	self.window.set_icon_from_file("img/iris.png")
	self.window.set_position(gtk.WIN_POS_CENTER)

	vbox = gtk.VBox(False, 0)
        self.window.add(vbox)
        vbox.show()

        hbox0 = gtk.HBox(False, 0)
        vbox.pack_start(hbox0, True, True, 0)
        hbox0.show()


	label0 = gtk.Label("user: ");
        hbox0.pack_start(label0, True, True, 0)
	label0.show();

        self.eusr = gtk.Entry()
        self.eusr.set_max_length(50)
        hbox0.pack_start(self.eusr, False, True, 0)
        self.eusr.show()
	label0 = gtk.Label("@gmail.com ");
        hbox0.pack_start(label0, True, True, 0)
	label0.show();

        hbox1 = gtk.HBox(False, 0)
        vbox.pack_start(hbox1, True, True, 0)
        hbox1.show()

	label1 = gtk.Label("   pwd:    ");
        hbox1.pack_start(label1, False, True, 0)
	label1.show();

        self.epwd = gtk.Entry()
        self.epwd.set_max_length(50)
        self.epwd.set_visibility(False)
        hbox1.pack_start(self.epwd, False, True, 0)
        self.epwd.show()

        hbox2 = gtk.HBox(False, 0)
        vbox.pack_start(hbox2, False, True, 0)
        hbox2.show()

        startbtn = gtk.Button("Start")
        startbtn.connect("clicked", self.usrpwd_callback)
	startbtn.set_border_width(10)
	startbtn.set_size_request(100, 70);
	startbtn.enter()
        hbox2.pack_start(startbtn, True, True, 0)
        startbtn.set_flags(gtk.CAN_DEFAULT)
        startbtn.grab_default()
        startbtn.show()
                                 
        closebtn = gtk.Button(stock=gtk.STOCK_CLOSE)
        closebtn.connect("clicked", lambda w: gtk.main_quit())
	closebtn.set_border_width(10)
	closebtn.set_size_request(100, 70);
        hbox2.pack_start(closebtn, True, True, 0)
        closebtn.set_flags(gtk.CAN_DEFAULT)
        closebtn.grab_default()
        closebtn.show()

	#Create submenu rigth mouse button
        self.menu = gtk.Menu()
        self.populate_menu()
        self.Sicon=gtk.status_icon_new_from_file("img/iris.png")
	self.Sicon.connect("popup_menu", self.popup_menu_cb, self.menu)

	self.menu = gtk.Menu()
	self.window.set_focus(startbtn)
        self.window.show()


    def usrpwd_callback(self,widget):

        usr = self.eusr.get_text()
	usr += "@gmail.com"
        pwd = self.epwd.get_text()
	#Connect to Google Calendar
	try :
	 self.mycalendar = Gapi.Calendarapi(usr, pwd,self.Gsettings.get_Talarm(),self.Gsettings.get_Tdays(),self.Sicon)
	 self._falert()
	 self.gtimer=gobject.timeout_add(int(self.Gsettings.get_Trefresh()),self._falert)
	 self.window.hide()
        except Authentications_fail:
	 self.werrorm("Incorrect user or password")
	 self.window.show()
        except Internet_connection_lost:
	 self.Sicon.set_from_file("img/irisR.png");
	 self.Sicon.set_tooltip("No Internet connection")
	 self.werrorm("No Internet connection")
	 self.window.show()

    def _falert(self): # List all events for each calendar
	try:	
	 self.mycalendar._Find_alert()
	 self.Sicon.set_from_file("img/iris.png");
        except Internet_connection_lost:
	 self.Sicon.set_from_file("img/irisR.png");
	 self.Sicon.set_tooltip("No Internet connection")

    def _menuitem_List(self,widget): # List all events for each calendar
	try:	
	 self.mycalendar._List_events()
        except Internet_connection_lost:
	 self.Sicon.set_from_file("img/irisR.png");
	 self.Sicon.set_tooltip("No Internet connection")
	 self.werrorm("No Internet connection")

    def _intsert_event(self,widget,window):
	try:
	 self.mycalendar._InsertEvent(self.combo.get_active_text(),self.title.get_text(),'%sT%s:00.000+01:00' %(self.sdate.get_text(),self.stime.get_text()),'%sT%s:00.000+01:00' %(self.edate.get_text(),self.etime.get_text()))
	 window.destroy()
        except Internet_connection_lost:
	 self.Sicon.set_from_file("img/irisR.png");
	 self.Sicon.set_tooltip("No Internet connection")
	 self.werrorm("No Internet connection")
	 return


    def _menuitem_Insert(self,widget): #Menu for insert new events in a selected calendar

	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(350, 300)
        window.set_title("Geye insert event")
	window.set_icon_from_file("img/iris.png")
	window.set_position(gtk.WIN_POS_CENTER)


	vbox = gtk.VBox(False, 0)
        window.add(vbox)
        vbox.show()


        hbox_1 = gtk.HBox(False, 0)
        vbox.pack_start(hbox_1, False, True, 10)
        hbox_1.show()

	label_1 = gtk.Label(" Calendar:   ");
        hbox_1.pack_start(label_1, False, True, 0)
	label_1.show();
        self.combo = gtk.ComboBox()
        ls = gtk.ListStore(str)
	feed=0
	try:
	 feed = self.mycalendar._Find_calendars() #Find our calendars
        except Internet_connection_lost:
	 self.Sicon.set_from_file("img/irisR.png");
	 self.werrorm("No Internet connection")
	 return
	for i in range(0,len(feed)):
           ls.append([feed[i]])
        self.combo.set_model(ls)
        cellr = gtk.CellRendererText()
        self.combo.pack_start(cellr)
        self.combo.add_attribute(cellr, 'text', 0)
	hbox_1.pack_start(self.combo, False, True, 0)
	self.combo.set_active(0)
	self.combo.show()

        hbox0 = gtk.HBox(False, 0)
        vbox.pack_start(hbox0, True, True, 0)
        hbox0.show()

	label0 = gtk.Label(" Title:          ");
        hbox0.pack_start(label0, False, True, 0)
	label0.show();

        self.title = gtk.Entry()
        self.title.set_max_length(50)
        self.title.set_text("")
        hbox0.pack_start(self.title, False, True, 0)
        self.title.show()

        hbox1 = gtk.HBox(False, 0)
        vbox.pack_start(hbox1, True, True, 0)
        hbox1.show()

	label1 = gtk.Label(" Start Date: ");
        hbox1.pack_start(label1, False, True, 0)
	label1.show();

	current = time.time()
	cdate = time.strftime('%Y-%m-%d', time.gmtime(current))

        self.sdate = gtk.Entry()
        self.sdate.set_max_length(50)
        self.sdate.set_text(cdate)
        hbox1.pack_start(self.sdate, False, True, 0)
        self.sdate.show()

	label11 = gtk.Label(" YYYY-MM-DD");
        hbox1.pack_start(label11, False, True, 0)
	label11.show();

        hbox2 = gtk.HBox(False, 0)
        vbox.pack_start(hbox2, True, True, 0)
        hbox2.show()

	ctime = time.strftime('%H:00', time.gmtime(current))

	label2 = gtk.Label(" Start Time: ");
        hbox2.pack_start(label2, False, True, 0)
	label2.show();

        self.stime = gtk.Entry()
        self.stime.set_max_length(50)
        self.stime.set_text(ctime)
        hbox2.pack_start(self.stime, False, True, 0)
        self.stime.show()

	label21 = gtk.Label(" HH:MM");
        hbox2.pack_start(label21, False, True, 0)
	label21.show();

        hbox3 = gtk.HBox(False, 0)
        vbox.pack_start(hbox3, True, True, 0)
        hbox3.show()

	label3 = gtk.Label(" End Date:   ");
        hbox3.pack_start(label3, False, True, 0)
	label3.show();

        self.edate = gtk.Entry()
        self.edate.set_max_length(50)
        self.edate.set_text(cdate)
        hbox3.pack_start(self.edate, False, True, 0)
        self.edate.show()

	label31 = gtk.Label(" YYYY-MM-DD");
        hbox3.pack_start(label31, False, True, 0)
	label31.show();

        hbox4 = gtk.HBox(False, 0)
        vbox.pack_start(hbox4, True, True, 0)
        hbox4.show()

	ctime = time.strftime('%H:00', time.gmtime((current+3600)))
	label4 = gtk.Label(" End Time:   ");
        hbox4.pack_start(label4, False, True, 0)
	label4.show();

        self.etime = gtk.Entry()
        self.etime.set_max_length(50)
        self.etime.set_text(ctime)
        hbox4.pack_start(self.etime, False, True, 0)
        self.etime.show()

	label41 = gtk.Label(" HH:MM");
        hbox4.pack_start(label41, False, True, 0)
	label41.show();



        hbox5 = gtk.HBox(False, 0)
        vbox.pack_start(hbox5, False, True, 0)
        hbox5.show()

        savebtn = gtk.Button("Insert")
        savebtn.connect("clicked", self._intsert_event,window)
	savebtn.set_border_width(10)
	savebtn.set_size_request(80, 55);
	savebtn.enter()
        hbox5.pack_start(savebtn, True, True, 0)
        savebtn.set_flags(gtk.CAN_DEFAULT)
        savebtn.grab_default()
        savebtn.show()
                                 
        closebtn = gtk.Button(stock=gtk.STOCK_CLOSE)
        closebtn.connect("clicked", lambda w: window.destroy())
	closebtn.set_border_width(10)
	closebtn.set_size_request(80, 55);
        hbox5.pack_start(closebtn, True, True, 0)
        closebtn.set_flags(gtk.CAN_DEFAULT)
        closebtn.grab_default()
        closebtn.show()
	window.set_focus(savebtn)
        window.show()




    def	_save_Configure(self,widget,window): #Apply and save new Geye settings
	 window.destroy()
	 self.Gsettings.set_Talarm(self.Talarm.get_text())
	 self.mycalendar.alert_minuts=60*int(self.Talarm.get_text())
         if(self.Gsettings.get_Trefresh() != self.Trefresh.get_text()):
	  self.Gsettings.set_Trefresh(self.Trefresh.get_text())
	  gobject.source_remove(self.gtimer) # Remove previous time_out instance
	  self.gtimer=gobject.timeout_add(int(self.Trefresh.get_text()),self.mycalendar._Find_alert)
	 self.Gsettings.set_Tdays(self.Tdays.get_text())
	 self.until_days=86400*int(self.Tdays.get_text())
	 self.Gsettings.save_config()

    def	_menuitem_Configure(self,widget): #Settings menu
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(350, 200)
        window.set_title("Geye Settings")
	window.set_icon_from_file("img/iris.png")
	window.set_position(gtk.WIN_POS_CENTER)


	vbox = gtk.VBox(False, 0)
        window.add(vbox)
        vbox.show()

        hbox0 = gtk.HBox(False, 0)
        vbox.pack_start(hbox0, False, True, 10)
        hbox0.show()


	label0 = gtk.Label("    Time notify: ");
        hbox0.pack_start(label0, False, True, 0)
	label0.show();

        self.Talarm = gtk.Entry()
        self.Talarm.set_max_length(50)
        self.Talarm.set_text(self.Gsettings.get_Talarm())
        hbox0.pack_start(self.Talarm, False, True, 0)
        self.Talarm.show()

        hbox1 = gtk.HBox(False, 0)
        vbox.pack_start(hbox1, False, True, 10)
        hbox1.show()

	label1 = gtk.Label("    Recheck calendar:  ");
        hbox1.pack_start(label1, False, True, 0)
	label1.show();

        self.Trefresh = gtk.Entry()
        self.Trefresh.set_max_length(50)
        self.Trefresh.set_text(self.Gsettings.get_Trefresh())
        hbox1.pack_start(self.Trefresh, False, True, 0)
        self.Trefresh.show()

        hbox2 = gtk.HBox(False, 0)
        vbox.pack_start(hbox2, False, True, 10)
        hbox2.show()

	label2 = gtk.Label("    List Events until:  ");
        hbox2.pack_start(label2, False, True, 0)
	label2.show();

        self.Tdays = gtk.Entry()
        self.Tdays.set_max_length(50)
        self.Tdays.set_text(self.Gsettings.get_Tdays())
        hbox2.pack_start(self.Tdays, False, True, 0)
        self.Tdays.show()

	label3 = gtk.Label(" Days");
        hbox2.pack_start(label3, False, True, 0)
	label3.show();

        hbox3 = gtk.HBox(False, 0)
        vbox.pack_start(hbox3, False, True, 0)
        hbox3.show()

        savebtn = gtk.Button("Save")
        savebtn.connect("clicked", self._save_Configure,window)
	savebtn.set_border_width(10)
	savebtn.set_size_request(80, 55);
	savebtn.enter()
        hbox3.pack_start(savebtn, True, True, 0)
        savebtn.set_flags(gtk.CAN_DEFAULT)
        savebtn.grab_default()
        savebtn.show()
                                 
        closebtn = gtk.Button(stock=gtk.STOCK_CLOSE)
        closebtn.connect("clicked", lambda w: window.destroy())
	closebtn.set_border_width(10)
	closebtn.set_size_request(80, 55);
        hbox3.pack_start(closebtn, True, True, 0)
        closebtn.set_flags(gtk.CAN_DEFAULT)
        closebtn.grab_default()
        closebtn.show()
	window.set_focus(savebtn)
        window.show()


    def _menuitem_Logout(self,widget):
 	  self.window.show()

    def _halt_app(self,widget):
	gobject.source_remove(self.gtimer) # Remove time_out instance
	gtk.main_quit()

    def _license_win(self,widget): #License window
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(375, 350)
        window.set_title("License Geye")
	window.set_icon_from_file("img/iris.png")
	window.set_position(gtk.WIN_POS_CENTER)

	vbox=gtk.VBox()	
	licensescroller = gtk.ScrolledWindow()
        licensetextarea = gtk.TextView()
        licensescroller.set_vadjustment(gtk.Adjustment(300))
        licensescroller.add_with_viewport(licensetextarea)
        
   	licensetextarea.get_buffer().insert_at_cursor(' This program is free software: you can redistribute it\n')
   	licensetextarea.get_buffer().insert_at_cursor(' and/or modify it under the terms of the GNU General\n')
   	licensetextarea.get_buffer().insert_at_cursor(' Public License version 3, as published by the Free \n')
   	licensetextarea.get_buffer().insert_at_cursor(' Software Foundation. \n')
   	licensetextarea.get_buffer().insert_at_cursor(' \n')
   	licensetextarea.get_buffer().insert_at_cursor(' This program is distributed in the hope that it will be\n')
   	licensetextarea.get_buffer().insert_at_cursor(' useful, but WITHOUT ANY WARRANTY; without even\n')
   	licensetextarea.get_buffer().insert_at_cursor(' the implied warranties of MERCHANTABILITY,\n')
   	licensetextarea.get_buffer().insert_at_cursor(' SATISFACTORY QUALITY, or FITNESS FOR A\n')
   	licensetextarea.get_buffer().insert_at_cursor(' PARTICULAR PURPOSE.  See the GNU General Public\n')
   	licensetextarea.get_buffer().insert_at_cursor(' License for more details. \n')
   	licensetextarea.get_buffer().insert_at_cursor('  \n')
   	licensetextarea.get_buffer().insert_at_cursor(' You should have received a copy of the GNU General \n')
   	licensetextarea.get_buffer().insert_at_cursor(' Public License along with this program.  If not, see \n')
   	licensetextarea.get_buffer().insert_at_cursor(' <http://www.gnu.org/licenses/>.\n')
    
   	licensetextarea.set_editable(False)
   	licensetextarea.set_cursor_visible(False)
        vbox.pack_start(licensescroller,True,True,0)
	hbox=gtk.HBox()	
 	closebtn = gtk.Button(stock=gtk.STOCK_CLOSE)
        closebtn.connect("clicked", lambda w: window.destroy())
	closebtn.set_border_width(10)
	closebtn.set_size_request(80, 50);
        hbox.pack_end(closebtn,False,True,0)
        vbox.pack_start(hbox,False,True,15)
        window.add(vbox)
	window.show_all()

    def _menuitem_About(self,widget): # About window
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(250, 350)
        window.set_title("About Geye")
	window.set_icon_from_file("img/iris.png")
	window.set_position(gtk.WIN_POS_CENTER)

	vbox=gtk.VBox()	
	pixbufanim=gtk.gdk.pixbuf_new_from_file("img/iris.png")
	pixbufanim=gtk.gdk.Pixbuf.scale_simple(pixbufanim,115,109,gtk.gdk.INTERP_BILINEAR);
        image=gtk.Image()
        image.set_from_pixbuf(pixbufanim)
        image.show()
        vbox.pack_start(image,True,True,0)
	separator = gtk.SeparatorMenuItem()
        vbox.pack_start(separator,False,True,0)
	label0 = gtk.Label()
	label0.set_markup("<b>Geye v0.1 beta</b>\n")
        vbox.pack_start(label0, False, True, 0)
	label0.show()
	label1 = gtk.Label()
	label1.set_markup("Autor: Marc Moreno\n e-mail: moluxs@gmail.com")
        vbox.pack_start(label1, False, True, 0)
	label1.show();
	hbox=gtk.HBox()	
 	licensebtn = gtk.Button("License")
        licensebtn.connect("clicked", self._license_win)
	licensebtn.set_border_width(10)
	licensebtn.set_size_request(80, 50);
        hbox.pack_start(licensebtn,False,True,0)
 	closebtn = gtk.Button(stock=gtk.STOCK_CLOSE)
        closebtn.connect("clicked", lambda w: window.destroy())
	closebtn.set_border_width(10)
	closebtn.set_size_request(80, 50);
        hbox.pack_end(closebtn,False,True,0)
        vbox.pack_start(hbox,False,True,15)
        window.add(vbox)
	window.show_all()

    def populate_menu(self): #popup menu. It will be shown when you press the right button
        mnuitem = gtk.ImageMenuItem("List Events")
	mnuitem.connect("activate", self._menuitem_List)
        self.menu.append(mnuitem)

        mnuitem = gtk.ImageMenuItem("Insert Event")
	mnuitem.connect("activate", self._menuitem_Insert)
        self.menu.append(mnuitem)

	separator = gtk.SeparatorMenuItem()
        self.menu.append(separator)   
	
	mnuitem = gtk.ImageMenuItem("Configure")
	mnuitem.connect("activate", self._menuitem_Configure)
        self.menu.append(mnuitem)   

        mnuitem = gtk.ImageMenuItem("Logout")
	mnuitem.connect("activate", self._menuitem_Logout)
        self.menu.append(mnuitem)
 
        mnuitem = gtk.ImageMenuItem("Exit")
	mnuitem.connect("activate", self._halt_app)
        self.menu.append(mnuitem)

	separator = gtk.SeparatorMenuItem()
        self.menu.append(separator)          

        mnuitem = gtk.ImageMenuItem("About Geye")
	mnuitem.connect("activate", self._menuitem_About)
        self.menu.append(mnuitem)

    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)
        pass

    def werrorm(self,mss):
	 self.errorm = gtk.MessageDialog(parent = self.window, buttons = gtk.BUTTONS_OK, flags = gtk.DIALOG_MODAL, type = gtk.MESSAGE_ERROR, message_format = mss)
         self.errorm.set_title("Geye Error")
         result = self.errorm.run()
         self.errorm.destroy()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    Geye()
    main()
