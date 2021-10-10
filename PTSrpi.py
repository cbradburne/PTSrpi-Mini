#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import END
from tkinter.messagebox import askyesno
from tkinter import font as tkFont
from tkinter.scrolledtext import ScrolledText
from serial import *
import time
import serial.tools.list_ports
import pygame

ser = ''
backgroundColour = '#21282D'
buttonColour = '#757981'
borderColorOff = '#212121'
borderColorSet = '#FF0000'
borderColorAt = '#00FF00'
borderColorRun = '#FFBF00'
colour_cam = '#047101'

running = True
ser = ''
serialPortSelect = ''
joystick = ''
joystickName = ''
button0Pressed = False
button1Pressed = False
button2Pressed = False
button3Pressed = False
button4Pressed = False
button5Pressed = False
button6Pressed = False
button7Pressed = False
button8Pressed = False
button9Pressed = False
button10Pressed = False
button11Pressed = False
button12Pressed = False
button13Pressed = False
button14Pressed = False
button15Pressed = False
button16Pressed = False

arr = []
oldAxisX = 0
oldAxisY = 0
oldAxisZ = 0
axisX = 0
axisY = 0
axisZ = 0
data = bytearray(7)
hat = ()
oldHatX = 0
oldHatY = 0
previousTime = time.time()

joyCircleX = 31
joyCircleY = 31
sliderCircleX = 31

panKeyPressed = False
tiltKeyPressed = False
sliderKeyPressed = False

pageToggle = False
page2Toggle = False
isFullscreen = True

moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveSliderLeft = False
moveSliderRight = False

def findJoystick():
    global joystick
    global joystickName

    if pygame.joystick.get_count() < 1:                                #no joysticks found
        textBoxJoystick.configure(state='normal')
        textBoxJoystick.delete(0.0,END)
        textBoxJoystick.insert(END, 'No joystick found', "center")
        textBoxJoystick.see(END)
        textBoxJoystick.configure(state='disabled')
        return
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        joystickName = pygame.joystick.Joystick(0).get_name()
        textBoxJoystick.configure(state='normal')
        textBoxJoystick.delete(0.0,END)
        textBoxJoystick.insert(END, joystickName, "center")
        textBoxJoystick.see(END)
        textBoxJoystick.configure(state='disabled')

def sendSerial(sendValue):
    if (ser == ''):
        serialReadTextBox.configure(state='normal')
        serialReadTextBox.insert(END, 'Serial port not selected!\n')
        serialReadTextBox.see(END)
        serialReadTextBox.configure(state='disabled')
    else:
        ser.write(sendValue.encode())

def serial_ports():
    global ser
    global serialPortSelect

    serialPortSelect = ' - '
    usb_port = 'ttyUSB0'
    rfcomm_port = 'rfcomm'
    wchusb_port = 'wchusbserial'
    ports = serial.tools.list_ports.comports()
    available_ports = []

    for p in ports:
        available_ports.append(p.device)

    cb['values'] = available_ports
    cb.config(foreground="white")

    if serialPortSelect == ' - ':
        if (wchusb_port in '\t'.join(available_ports)):
            try:
                serialPortSelect = [string for string in available_ports if wchusb_port in string]
                index = available_ports.index(serialPortSelect[0])
                cb.current(index)
                ser = Serial(serialPortSelect[0], 57600, timeout=0, writeTimeout=0)
                readSerial()
                cb.place(anchor='nw', height='30', width='240', x='50', y='3')
            except:
                serialPortSelect = [' - ']
        elif (usb_port in '\t'.join(available_ports)):
            try:
                serialPortSelect = [string for string in available_ports if usb_port in string]
                index = available_ports.index(serialPortSelect[0])
                cb.current(index)
                ser = Serial(serialPortSelect[0], 57600, timeout=0, writeTimeout=0)
                readSerial()
                cb.place(anchor='nw', height='30', width='240', x='50', y='3')
            except:
                serialPortSelect = [' - ']
        elif (rfcomm_port in '\t'.join(available_ports)):
            try:
                serialPortSelect = [string for string in available_ports if rfcomm_port in string]
                index = available_ports.index(serialPortSelect[0])
                cb.current(index)
                ser = Serial(serialPortSelect[0], 57600, timeout=0, writeTimeout=0)
                readSerial()
                cb.place(anchor='nw', height='30', width='240', x='50', y='3')
            except:
                serialPortSelect = [' - ']

