#coding:utf-8
# found on <http://files.majorsilence.com/rubbish/pygtk-book/pygtk-notebook-html/pygtk-notebook-latest.html#SECTION00430000000000000000>
# simple example of a tray icon application using PyGTK


import gtk,gobject
import urllib2,cookielib
import urllib
import socket
import time

global timer_id

def my_log(str):
    log_file = open("log.txt", 'a')
    log_file.write("[%s] " % time.strftime("%Y-%m-%d %X",time.localtime()) + str + "\n")
    log_file.close()
    
def auto_login():
    headers = {
        'Host':'202.103.24.68',
        'Origin':'http://202.103.24.68',
        'Referer':'http://202.103.24.68/login',
        'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
    }
    
    values = {
            'username':'',
            'password':'',
            'save_user':'1',
            'save_pass':'1',
            'url':'',
            'password_enc':'MDIxMTAwMTI5My5hc2Q=',
            'newpassword_enc':'',
            'retype_newpassword_enc':'',
            'login':'1',
            'login_type':'login',
            'uri':'aHR0cDovLzE5Mi4xNjguNjAuNjUv',
            'password_type':'normal',
            'password_orig':''
        }

    url = 'http://202.103.24.68/login'
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    
    data = urllib.urlencode(values)
    
    req = urllib2.Request(url, data, headers)
    login_response=urllib2.urlopen(req, timeout = 5)

def check_online(url):
    
    try:
        headers = {
            'Referer':url,
            'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'
        }

        req = urllib2.Request(url)    
        response = urllib2.urlopen(req)    
        the_page = response.read()
        if the_page.find("用户认证系统 登录界面") != -1:
            my_log("You are offline")
            return False
        else:
            my_log("You are still online!")
            return True

    except Exception,e:
        my_log("You are offline")
        my_log (e)
        return False

def keep_online():
        global timer_id
        if not check_online("http://www.baidu.com"):
            try:
                auto_login()
                my_log("Login success")
            except:
                my_log("Login error!")
                
        timer_id = gobject.timeout_add(1000 * 500, keep_online)

def message(data=None):
  "Function to display messages to the user."
  
  msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL,
    gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
  msg.run()
  msg.destroy()
 
def open_app(data = None):
  global timer_id
  if not timer_id:
      timer_id = gobject.timeout_add(1000 * 500, keep_online)
  my_log("Tast started!")

def stop_app(data = None):
  global timer_id
  gobject.source_remove(timer_id)
  timer_id = 0
  my_log("Tast stopped!")
  
def close_app(data = None):
  global timer_id
  if timer_id:
      gobject.source_remove(timer_id)
      timer_id = 0
      my_log("Tast stopped!")
      
  my_log("Tast exit!")
  gtk.main_quit()
 
def make_menu(event_button, event_time, data=None):
  menu = gtk.Menu()
  
  open_item = gtk.MenuItem("Start Monitor")
  stop_item = gtk.MenuItem("Stop Monitor")
  close_item = gtk.MenuItem("Exit")
  about_item = gtk.MenuItem("About")
  
  #Append the menu items
  menu.append(about_item)
  menu.append(open_item)
  menu.append(stop_item)
  menu.append(close_item)
  #add callbacks
  about_item.connect_object("activate", message, "这个小程序用来自动登录烽火通信公司的上网行为管理账户。\n保持PC持续在线。\n联系作者：moupeng.yang@gmail.com")
  open_item.connect_object("activate", open_app, "Start Monitor")
  stop_item.connect_object("activate", stop_app, "Stop Monitor")
  close_item.connect_object("activate", close_app, "Close Monitor")
  #Show the menu items
  about_item.show()
  open_item.show()
  stop_item.show()
  close_item.show()
  
  #Popup the menu
  menu.popup(None, None, None, event_button, event_time)
 
def on_right_click(data, event_button, event_time):
  make_menu(event_button, event_time)
 
def on_left_click(event):
  message("这个小程序用来自动登录烽火通信公司的上网行为管理账户。\n保持PC持续在线。\n联系作者：moupeng.yang@gmail.com")
 
if __name__ == '__main__':
  global timer_id
  timer_id = 0
  icon = gtk.status_icon_new_from_file("Color.ico")
  icon.connect('popup-menu', on_right_click)
  icon.connect('activate', on_left_click)
  gtk.main()
