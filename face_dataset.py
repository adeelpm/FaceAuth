
import cv2
import os
from face_training import train
import PySimpleGUI as sg


def register(id):
    sg.theme("LightGreen")


    layout = [
        [sg.Text("Register", size=(70, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],
       [ sg.Text("Capturing Facedata", size=(70, 1), justification="center",key='-TEXT-')]
        ]
    window = sg.Window("Register", layout, location=(500,200))







    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    face_detector = cv2.CascadeClassifier('c:/Users/Abdur Rahman Adeel/Desktop/FaceAuth/haarcascade_frontalface_default.xml')

        

    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    count = 0

    while(True):

        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break  
        

        ret, img = cam.read()
        # img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            print(count)

            cv2.imwrite("c:/Users/Abdur Rahman Adeel/Desktop/FaceAuth/dataset/User." + str(id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            imgbytes = cv2.imencode(".png", img)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes)

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 60: # Take 30 face sample and stop video
            break
        elif count == 57: # Take 30 face sample and stop video
            window['-TEXT-'].update('Capture Successful')
        



  
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

    train()
    window.close()

    