def updateComPortlist():
    list = serial_ports()
    cb['values'] = list

def on_select(event):
    global ser
    global serialPortSelect

    serialPortSelect = cb.get()
    baudRate = 57600
    ser = Serial(serialPortSelect , baudRate, timeout=0, writeTimeout=0) #ensure non-blocking
    readSerial()

def sendAddPos(event):
    temp='#'
    sendSerial(temp)

def sendEditPos(event):
    temp='E'
    sendSerial(temp)

def sendGOFirst(event):
    temp='['
    sendSerial(temp)

def sendGOBack(event):
    temp='<'
    sendSerial(temp)

def sendGOFwd(event):
    temp='>'
    sendSerial(temp)

def sendGOLast(event):
    temp=']'
    sendSerial(temp)

def sendExecMoves(event):
    temp=';1'
    sendSerial(temp)

def sendOrbitPoint(event):
    temp='@1'
    sendSerial(temp)

def sendTimelapse(event):
    temp='l'
    sendSerial(temp)

def sendPanoramicLapse(event):
    temp='L'
    sendSerial(temp)

def sendReport(event):
    temp='R'
    sendSerial(temp)

def clearText(event):
    serialReadTextBox.configure(state='normal')
    serialReadTextBox.delete(0.0,END)
    serialReadTextBox.configure(state='disabled')

def refreshPorts(event):
    findJoystick()
    serial_ports()

def confirmClearArray(event):
    answer = askyesno(title='confirmation', message='Are you sure you want to clear the array?')
    if answer:
        sendClearArray()

def sendClearArray():
    temp='C'
    sendSerial(temp)

def doPageToggle(event):
    global pageToggle
    global page2Toggle

    page2Toggle = False
    pageToggle = not pageToggle
    if pageToggle:
        frame_4.lower()
        frame_3.lift()
        frame_2.lower()

        serialReadTextBox.place_forget()
        serialReadTextBox.place(anchor='nw', x='0', y='0', height='430', width='740')

    elif not pageToggle:
        frame_4.lower()
        frame_2.lift()

        serialReadTextBox.place_forget()
        serialReadTextBox.place(anchor='nw', x='0', y='0', height='40', width='740')
        
def doPage2Toggle(event):
    global pageToggle
    global page2Toggle

    pageToggle = False
    page2Toggle = not page2Toggle
    if page2Toggle:
        frame_4.lift()
        frame_2.lower()

        serialReadTextBox.place_forget()
        serialReadTextBox.place(anchor='nw', x='0', y='0', height='40', width='740')

    elif not page2Toggle:
        frame_4.lower()
        frame_2.lift()
        
        serialReadTextBox.place_forget()
        serialReadTextBox.place(anchor='nw', x='0', y='0', height='40', width='740')

def textEnd():
    serialReadTextBox.see('end')

def goFull(event):
    global isFullscreen

    isFullscreen = not isFullscreen
    if isFullscreen:
        mainWindow.attributes("-fullscreen", True)
    elif not isFullscreen:
        mainWindow.attributes("-fullscreen", False)

def doQuit(event):
    mainWindow.destroy()

def setMoveUp(event):
    global axisY
    global tiltKeyPressed
    global moveUp
    global moveDown

    tiltKeyPressed = True
    moveUp = True
    moveDown = False
    axisY = -255

def setMoveDown(event):
    global axisY
    global tiltKeyPressed
    global moveUp
    global moveDown

    tiltKeyPressed = True
    moveUp = False
    moveDown = True
    axisY = 255

def setMoveTiltStop():
    global axisY
    global tiltKeyPressed
    global moveUp
    global moveDown

    tiltKeyPressed = False
    moveUp = False
    moveDown = False
    axisY = 0

def setMoveLeft(event):
    global axisX
    global panKeyPressed
    global moveLeft
    global moveRight

    panKeyPressed = True
    moveLeft = True
    moveRight = False
    axisX = -255

def setMoveRight(event):
    global axisX
    global panKeyPressed
    global moveLeft
    global moveRight

    panKeyPressed = True
    moveLeft = False
    moveRight = True
    axisX = 255

def setMovePanStop():
    global axisX
    global panKeyPressed
    global moveLeft
    global moveRight

    panKeyPressed = False
    moveLeft = False
    moveRight = False
    axisX = 0

