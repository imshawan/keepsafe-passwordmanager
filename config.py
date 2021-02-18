''' 
    This module handles all the user related configurations and settings for KeepSafe - Password Manager
    Author: Shawan Mandal
    
    MIT License, see LICENSE for more details.
    Copyright (c) 2021 Shawan Mandal
'''


from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import tkinter as tk
import base64, json, os
import icons_base64 as icon
import encryption as crypt
from datetime import datetime
import handle_db as D_base

#CONFIG File
global configFile

cf = 'resources'
if not os.path.exists(cf):
    os.makedirs(cf)
fl = 'config.dat'
configFile = os.path.join(cf, fl)


def timestamp():
    '''Returns current date and timestamp'''
    t = datetime.now()
    return t.strftime('%d:%m:%Y'), t.strftime('%H:%M:%S')

def getICO(icon):
    base64_img_bytes = icon.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    ico = PhotoImage(data=decoded_image_data)
    return ico

def destroyWindows(win1, win2):
    win2.destroy()
    win1.destroy()
    
def handle_message(args, screen, mainwindow):
    width = 370
    height = 260
    win = tk.Toplevel()

    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()

    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)
    # MAIN ICON
    mainICO = getICO(icon.ICO_MAIN)
    win.iconphoto(False, mainICO)

    if args == 'success':
        vector = getICO(icon.ICO_TICK)
        vectorlbl = Button(win, image=vector, bd=0, command=lambda: destroyWindows(mainwindow, screen))
        vectorlbl.img = vector
        vectorlbl.place(x=110,y=10)
        txt1 = Label(win, text='TASK SUCCESSFUL', font=(None, 17, 'bold'), fg='green')
        txt1.place(x=70,y=170)
        subTxt = Label(win, text='Please restart the application and authenticate yourself \nwith new credentials to continue usage',font=(None, 10), justify=CENTER)
        subTxt.place(x=23,y=205)
    elif args == 'fail':
        vector = getICO(icon.ICO_CROSS)
        vectorlbl = Button(win, image=vector, bd=0, command=win.destroy)
        vectorlbl.img = vector
        vectorlbl.place(x=110,y=10)
        txt1 = Label(win, text='ACCESS DENIED', font=(None, 17, 'bold'), fg='red')
        txt1.place(x=90,y=170)
        subTxt = Label(win, text="Something doesn't seem right!\nPlease check your password once and try again",font=(None, 10), justify=CENTER)
        subTxt.place(x=43,y=205)
    elif args == 'welcome':
        vector = getICO(icon.ICO_TICK)
        vectorlbl = Button(win, image=vector, bd=0, command=win.destroy)
        vectorlbl.img = vector
        vectorlbl.place(x=110,y=10)
        txt1 = Label(win, text='USER AUTHENTICATED!', font=(None, 17, 'bold'), fg='green')
        txt1.place(x=45,y=170)
        subTxt = Label(win, text='Welcome!',font=(None, 12, 'bold'), justify=CENTER)
        subTxt.place(x=140,y=210)
    win.focus_set()

def getUsername(master_password):
    global configFile
    with open(configFile, 'rb') as config_file:
            data_bytes = config_file.read()
        
    try:
        config_data = crypt.decryptData(data_bytes, master_password)
        D_base.pswd = master_password
    except RuntimeError as err:
        return 'error'

    json_res = json.loads(config_data.decode('utf-8'))
    return json_res

