''' This module includes informations such as ABOUT and LICENSE information required for KeepSafe - Password Manager
    Author: Shawan Mandal
    
    MIT License, see LICENSE for more details.
    Copyright (c) 2021 Shawan Mandal
'''


from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import tkinter as tk
import platform, socket, base64
import icons_base64 as icons




def getICO(icon):
    base64_img_bytes = icon.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    ico = PhotoImage(data=decoded_image_data)
    return ico

def aboutwindow(windows):
    width = 500
    height = 570
    win = tk.Toplevel()
    win.wm_title("KeepSafe - About")
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()

    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)
    win.focus_set()
    #mainico = geticons(MAIN)
    #win.iconphoto(False, mainico)
    iconMain = getICO(icons.MAIN_ICOTXT)

    host = socket.gethostname()
    processor = platform.processor()
    System = f'{platform.system()}, {platform.version()}, {platform.architecture()[0]}'
    Machine = processor.split(',')

    headFrame = Frame(win, height=100, width=width, bg='#212731')
    headFrame.place(x=0,y=0)
    
    lbl1 = Label(headFrame, image=iconMain, borderwidth=0)
    lbl1.img = iconMain
    lbl1.place(x=145,y=5)
    vlbl = Label(headFrame, text='Version 1.0.1', bg='#212731', fg='#ffffff', font=(None, 8, 'bold'))
    vlbl.place(x=205,y=72)
    
    infoframe = Frame(win, height=95, width=380, highlightthickness=1, highlightbackground='black', bg='silver')
    infoframe.place(x=60,y=120)

    lbl2 = Label(infoframe, text=f'Host Machine: {host}', bg='silver')
    lbl2.place(x=20, y=5)
    lbl3 = Label(infoframe, text=f'Current System: {System}', bg='silver')
    lbl3.place(x=20, y=25)
    lbl4 = Label(infoframe, text=f'Processor: {processor}', bg='silver')
    lbl4.place(x=20, y=45)
    lbl5 = Label(infoframe, text=f'Machine Type: {Machine[1]}', bg='silver')
    lbl5.place(x=20, y=65)

    aboutframe = Frame(win, height=230, width=420)
    aboutframe.place(x=55, y=230)
    about = Label(aboutframe, text='KeepSafe is a free Powerful and secure password manager with a elegant \n'\
                                    'design. It lets you manage all your credentials quickly and efficiently for \n'\
                                    'local applications and online services in a single window. \n\n'\
                                    'KeepSafe stores your credentials in an encrypted database so that no one\n'\
                                    'can access your sensitive information without your permission.\n', justify=LEFT)
    about.place(x=0,y=0)
    
    features = Label(aboutframe, text='Currently KeepSafe fully Supports (Features): \n\n'\
                                        '    - A simple, flat and minimal UI design\n'\
                                        '    - Add, Modify, Delete records with ease\n'\
                                        '    - All of your credentials are stored in a encrypted database\n'\
                                        '    - Friendly User Account controls', justify=LEFT)
    features.place(x=0, y=95)

    footer = Frame(win, height=60, width=420)
    footer.place(x=60,y=440)
    footerlbl = Label(footer, text='KeepSafe is a free and open-source password manager. Send me your \n'\
                                    'feedbacks, bug-reports and suggestions about KeepSafe to:', justify=CENTER)
    footerlbl.place(x=0,y=0)
    emaillbl = Label(footer, text='imshawan.dev049@gmail.com',fg="blue", cursor="hand2")
    emaillbl.place(x=100,y=35)

    b = ttk.Button(win, text="CLOSE", command=win.destroy)
    b.place(x=206, y=510)

def licenses(windows):
    width = 500
    height = 480
    win = tk.Toplevel()
    win.wm_title("KeepSafe - View Licenses")
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()

    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)
    win.focus_set()
    #mainico = geticons(MAIN)
    #win.iconphoto(False, mainico)
    iconMain = getICO(icons.MAIN_ICOTXT)

    infoframe = Frame(win, height=60, width=width, bg='#212731')
    infoframe.place(x=0,y=5)
    lbl1 = Label(infoframe, image=iconMain, borderwidth=0)
    lbl1.img = iconMain
    lbl1.place(x=145,y=5)
    mit = Label(win, text='MIT License', font=(None, 12, "bold"))
    mit.place(x=198,y=80)
    copyryt = Label(win, text='Copyright (c) 2020 Shawan Mandal')
    copyryt.place(x=150,y=105)

    bottomfrm = Frame(win, height=290, width=420)
    bottomfrm.place(x=45, y=130)
    textlbl = Label(bottomfrm, text='Permission is hereby granted, free of charge, to any person obtaining a copy\n'\
                                    'of this software and associated documentation files (the "Software"), to deal\n'\
                                    'in the Software without restriction, including without limitation the rights to\n'\
                                    'use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies\n'\
                                    'of the Software, and to permit persons to whom the Software is furnished to \n'\
                                    'do so, subject to the following conditions:\n\n'\
                                    'The above copyright notice and this permission  notice shall be included in\n'\
                                    'all copies or substantial portions of the Software.\n\n'\
                                    'THE  SOFTWARE  IS  PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\n'\
                                    'EXPRESS  OR  IMPLIED, INCLUDING  BUT NOT LIMITED TO THE WARRANTIES \n'\
                                    'OF MERCHANTABILITY, FITNESS  FOR  A  PARTICULAR PURPOSE AND NON-\n'\
                                    'INFRINGEMENT.IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLD-\n'\
                                    'ERS BE  LIABLE  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\n'\
                                    'IN AN ACTION  OF CONTRACT, TORT  OR OTHERWISE, ARISING FROM, OUT\n'\
                                    'OF  OR  IN  CONNECTION  WITH  THE  SOFTWARE  OR  THE  USE  OR OTHER\n'\
                                    'DEALINGS IN THE SOFTWARE.', justify=LEFT)
    textlbl.place(x=0,y=0)

    b = ttk.Button(win, text="CLOSE", command=win.destroy)
    b.place(x=205, y=420)

