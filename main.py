# Libraries
from tkinter import *
from cefpython3 import cefpython as cef
import sys
import os
import platform
import logging as log
import threading

# Variables

# Presets
main = Tk()
logger = log.getLogger("main.py")
web = "https://www.google.com/"
showurl = StringVar(main,value=web)

# Log
logger.setLevel(log.DEBUG)
stream_handler = log.StreamHandler()
formatter = log.Formatter("[%(asctime)s] %(filename)s: %(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.info("Starting")

# Browser Settings
settings = {
    # "debug": True,
    # "log_severity": cef.LOGSEVERITY_INFO,
    "log_file": "debug.log",
    "product_version":"Browsle/1.0"
}
# cef.Initialize(settings=settings)
###############################

## Window #####################
logger.info("Setting window")

main.geometry("857x480")
main.minsize(200,100)
main.title("Home - Browsle")
main.iconbitmap("resources/favicon.ico")

logger.info("Window set")
###############################

## Configs ####################
# url bar
Grid.columnconfigure(main,2,weight=1)
Grid.rowconfigure(main,0,weight=1)
Grid.rowconfigure(main,1,weight=4)

# browser
# Grid.columnconfigure(main,0)
###############################

## Commands ###################
# Load custom website
def loadWeb():
    web = urlbar.get()
    logger.info("Loading "+web)
    showurl.set(web)
    urlbar.config(textvariable=showurl)
    
# Dynamic embed browser size
def setBrowserSize(*args):
    browser.config(height=main.winfo_height(),width=main.winfo_width(),)
###############################

## Web ########################
def WebPage(frame,url):
    logger.info("Starting browser")
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id())
    cef.Initialize(settings=settings)
    cef.CreateBrowserSync(window_info, url=url)
    cef.MessageLoop()
    logger.info("Browser showed")
###############################

## Widgets ####################
# Set widgets
back = Button(main,text="<")
forw = Button(main,text=">")
urlbar = Entry(main,textvariable=showurl,font=("Consolas"))
load = Button(main,text="(Re)Load",command=loadWeb)
browser = Frame(main,bg="blue")
logger.info("Widget set")

# Show widgets
back.grid(row=0,column=0,sticky="NW")
forw.grid(row=0,column=1,sticky="NW")
urlbar.grid(row=0,column=2,sticky="NEW")
load.grid(row=0,column=3,sticky="NE")
browser.grid(row=1,column=0,columnspan=4)
logger.info("Widget showed")

# Start browser
thread = threading.Thread(target=lambda:WebPage(browser,web))
thread.start()
# WebPage(browser,"https://www.google.com/")
logger.info("Thread started")
###############################

## Detections #################
main.bind("<Configure>", setBrowserSize)
###############################

## foot #######################
logger.info("Mainloop started")
main.mainloop()
logger.info("Mainloop stopped")
cef.Shutdown()

logger.info("Program stopped")
###############################