def setMoveSliderLeft(event):
    global axisZ
    global sliderKeyPressed
    global moveSliderLeft
    global moveSliderRight

    sliderKeyPressed = True
    moveSliderLeft = True
    moveSliderRight = False
    axisZ = -255

def setMoveSliderRight(event):
    global axisZ
    global sliderKeyPressed
    global moveSliderLeft
    global moveSliderRight

    sliderKeyPressed = True
    moveSliderLeft = False
    moveSliderRight = True
    axisZ = 255

def setMoveSliderStop():
    global axisZ
    global sliderKeyPressed
    global moveSliderLeft
    global moveSliderRight

    sliderKeyPressed = False
    moveSliderLeft = False
    moveSliderRight = False
    axisZ = 255
    axisZ = 0

def btcomm(event):
    os.popen('sh ./btcomm.sh')
    
def circle(canvas,x,y, r):
    id = canvas.create_oval(x-r,y-r,x+r,y+r, fill="red")
    return id

def scale(val, src, dst):
    # Scale the given value from the scale of src to the scale of dst.
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def tohex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))

mainWindow = tk.Tk()
mainWindow.title('Pan / Tilt Controller')
mainWindow.configure(width='800', height='480')
mainWindow.attributes("-fullscreen", True)

style= ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground=backgroundColour, selectbackground=backgroundColour, highlightthickness=0)

helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
helv30 = tkFont.Font(family='Helvetica', size=30)
helv18 = tkFont.Font(family='Helvetica', size=18)

frame_1 = tk.Frame(mainWindow, bg=backgroundColour, width='800', height='480')
frame_1.place(anchor='nw', x='0', y='0')
frame_1.lift()

frame_3 = tk.Frame(mainWindow, bg=backgroundColour, width='745', height='435')
frame_3.place(anchor='nw', x='30', y='40')

frame_2 = tk.Frame(mainWindow, bg=backgroundColour, width='745', height='405')
frame_2.place(anchor='nw', x='30', y='70')
frame_2.lift()

frame_4 = tk.Frame(mainWindow, bg=backgroundColour, width='745', height='405')
frame_4.place(anchor='nw', x='30', y='70')
frame_4.lower()

canvas = tk.Canvas(frame_2, bg=backgroundColour, highlightbackground='#7D0000', highlightthickness=2, width='60', height='60')
canvas.place(anchor='nw', x='338', y='120')

canvas2 = tk.Canvas(frame_2, bg=backgroundColour, highlightbackground='#7D0000', highlightthickness=2, width='60', height='20')
canvas2.place(anchor='nw', x='338', y='200')

cb = ttk.Combobox(frame_1, postcommand=updateComPortlist)
cb.place(anchor='nw', height='30', width='240', x='50', y='3')

midBox = tk.Text(frame_1, bg=backgroundColour, fg='White', bd=0, highlightthickness=0)
midBox.configure(state='disabled')
midBox.place(anchor='nw', x='28', y='38', height='435', width='745')
midBox.lower()

serialReadTextBox = ScrolledText(frame_3, bg=backgroundColour, fg='White', highlightthickness=1)
serialReadTextBox.configure(state='disabled')
serialReadTextBox.place(anchor='nw', x='0', y='0', height='40', width='740')

textBoxJoystick = tk.Text(frame_1, bg=backgroundColour, fg='White', font=("Helvetica", 12))
textBoxJoystick.place(anchor='nw', x='300', y='3', height='30', width='450')
textBoxJoystick.configure(state='disabled')
textBoxJoystick.tag_configure("center", justify='center')

buttonGoFirst = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='<<', font=helv36)
buttonGoFirst.place(anchor='nw', height='140', width='140', x='0', y='255')
buttonGoFirst.bind('<Button-1>', sendGOFirst)
buttonGoBack = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='<', font=helv36)
buttonGoBack.place(anchor='nw', height='140', width='140', x='200', y='255')
buttonGoBack.bind('<Button-1>', sendGOBack)
buttonGoFwd = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='>', font=helv36)
buttonGoFwd.place(anchor='nw', height='140', width='140', x='400', y='255')
buttonGoFwd.bind('<Button-1>', sendGOFwd)
buttonGoLast = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='>>', font=helv36)
buttonGoLast.place(anchor='nw', height='140', width='140', x='600', y='255')
buttonGoLast.bind('<Button-1>', sendGOLast)

