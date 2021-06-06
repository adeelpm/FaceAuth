import PySimpleGUI as sg
from face_dataset import register
from collections import OrderedDict


def input():
    layout = [
        [sg.Text("Enter UserID", size=(20, 1)), sg.InputText()],
        [sg.Text("Enter UserName", size=(20, 1)), sg.InputText()],
        [sg.Button("Enter", size=(20, 1)), ],
    ]

    window = sg.Window("Input", layout, location=(500, 300))


    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break  
        if event=="Enter":
            usernames=OrderedDict()
            try:
                f = open('trainer/file.txt', 'r+')
                read=f.read()
                usernames = eval(read)
                usernames[values[0]]=values[1]
                # print(usernames[1])
                f = open('trainer/file.txt', 'w+')
                f.write(str(usernames))
                f.close()
        
            except Exception as e:
                print(e)
                f = open('trainer/file.txt', 'w+')
                usernames[values[0]]=values[1]
                f.write(str(usernames))
                f.close()
        
            break
    window.close()
    register(values[0])        
            




    



    

# print(values[0],values[1]) 