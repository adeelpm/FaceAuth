import PySimpleGUI as sg
from input import input
from face_recognition import login

sg.theme("LightGreen")
layout = [
    [sg.Text("Auth++", size=(60, 1),justification='center')],
    [sg.Text("", size=(10, 1)),sg.Button("Register", size=(10, 2)),sg.Button("Register Eye Gesture", size=(10, 2)),sg.Button("Login", size=(10, 2)) ],
]

window = sg.Window("Auth++", layout,location=(500, 300))


while True:
    event, values = window.read(timeout=20)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break  
    elif event == "Register":
        input()
    elif event == "Register Eye Gesture":
        login(2)
    elif event == "Login":
        login(1)