def manageEnc(userEntry, passEntry, operation, win, mainwindow):
    '''This function takes the parameters "Master Password", "Username and password" for new registration and "Operation" for the type of operation
    (either register or login) and performs the required work.'''
    if operation == 'register':
        usr = userEntry.get()
        pas = master_password = passEntry.get()
        date, time = timestamp()
        data = {}
        data = {  #login_credentials
            'username': f'{usr}',
            'password': f'{pas}',
            'date': f'{date}',
            'time': f'{time}'
        }
        data_bytes = json.dumps(data).encode('utf-8')
        try:
            config_data = crypt.encryptData(data_bytes, master_password)
            D_base.pswd = master_password
        except RuntimeError:
            handle_message('fail', win)
            return

        with open(configFile, 'wb') as config_file:
            config_file.write(config_data)
        handle_message('success', win)
        win.destroy()

    elif operation == 'change':
        users = []
        master_password = userEntry.get()
        new_password = passEntry.get()
        with open(configFile, 'rb') as config_file:
            data_bytes = config_file.read()
        
        try:
            config_data = crypt.decryptData(data_bytes, master_password)
        except RuntimeError:
            handle_message('fail', win)
            return

        json_res = json.loads(config_data.decode('utf-8'))
        oldPass = json_res['password']
        json_res['password'] = new_password

        data_bytes = json.dumps(json_res).encode('utf-8')
        try:
            config_data = crypt.encryptData(data_bytes, new_password)
        except RuntimeError:
            handle_message('fail', win)
            return
        with open(configFile, 'wb') as config_file:
            config_file.write(config_data)

        tables = D_base.getTables()
        tables.sort()
        D_base.pswd = new_password
        for table in tables:
            fields = D_base.getElements(table)
            for i in fields.keys():
                users.append(i)

            for theUser in users:
                D_base.updateHASH(table, theUser, oldPass)
    
        handle_message('success', win, mainwindow)
        win.destroy()
        

def config(windows, configured, userAuthentication):
    if userAuthentication == True or userAuthentication == 'newuser':
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

    # MAIN ICON
    mainICO = getICO(icon.ICO_MAIN)
    win.iconphoto(False, mainICO)

    background = getICO(icon.CONFIG_1)
    background_2 = getICO(icon.CONFIG_2)

    savebtnico = getICO(icon.CONF_SAVE)
    savebtnico = savebtnico.subsample(2,2)

    closebtnico = getICO(icon.CONF_CLOSE)
    closebtnico = closebtnico.subsample(2,2)

    if configured:
        win.wm_title("KeepSafe - Change Passwords")
        #savebtn.config(command=lambda: manageEnc(userEntry, passEntry, 'change'))
        mainLbl = Label(win, image=background_2, highlightthickness=0, borderwidth=0)
        mainLbl.img = background_2
        mainLbl.place(x=0,y=0)

        userEntry = Entry(win, font=(None, 10), width=35, highlightthickness=1, highlightbackground='white', bg='#3f6975', fg='white')
        userEntry.insert(INSERT, 'Current password')
        userEntry.place(x=100,y=202)

        passEntry = Entry(win, font=(None, 10), width=35, highlightthickness=1, highlightbackground='white', bg='#3f6975', fg='white')
        passEntry.insert(INSERT, 'New password')
        passEntry.place(x=100,y=265)
        savebtn = Button(win, image=savebtnico, bd=0, bg='#3f6975', activebackground='#00ce00', command=lambda: manageEnc(userEntry, passEntry, 'change', win, windows))
        savebtn.img = savebtnico
        savebtn.place(x=110,y=310)
    else:
        win.wm_title("KeepSafe - Set-up new account")
        #savebtn.config(command=lambda: manageEnc(userEntry, passEntry, 'register'))
        mainLbl = Label(win, image=background, highlightthickness=0, borderwidth=0)
        mainLbl.img = background
        mainLbl.place(x=0,y=0)

        userEntry = Entry(win, font=(None, 10), width=35, highlightthickness=1, highlightbackground='white', bg='#3f6975', fg='white')
        userEntry.insert(INSERT, 'Enter a username')
        userEntry.place(x=100,y=202)

        passEntry = Entry(win, font=(None, 10), width=35, highlightthickness=1, highlightbackground='white', bg='#3f6975', fg='white')
        passEntry.insert(INSERT, 'Create password')
        passEntry.place(x=100,y=265)
        savebtn = Button(win, image=savebtnico, bd=0, bg='#3f6975', activebackground='#00ce00', command=lambda: manageEnc(userEntry, passEntry, 'register', win))
        savebtn.img = savebtnico
        savebtn.place(x=110,y=310)
        
    # CLOSE BUTTON
    
    closebtn = Button(win, image=closebtnico, bd=0, bg='#3f6975', activebackground='#ff0000', command=win.destroy) 
    closebtn.img = closebtnico
    closebtn.place(x=250,y=310)
    
    win.focus_set()
