import cv2 as cv
from PIL import Image,ImageTk
import tkinter as tk
import numpy as np
import time
import datetime
#import RPi.GPIO as GPIO



#in1 = 24
#in2 = 23
#en = 25

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(24,GPIO.OUT)
#GPIO.setup(23,GPIO.OUT)
#GPIO.setup(25,GPIO.OUT)
#GPIO.output(24,False)
#GPIO.output(23,False)
#p = GPIO.PWM(25,1000)
#p.start(0)


def start(): 
#   p.start(0)
    print('start')   
#   GPIO.output(in1,True)
#   GPIO.output(in2,True)
#   p.ChangeDutyCycle(50)

def stop():
    print('stop')
    #p.stop()
    
   
    
def ex():
    cam.release()
    root.destroy()
    

wcam , hcam = 640,480
cam = cv.VideoCapture(1)
cam.set(3,wcam)
cam.set(4,wcam)


#def showframe():
#    global frame 
#    global imgtk

#    check, frame = cam.read()
#    cvimage = cv.cvtColor(frame,cv.COLOR_BGR2RGBA)
#    img = Image.fromarray(cvimage)
#    imgtk = ImageTk.PhotoImage(image = img)
    
#    lmain.imgtk  = imgtk
#    lmain.configure(image=imgtk)
#    lmain.after(10,showframe)

def contour():
    global frame
    global imgtk
    check,frame =cam.read()
    f = cv.cvtColor(frame.copy(),cv.COLOR_BGR2HSV)
    red_lower = np.array([0,87,111],np.uint8) #136,87,111
    red_upper = np.array([20,255,255],np.uint8) #180,255,255
    
    blue_lower = np.array([100,111,55],np.uint8)
    blue_upper = np.array([130,255,255],np.uint8)
    
    green_lower = np.array([25,111,55],np.uint8)
    green_upper = np.array([102,255,150],np.uint8)
    
    red = cv.inRange(f,red_lower,red_upper)
    green = cv.inRange(f,green_lower,green_upper)
    blue = cv.inRange(f,blue_lower,blue_upper)
    
    red_contours,hierarchy = cv.findContours(red,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    green_contours,hierarchy = cv.findContours(green,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    blue_contours,hierarchy = cv.findContours(blue,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    
    if len(red_contours) != 0:
        for rcontour in red_contours:
            if cv.contourArea(rcontour) > 300:
                x,y,w,h = cv.boundingRect(rcontour)
                frame = cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                cv.putText(frame,'RED',(x,y),cv.FONT_HERSHEY_COMPLEX,1,(0,0,255))
          
            
    if len(blue_contours) != 0 :
        for bcontour in blue_contours:
            if cv.contourArea(bcontour) > 500:
                x,y,w,h = cv.boundingRect(bcontour)
                frame = cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                cv.putText(frame,'BLUE',(x,y),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0))       
    
    
    if len(green_contours) != 0:
        for gcontour in green_contours:
            if cv.contourArea(gcontour) > 500:
                    x,y,w,h = cv.boundingRect(gcontour)
                    frame = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    cv.putText(frame,'GREEN',(x,y),cv.FONT_HERSHEY_COMPLEX,1,(0,255,0))  

    
     
    cvimage = cv.cvtColor(frame,cv.COLOR_BGR2RGBA)
    img = Image.fromarray(cvimage)
    imgtk = ImageTk.PhotoImage(image = img)
    
    lmain.imgtk  = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10,contour)
    


root = tk.Tk()
root.title('Color Detection')
root.config(bg='black')

imageFrame = tk.Frame(root,width=600,height=700)
imageFrame.grid(row=0,column=0,columnspan=2,padx=10,pady=2)

lmain = tk.Label(imageFrame)
lmain .grid(row=0,column=0)

startbutton = tk.Button(text='Start',fg='green',command=start)
startbutton.grid(row=2,column=0,sticky='NSEW')

stopbutton = tk.Button(text='Stop',fg='yellow',command=stop)
stopbutton.grid(row=4,column=0,sticky='NSEW')

exitbutton = tk.Button(text='Exit',fg='red',command=ex)
exitbutton.grid(row=6,column=0,sticky='NSEW')

contour()
root.mainloop()