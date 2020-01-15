#!/user/bin/env python3

#use "sudo ln -sf /usr/bin/python3.4 /usr/bin/python"
#changing the default python

#To run in console use "python3 PhotoBooth.py"

from subprocess import call  
from datetime import datetime 
import picamera
import time
from tkinter import *
from tkinter import ttk
import RPi.GPIO as GPIO
from PIL import Image, ImageTk
import urllib
import os



def my_callback(channel):
    global pressed
    pressed = True

#Summary: The method creates a window that previews the picture taken
#with the ability to input a caption.
def showPreview(): 
    #Using tkinter for creating windows.
    #root is created in the main program loop
    root.title("Add a caption")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    root.update_idletasks()

    #To prevent root window from appearing in random locations
    #Grabbing the width and height of the current screen and finding
    #rough middle of the screen location.
    w=mainframe.winfo_screenwidth()
    h=mainframe.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    root.geometry("%dx%d+%d+%d" % (800, 480, 0, 0))

    #Creating the frame inside the root window.
    mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    #Image is handled by PIL
    #Open taken from the main loop.
    img = Image.open(filePath)
    img.thumbnail((500,300), Image.ANTIALIAS)#Define the size of the preview image.
    newimg = ImageTk.PhotoImage(img)
    ttk.Label(mainframe, image = newimg).grid(column = 0, row = 1,sticky=W)

    #Input text box for adding a caption to the image.
    captionBox = ttk.Entry(mainframe, width=40, textvariable=caption)
    captionBox.grid(column=0, row=3, sticky=(W,E))

    #Create tweet button and text box.
    ttk.Label(mainframe, text="Add a caption for the tweet!").grid(column=0, row=2, sticky=W)
    ttk.Button(root, text="Tweet", command = tweet).grid(column=3, row=3, sticky=W)
    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    captionBox.focus()

    #Bind the enter key to allow same effect as clicking the button.
    root.bind('<Return>', tweet)
    root.bind('<Escape>', onEscape)
    root.protocol("WM_DELETE_WINDOW", onClose)

    root.mainloop()

#Method for proper cleanup.    
def onClose():
    root.destroy()
    GPIO.cleanup()
    global exit1
    exit1 = True

#Escape and reloop
def onEscape(*args):
    root.destroy()

#Check internet connection


#------
#Main
#------

#Bind the GPIO
GPIO.setmode(GPIO.BCM)
button1_pin = 23
led_pin = 21
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    
GPIO.setup(led_pin, GPIO.OUT)
exit1 = False
#Main loops to allow for continuous image taking.
while not exit1:
    GPIO.output(led_pin, 1)
    pressed = False
    fileName = 'pic2.jpg'
    filePath = "/home/pi/Desktop/PhotoBooth/" + fileName
    root = Tk()#Create root
    caption = StringVar()#Define caption text to use in the root window.
    #Start camera preview and wait for button press.
    with picamera.PiCamera() as camera:
        #camera.resoution = (2592, 1944)
        camera.start_preview()
        try:
            GPIO.wait_for_edge(button1_pin, GPIO.FALLING, bouncetime = 500)
        except KeyboardInterupt:
            onClose()
        camera.stop_preview();
        time.sleep(1)
        GPIO.output(led_pin, 0)
        camera.capture(fileName)
        os.system('echo "Learn how to make this at TechLab" | lpr')
        os.system("lpr -o fit-to-page /home/pi/Desktop/pic2.jpg")
        #showPreview()
    