buttonAddToArray = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Add\nPos', font=helv30)
buttonAddToArray.place(anchor='nw', height='140', width='140', x='120', y='103')
buttonAddToArray.bind('<Button-1>', sendAddPos)
buttonEditArray = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Edit\nPos', font=helv30)
buttonEditArray.place(anchor='nw', height='140', width='140', x='480', y='103')
buttonEditArray.bind('<Button-1>', sendEditPos)

buttonClearArray = tk.Button(frame_2, bg='#AA0000', activebackground='#AA0000', activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Clear\nArray', font=helv18)
buttonClearArray.place(anchor='nw', height='80', width='100', x='0', y='10')
buttonClearArray.bind('<Button-1>', confirmClearArray)
buttonOrbitPoint = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Orbit\nPoint', font=helv18)
buttonOrbitPoint.place(anchor='nw', height='80', width='100', x='160', y='10')
buttonOrbitPoint.bind('<Button-1>', sendOrbitPoint)
buttonTimelapse = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Time\nlapse', font=helv18)
buttonTimelapse.place(anchor='nw', height='80', width='100', x='320', y='10')
buttonTimelapse.bind('<Button-1>', sendTimelapse)
buttonPanoramiclapse = tk.Button(frame_2, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Pano\nlapse', font=helv18)
buttonPanoramiclapse.place(anchor='nw', height='80', width='100', x='480', y='10')
buttonPanoramiclapse.bind('<Button-1>', sendPanoramicLapse)
buttonExecMoves = tk.Button(frame_2, bg='#00AA00', activebackground='#00AA00', activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Execute\nMoves', font=helv18)
buttonExecMoves.place(anchor='nw', height='80', width='100', x='640', y='10')
buttonExecMoves.bind('<Button-1>', sendExecMoves)

buttonReport = tk.Button(frame_3, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Report', font=helv18)
buttonReport.place(anchor='nw', height='28', width='80', x='640', y='34')
buttonReport.bind('<Button-1>', sendReport)
buttonClearText = tk.Button(frame_3, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Clear', font=helv18)
buttonClearText.place(anchor='nw', height='28', width='80', x='550', y='34')
buttonClearText.bind('<Button-1>', clearText)
buttonBTcomm = tk.Button(frame_3, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='Connect', font=helv18)
buttonBTcomm.place(anchor='nw', height='28', width='100', x='440', y='34')
buttonBTcomm.bind('<Button-1>', btcomm)

buttonPage = tk.Button(frame_1, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='', font=helv18, command=textEnd)
buttonPage.place(anchor='nw', height='140', width='26', x='3', y='170')
buttonPage.bind('<Button-1>', doPageToggle)
buttonPage2 = tk.Button(frame_1, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='', font=helv18, command=textEnd)
buttonPage2.place(anchor='nw', height='140', width='26', x='770', y='170')
buttonPage2.bind('<Button-1>', doPage2Toggle)

buttonFS = tk.Button(frame_1, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='FS', font=helv18)
buttonFS.place(anchor='nw', height='30', width='30', x='0', y='0')
buttonFS.bind('<Button-1>', goFull)
buttonQuit = tk.Button(frame_1, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='X', font=helv18)
buttonQuit.place(anchor='nw', height='30', width='30', x='770', y='0')
buttonQuit.bind('<Button-1>', doQuit)

buttonUp = tk.Button(frame_4, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='^', font=helv18, command=setMoveTiltStop)
buttonUp.place(anchor='nw', height='100', width='100', x='160', y='20')
buttonUp.bind('<Button-1>', setMoveUp)
buttonDown = tk.Button(frame_4, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='v', font=helv18, command=setMoveTiltStop)
buttonDown.place(anchor='nw', height='100', width='100', x='160', y='260')
buttonDown.bind('<Button-1>', setMoveDown)
buttonLeft = tk.Button(frame_4, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='<', font=helv18, command=setMovePanStop)
buttonLeft.place(anchor='nw', height='100', width='100', x='40', y='140')
buttonLeft.bind('<Button-1>', setMoveLeft)
buttonRight = tk.Button(frame_4, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='>', font=helv18, command=setMovePanStop)
buttonRight.place(anchor='nw', height='100', width='100', x='280', y='140')
buttonRight.bind('<Button-1>', setMoveRight)

buttonSliderLeft = tk.Button(frame_4, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='<', font=helv18, command=setMoveSliderStop)
buttonSliderLeft.place(anchor='nw', height='100', width='100', x='400', y='280')
buttonSliderLeft.bind('<Button-1>', setMoveSliderLeft)
buttonSliderRight = tk.Button(frame_4, bg=buttonColour, activebackground=buttonColour, activeforeground="white", highlightbackground=borderColorOff, fg="white", text='>', font=helv18, command=setMoveSliderStop)
buttonSliderRight.place(anchor='nw', height='100', width='100', x='640', y='280')
buttonSliderRight.bind('<Button-1>', setMoveSliderRight)

circle(canvas,31,31,5)
circle(canvas2,31,11,5)

def readSerial():
    global ser

    if (ser == ''):
        return
    else:
        if ser.in_waiting > 0:
            c = ser.readline()           # Read data out of the buffer until a carraige return / new line is found

            if len(c) > 0:
                if c == b'\r\n':
                    c = ''
                    return

            if (c[0] == 4):
                c = ''
                return

            c = c.decode("utf8", "ignore")
            c = c.replace('\r', '')
            
            if c[0] == "":
                c = ''
                return
            else:                                    # add to the buffer
                serialReadTextBox.configure(state='normal')
                serialReadTextBox.insert(END, c)
                serialReadTextBox.see(END)
                serialReadTextBox.configure(state='disabled')
            c = ''

def sendJoystick(arr):
    global ser
    global data
    
    sliderInt = int(arr[1], 16)
    panInt = int(arr[2], 16)
    tiltInt = int(arr[3], 16)

    data[0] = 4
    
    if ((sliderInt > 0) and (sliderInt < 256)):
        data[1] = 0
        data[2] = sliderInt
    elif sliderInt > 257:
        data[1] = 255
        data[2] = (sliderInt-65281)
    else:
        data[1] = 0
        data[2] = 0

    if ((panInt > 0) and (panInt < 256)):
        data[3] = 0
        data[4] = panInt
    elif panInt > 257:
        data[3] = 255
        data[4] = (panInt-65281)
    else:
        data[3] = 0
        data[4] = 0

    if ((tiltInt > 0) and (tiltInt < 256)):
        data[5] = 0
        data[6] = tiltInt
    elif tiltInt > 257:
        data[5] = 255
        data[6] = (tiltInt-65281)
    else:
        data[5] = 0
        data[6] = 0
    
    if ser == '':
        pass
    else:
        ser.write(data)

def process_events():
    global running
    global arr
    global joystick
    global joystickName
    global button0Pressed
    global button1Pressed
    global button2Pressed
    global button3Pressed
    global button4Pressed
    global button5Pressed
    global button6Pressed
    global button7Pressed
    global button8Pressed
    global button9Pressed
    global button10Pressed
    global button11Pressed
    global button12Pressed
    global button13Pressed
    global button14Pressed
    global button15Pressed
    global button16Pressed
    global oldAxisX
    global oldAxisY
    global oldAxisZ
    global oldHatX
    global oldHatY
    global axisX
    global axisY
    global axisZ
    global previousTime
    global running
    global panKeyPressed
    global tiltKeyPressed
    global sliderKeyPressed
    global joyCircleX
    global joyCircleY
    global sliderCircleX

    joyPS4 = "Sony"
    joyPS4BT = "DUALSHOCK"
    joyPS4Win = "PS4"
    joyX360 = "360"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        deadRangeLow = -0.2
        deadRangeHigh = 0.2

        if joystick == '':
            pass
        else:
            if (joyPS4 in joystickName) or (joyPS4BT in joystickName) or (joyPS4Win in joystickName):
                #print ("PS4 Controller Found")\
                '''
                hat = joystick.get_hat(0)
                hatX = hat[0]
                hatY = hat[1]
                if (hatX != oldHatX):
                    oldHatX = hatX
                    if hatX == 1:                                                       #  RIGHT
                        sendReport()
                    if hatX == -1:                                                      #  LEFT
                        sendReport()

                if (hatY != oldHatY):
                    oldHatY = hatY
                    if hatY == 1:                                                       #  UP
                        sendReport()
                    if hatY == -1:                                                      #  DOWN
                        sendReport()
                '''

                if event.type == pygame.JOYBUTTONDOWN: 
                    if (joystick.get_button(0) and not button0Pressed):                 #  Square
                        button0Pressed = True
                        sendExecMoves(1)
                    elif (joystick.get_button(1) and not button1Pressed):               #  Cross
                        button1Pressed = True
                        sendAddPos(1)
                    elif (joystick.get_button(2) and not button2Pressed):               #  Circle
                        button2Pressed = True
                        sendEditPos(1)
                    elif (joystick.get_button(3) and not button3Pressed):               #  Triangle
                        button3Pressed = True
                        sendClearArray()
                '''
                    elif (joystick.get_button(4) and not button4Pressed):               #  L1
                        button4Pressed = True
                    elif (joystick.get_button(5) and not button5Pressed):               #  R1
                        button5Pressed = True
                    elif (joystick.get_button(6) and not button6Pressed):               #  L2
                        button6Pressed = True
                    elif (joystick.get_button(7) and not button7Pressed):               #  R2
                        button7Pressed = True
                    elif (joystick.get_button(8) and not button8Pressed):               #  Share
                        button8Pressed = True
                    elif (joystick.get_button(9) and not button9Pressed):               #  Option
                        button9Pressed = True
                    elif (joystick.get_button(10) and not button10Pressed):             #  L3
                        button10Pressed = True
                    elif (joystick.get_button(11) and not button11Pressed):             #  R3
                        button11Pressed = True
                '''

                if not panKeyPressed and not tiltKeyPressed:
                    joyXread = joystick.get_axis(0)
                    joyYread = joystick.get_axis(1)

                    if (joyXread < deadRangeLow):
                        axisX = int(scale(joyXread, (-1.0,deadRangeLow), (-255,0)))
                    elif (joyXread > deadRangeHigh):
                        axisX = int(scale(joyXread, (deadRangeHigh,1.0), (0,255)))
                    else:
                        axisX = 0

                    if (joyYread < deadRangeLow):
                        axisY = int(scale(joyYread, (-1.0,deadRangeLow), (-255,0)))
                    elif (joyYread > deadRangeHigh):
                        axisY = int(scale(joyYread, (deadRangeHigh,1.0), (0,255)))
                    else:
                        axisY = 0

                if not sliderKeyPressed:
                    joyZread = joystick.get_axis(3)

                    if (joyZread < deadRangeLow):
                        axisZ = int(scale(joyZread, (-1.0,deadRangeLow), (-255,0)))
                    elif (joyZread > deadRangeHigh):
                        axisZ = int(scale(joyZread, (deadRangeHigh,1.0), (0,255)))
                    else:
                        axisZ = 0
            if (joyX360 in joystickName):
                #print ("XBOX360 USB Controller Found")
                '''
                hat = joystick.get_hat(0)
                hatX = hat[0]
                hatY = hat[1]
                if (hatX != oldHatX):
                    oldHatX = hatX
                    if hatX == 1:                                                       #  RIGHT
                        sendReport()
                    if hatX == -1:                                                      #  LEFT
                        sendReport()

                if (hatY != oldHatY):
                    oldHatY = hatY
                    if hatY == 1:                                                       #  UP
                        sendReport()
                    if hatY == -1:                                                      #  DOWN
                        sendReport()
                '''
                if event.type == pygame.JOYBUTTONDOWN: 
                    if (joystick.get_button(0) and not button0Pressed):                 #  A
                        button0Pressed = True
                        sendAddPos(1)
                    elif (joystick.get_button(1) and not button1Pressed):               #  B
                        button1Pressed = True
                        sendEditPos(1)                
                    elif (joystick.get_button(2) and not button2Pressed):               #  X
                        button2Pressed = True
                        sendExecMoves(1)
                    elif (joystick.get_button(3) and not button3Pressed):               #  Y
                        button3Pressed = True
                        sendClearArray()
                '''
                    elif (joystick.get_button(4) and not button4Pressed):               #  L1
                        button4Pressed = True
                    elif (joystick.get_button(5) and not button5Pressed):               #  R1
                        button5Pressed = True
                    elif (joystick.get_button(6) and not button6Pressed):               #  Back
                        button6Pressed = True
                    elif (joystick.get_button(7) and not button7Pressed):               #  Start
                        button7Pressed = True
                    elif (joystick.get_button(8) and not button8Pressed):               #  Xbox
                        button8Pressed = True
                    elif (joystick.get_button(9) and not button9Pressed):               #  L3
                        button9Pressed = True
                    elif (joystick.get_button(10) and not button10Pressed):             #  R3
                        buttonL10Pressed = True
                '''

                if not panKeyPressed and not tiltKeyPressed:
                    joyXread = joystick.get_axis(0)
                    joyYread = joystick.get_axis(1)

                    if (joyXread < deadRangeLow):
                        axisX = int(scale(joyXread, (-1.0,deadRangeLow), (-255,0)))
                    elif (joyXread > deadRangeHigh):
                        axisX = int(scale(joyXread, (deadRangeHigh,1.0), (0,255)))
                    else:
                        axisX = 0

                    if (joyYread < deadRangeLow):
                        axisY = int(scale(joyYread, (-1.0,deadRangeLow), (-255,0)))
                    elif (joyYread > deadRangeHigh):
                        axisY = int(scale(joyYread, (deadRangeHigh,1.0), (0,255)))
                    else:
                        axisY = 0

                if not sliderKeyPressed:
                    joyZread = joystick.get_axis(3)

                    if (joyZread < deadRangeLow):
                        axisZ = int(scale(joyZread, (-1.0,deadRangeLow), (-255,0)))
                    elif (joyZread > deadRangeHigh):
                        axisZ = int(scale(joyZread, (deadRangeHigh,1.0), (0,255)))
                    else:
                        axisZ = 0
        
        if event.type == pygame.JOYBUTTONUP:
            if (button0Pressed and not joystick.get_button(0)):
                button0Pressed = False
            elif (button1Pressed and not joystick.get_button(1)):
                button1Pressed = False
            elif (button2Pressed and not joystick.get_button(2)):
                button2Pressed = False
            elif (button3Pressed and not joystick.get_button(3)):
                button3Pressed = False
            elif (button4Pressed and not joystick.get_button(4)):
                button4Pressed = False
            elif (button5Pressed and not joystick.get_button(5)):
                button5Pressed = False
            elif (button6Pressed and not joystick.get_button(6)):
                button6Pressed = False
            elif (button7Pressed and not joystick.get_button(7)):
                button7Pressed = False
            elif (button8Pressed and not joystick.get_button(8)):
                button8Pressed = False
            elif (button9Pressed and not joystick.get_button(9)):
                button9Pressed = False
            elif (button10Pressed and not joystick.get_button(10)):
                button10Pressed = False
            elif (button11Pressed and not joystick.get_button(11)):
                button11Pressed = False
            elif (button12Pressed and not joystick.get_button(12)):
                button12Pressed = False
            elif (button13Pressed and not joystick.get_button(13)):
                button13Pressed = False
            elif (button14Pressed and not joystick.get_button(14)):
                button14Pressed = False

        axisXDOT = scale(axisX, (-255,255), (-1.0,1.0))
        axisYDOT = scale(axisY, (-255,255), (-1.0,1.0))
        axisZDOT = scale(axisZ, (-255,255), (-1.0,1.0))

        joyCircleX = (axisXDOT*30)+31                                                  # Draw Dots
        joyCircleY = (axisYDOT*30)+31
        sliderCircleX = (axisZDOT*30)+31

pygame.init()

cb.bind('<<ComboboxSelected>>', on_select)

findJoystick()
serial_ports()

while running:
    process_events()

    if (((axisX != oldAxisX) or (axisY != oldAxisY) or (axisZ != oldAxisZ)) and ((time.time() - previousTime) > 0.1)):
        previousTime = time.time()
        oldAxisX = axisX
        oldAxisY = axisY
        oldAxisZ = axisZ
        axisXh = tohex(axisX, 16)
        axisYh = tohex(-axisY, 16)
        axisZh = tohex(axisZ, 16)

        canvas.delete('all')
        canvas2.delete('all')
        circle(canvas,joyCircleX,joyCircleY,5)
        circle(canvas2,sliderCircleX,11,5)

        arr = [4, axisZh, axisXh, axisYh]
        sendJoystick(arr)
        #print(4,' - ', axisZ, ' - ', axisX, ' - ', axisY)

    try:
        readSerial()
    except:
        ser=''
        serialReadTextBox.configure(state='normal')
        serialReadTextBox.insert(END, 'Serial port not selected!\n')
        serialReadTextBox.see(END)
        serialReadTextBox.configure(state='disabled')
        
    mainWindow.update()

mainWindow.quit
    