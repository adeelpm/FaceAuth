
from PySimpleGUI.PySimpleGUI import Window
import cv2
import numpy as np
import os
import time
from numpy.lib.type_check import _getmaxmin 
from gaze_tracking import GazeTracking
import PySimpleGUI as sg
from collections import OrderedDict



starttime=0.0

def starttimes(text):
    global starttime
    starttime=0.0
    starttime=time.time()
    print(text)



def login(flag):
    sg.theme("LightGreen")

    # Define the window layout
    layout = [
        [sg.Text("Window Main", size=(80, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],

        [sg.Radio("None", "Radio", True, size=(10, 1))],
        
    
        [
            sg.Radio("blur", "Radio", size=(10, 1), key="-BLUR-"),
            sg.Slider(
                (1, 11),
                1,
                1,
                orientation="h",
                size=(40, 15),
                key="-BLUR SLIDER-",
            ),
        ],
        [
            sg.Radio("hue", "Radio", size=(10, 1), key="-HUE-"),
            sg.Slider(
                (0, 225),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-HUE SLIDER-",
            ),
        ],
        [
            sg.Radio("enhance", "Radio", size=(10, 1), key="-ENHANCE-"),
            sg.Slider(
                (1, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-ENHANCE SLIDER-",
            ),
        ],
        [sg.Button("Exit", size=(10, 1))],
    ]

    # Create the window and show it without the plot
    window = sg.Window("Auth++", layout, location=(400, 100))
    









    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('c:/Users/Abdur Rahman Adeel/Desktop/FaceAuth/trainer/trainer.yml')
    cascadePath = "c:/Users/Abdur Rahman Adeel/Desktop/FaceAuth/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX
    gaze = GazeTracking()

    #iniciate id counter
    id = 0


    usernames=OrderedDict()
    f = open('trainer/file.txt', 'r')
    read=f.read()
    usernames = eval(read)
    f.close()

    if flag==1:
        frr=OrderedDict()
        f1 = open('trainer/fileone.txt', 'r')
        read=f1.read()
        frr = eval(read)
        
        f1.close()

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # cam.set(3, 640) # set video widht
    # cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)





    text=""
    texttwo=""
    textthree=""

    vtop=vbottom=vleft=vright=0

    registerb=False
    loginb=False

    xy=0
    xz=0
    length=0
    blinkcount=0
    arr=[0] * 4
    counterl=0
    arrl=[0] * 4
    counter=0
    verifynum=0
    
    endtime=0
    totaltime=0
    
    tems=0.0
    tt=0
    id1=0

    if flag==2:
        registerb=True
        loginb=False
        blinkcount=0
        print("Started Monitoring for Registeration")
    if flag==1:     
        registerb=False
        loginb=True
        blinkcount=0
        print("Started Monitoring for login")
    while True:
        if counter>=4:
            break
        if counterl>=4:
            break

        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break  

        tems=time.time()-float(starttime)
      
        if tems<1.5 and tems>1.2:
            starttimes(text)
        ret, img =cam.read()
        gaze.refresh(img)
        img= gaze.annotated_frame()

     
        if values["-BLUR-"]:
            img = cv2.GaussianBlur(img, (21, 21), values["-BLUR SLIDER-"])
        elif values["-HUE-"]:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img[:, :, 0] += int(values["-HUE SLIDER-"])
            img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        elif values["-ENHANCE-"]:
            enh_val = values["-ENHANCE SLIDER-"] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)





        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        
        if gaze.is_left():
            text = "Looking left"
            if tems>0.5 and tems<1.0:
                if counter<4:
                    if registerb:
                        arr[counter]="left"
                        counter=counter+1
                        starttimes(text)
                if counterl<4:
                    if loginb==True:
                        arrl[counterl]="left"
                        counterl=counterl+1
                        starttimes(text)
                
        elif gaze.is_top():
            text = "top"
            if tems>0.5 and tems<1.0:
                if counter<4:
                    if registerb:
                        arr[counter]="top"
                        counter=counter+1
                        starttimes(text)
                if counterl<4:
                    if loginb==True:
                        arrl[counterl]="top"
                        counterl=counterl+1
                        starttimes(text)

    
        elif gaze.is_right():
            text = "Looking right"
            vright=vright+1
            if tems>0.5 and tems<1.0:
                if counter<4:
                    if registerb:
                        arr[counter]="right"
                        counter=counter+1
                        starttimes(text)
                if counterl<4:
                    if loginb==True:
                        arrl[counterl]="right"
                        counterl=counterl+1
                        starttimes(text)
        elif gaze.is_center():
            text = "Looking center"

        if gaze.is_blinking():
            texttwo = "Blinking"
            blinkcount=blinkcount+1
            starttimes(texttwo)
        elif gaze.is_blinking()==False:
            texttwo="Not blinking"

        


    
        
        

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            if (confidence < 100):
                
                id1=id
                id = usernames[str(id)]
                confidence = "  {0}%".format(round(100 - confidence))
            
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                text="Unidentified face"
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            




        cv2.putText(img, str(text), (10, 65), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0,0,0), 2)
        cv2.putText(img, str(texttwo), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0,0,0), 2)

        imgbytes = cv2.imencode(".png", img)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break



    

    if flag==1:
        if counterl==4:
            
            for countss,xx in enumerate(frr[id1]):
                print("frr : "+str(frr[id1][countss])+" arrl : "+str(arrl[countss]))
                if(frr[id1][countss]==arrl[countss]):
                    verifynum+=1

            
            if verifynum==counterl:
                sg.popup("Login Successful")
                print("welcome!!")
            else:
                print("Wrong secure code!!")


    print("\n Exiting Program and cleanup stuff")
    
 
    cam.release()

    if flag==2:
        gesturecode=OrderedDict()
        try:
            f = open('trainer/fileone.txt', 'r+')
            read=f.read()
            gesturecode = eval(read)
            gesturecode[id1]=arr
            # print(usernames[1])
            f = open('trainer/fileone.txt', 'w+')
            f.write(str(gesturecode))
            f.close()
            
        except Exception as e:
            print(e)
            f = open('trainer/fileone.txt', 'w+')
            gesturecode[id1]=arr
            f.write(str(gesturecode))
            f.close()

        print("Successfully Registered Gesture")

    window.close()

