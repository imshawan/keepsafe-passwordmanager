''' This module handles all the user related configurations and settings for KeepSafe - Password Manager
    Author: Shawan Mandal
    
    MIT License, see LICENSE for more details.
    Copyright (c) 2021 Shawan Mandal
'''


from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import tkinter as tk
import base64, json
import icons_base64 as icon
import encryption as crypt
from datetime import datetime


'''width = 800
height = 700
windows = tk.Tk()
windows.wm_title("KeepSafe - About")
screen_width = windows.winfo_screenwidth()
screen_height = windows.winfo_screenheight()

x = int((screen_width/2) - (width/2))
y = int((screen_height/2) - (height/2))

windows.geometry("{}x{}+{}+{}".format(width, height, x, y))
windows.resizable(False, False)'''

def timestamp():
    '''Returns current timestamp'''
    t = datetime.now()
    return t.strftime('%H:%M:%S')

def getICO(icon):
    base64_img_bytes = icon.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    ico = PhotoImage(data=decoded_image_data)
    return ico

def getUsername(master_password):
    with open('config.json', 'rb') as config_file:
            data_bytes = config_file.read()
        
    try:
        config_data = crypt.decryptData(data_bytes, master_password)
    except RuntimeError as err:
        return 'error'

    json_res = json.loads(config_data.decode('utf-8'))
    return json_res

def manageEnc(master_password, usr, pas, operation):
    '''This function takes the parameters "Master Password", "Username and password" for new registration and "Operation" for the type of operation
    (either register or login) and performs the required work.'''
    if operation == 'register':
        time = timestamp()
        data = {}
        data['login_credentials'] = {
            'username': f'{usr}',
            'password': f'{pas}',
            'time': f'{time}'
        }
        data_bytes = json.dumps(data).encode('utf-8')
        try:
            config_data = crypt.encryptData(data_bytes, master_password)
        except RuntimeError as err:
            print(err)
            return

        with open('config.json', 'wb') as config_file:
            config_file.write(config_data)

    elif operation == 'change':
        with open('config.json', 'rb') as config_file:
            data_bytes = config_file.read()
        
        try:
            config_data = crypt.decryptData(data_bytes, master_password)
        except RuntimeError as err:
            print(err)
            return

        json_res = json.loads(config_data.decode('utf-8'))
        print(json_res)


def config(windows, configured, userAuthentication):
    if userAuthentication:
        pass
    else:
        messagebox.showerror("Error!", "Authenticate yourself first!")
        return

    width = 450
    height = 420
    win = tk.Toplevel()
    
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()

    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)



    background = getICO(icon.CONFIG_1)
    background_2 = getICO(icon.CONFIG_2)


    savebtnico = getICO(icon.CONF_SAVE)
    savebtnico = savebtnico.subsample(2,2)

    closebtnico = getICO(icon.CONF_CLOSE)
    closebtnico = closebtnico.subsample(2,2)

    if configured:
        win.wm_title("KeepSafe - Change Passwords")
        mainLbl = Label(win, image=background_2, highlightthickness=0, borderwidth=0)
        mainLbl.img = background_2
        mainLbl.place(x=0,y=0)

        userEntry = Entry(win, font=(None, 10), width=35, highlightthickness=1, highlightbackground='white', bg='#3f6975', fg='white')
        userEntry.insert(INSERT, 'Current password')
        userEntry.place(x=100,y=202)

        passEntry = Entry(win, font=(None, 10), width=35, highlightthickness=1, highlightbackground='white', bg='#3f6975', fg='white')
        passEntry.insert(INSERT, 'New password')
        passEntry.place(x=100,y=265)
    else:
        win.wm_title("KeepSafe - Set-up new account")
        mainLbl = Label(win, image=background, highlightthickness=0, borderwidth=0)
        mainLbl.img = background
        mainLbl.place(x=0,y=0)

        userEntry = Entry(win, font=(None, 10), width=35, highlightthickness=1, highlightbackground='white', bg='#3f6975', fg='white')
        userEntry.insert(INSERT, 'Enter a username')
        userEntry.place(x=100,y=202)

        passEntry = Entry(win, font=(None, 10), width=35, highlightthickness=1, highlightbackground='white', bg='#3f6975', fg='white')
        passEntry.insert(INSERT, 'Create password')
        passEntry.place(x=100,y=265)

    savebtn = Button(win, image=savebtnico, bd=0, bg='#3f6975', activebackground='#00ce00')
    savebtn.img = savebtnico
    closebtn = Button(win, image=closebtnico, bd=0, bg='#3f6975', activebackground='#ff0000', command=win.destroy) 
    closebtn.img = closebtnico
    savebtn.place(x=118,y=310)
    closebtn.place(x=240,y=310)
    win.focus_set()




