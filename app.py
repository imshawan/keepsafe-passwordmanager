''' Main script for KeepSafe - Password Manager
    Author: Shawan Mandal
    
    MIT License, see LICENSE for more details.
    Copyright (c) 2021 Shawan Mandal
'''


import base64, sys
import handle_db as db
from tkinter import *
import tkinter as tk
import icons_base64 as sm
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle 

keepsafe_ico = sm.MAIN_ICOTXT
addbutton = sm.ICO_ADD
modifybtn = sm.ICO_MODIFY
deletebtn = sm.ICO_DEL
infobtn = sm.ICO_INFO
closebtn = sm.ICO_CLOSE
global response, userAuthentication
userAuthentication = False
response = False
clicked = False
height=550
width=856
bars = 'silver'
mainColor = '#212731'
    

windows = tk.Tk()
windows.title('KeepSafe - Password Manager')

screen_width = windows.winfo_screenwidth()
screen_height = windows.winfo_screenheight()

x = int((screen_width/2) - (width/2))
y = int((screen_height/2) - (height/2))

windows.geometry("{}x{}+{}+{}".format(width, height, x, y))
windows.config(bg='#A9A9A9')
windows.resizable(False, False)
root=Frame(windows, height=height, width=width, highlightthickness=0, bg=mainColor)
root.place(x=0,y=0)
C = Frame(root, height=467, width=3, bg=bars)
C.place(x=0, y=80)
D = Frame(root, height=3, width=243, bg=bars)
D.place(x=0, y=height-3)

#INIT STYLES
styles = ttk.Style()
style = ThemedStyle(windows)
#app.ttkStyle = ThemedStyle(app.topLevel)
style.set_theme("adapta")
styles.map("Treeview", background=[('selected', '#0f51c9')])
#styles.theme_use('black')
styles.configure("Treeview", background='#f0f0f0', foreground = 'black',fieldbackground="#f0f0f0", font=(None, 10))
styles.configure("Treeview.Heading", font=(None, 10,'bold'))

def getICONS(icon):
    base64_img_bytes = icon.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    ico = PhotoImage(data=decoded_image_data)
    return ico

def checkAuthentication():
    global userAuthentication
    passwd = L_BOX.get()
    if passwd == 'Enter Master Password':
        loginFrame.destroy()
        #messagebox.showinfo('Welcome!', "Authentication Succeeded!")
        userAuthentication = True
        getData(False)
    else:
        messagebox.showerror('Error!', "Authentication Failed!")

def close():
    sys.exit()

def getValues(category):
    ''' This function fetches all the values (rows and columns) from the table supplied as arguements in Variable "category"'''
    usr = []
    psw = []
    global rightframelistbox
    fields = db.getElements('hello')
    for i in fields.keys():
        usr.append(i)
    for i in fields.values():
        psw.append(i)
    getData(False)
    for i in range(len(usr)):
        rightframelistbox.insert('', 'end', values=(str(i+1) + ".",usr[i],psw[i]))
    
    rightframelistbox.config(yscrollcommand=rightframelistboxscroll.set)
    rightframelistboxscroll.config(command=rightframelistbox.yview)

def getData(clicked): 
    '''This function fetches all the tables from the database'''
    tbl = []
    global leftframelistbox, rightframelistbox, userAuthentication
    if userAuthentication != True:
        messagebox.showerror('Error!', "Authenticate Yourself First!")
        return
    else:
        pass

    tables = db.getTables()
    tables.sort()
    for table in tables:
        leftframelistbox.insert('', 'end', values=table)
    if clicked:
        currentSelectionLeft = leftframelistbox.focus()
        valueArray_2 = leftframelistbox.item(currentSelectionLeft)['values'] # CONTAINS ARRAY
        if valueArray_2 == "":
            return
        else:
            for i in leftframelistbox.get_children():
                leftframelistbox.delete(i)
            for i in rightframelistbox.get_children():
                rightframelistbox.delete(i)
            getValues(valueArray_2[0])

def getCurrentValues(r):
    currentSelectionRight = r.focus()
    valueArray_1 = r.item(currentSelectionRight)['values']
    username = valueArray_1[1]
    passwrd = valueArray_1[2]
    return username, passwrd
    

def view():
    global rightframelistbox
    username =''
    passwrd = ''
    try:
        username, passwrd = getCurrentValues(rightframelistbox)
    except:
        pass
    
    if username == '' and passwrd == '':
        return
        
    width = 500
    height = 220
    win = tk.Toplevel()
    win.wm_title("KeepSafe - View")
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()

    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)
    win.focus_set()

    win_root = Frame(win, height=height-20, width=width-20)
    win_root.place(x=10, y=10)

    #USERNAME Frame
    U_FRAME = Frame(win_root, height=70, width=450)
    U_FRAME.place(x=15,y=5)
    u = Label(U_FRAME, text='Your Username:',font=(None, 14, 'bold'))
    u.place(x=0, y=0)
    U_BOX = Entry(U_FRAME,font=('monospace', 11))
    U_BOX.insert(INSERT, username)
    U_BOX.config(width=55, highlightthickness=1, highlightbackground='#0b5394')
    U_BOX.place(x=2,y=35)

    #PASSWORD Frame
    P_FRAME = Frame(win_root, height=70, width=450)
    P_FRAME.place(x=15,y=80)
    p = Label(P_FRAME, text='Your Password:', font=(None, 14, 'bold'))
    p.place(x=0, y=0)
    P_BOX = Entry(P_FRAME,font=('monospace', 11))
    P_BOX.insert(INSERT, passwrd)
    P_BOX.config(width=55, highlightthickness=1, highlightbackground='#0b5394')
    P_BOX.place(x=2,y=35)

    #BUTTONS
    bs = Button(win, text='Close',bd=0, bg=bars, width=10, activebackground=bars, command=win.destroy)
    bs.config(highlightbackground='blue', highlightthickness=1)
    bs.config(highlightcolor="red")
    bs.place(x=210, y=height-48)

def resetConsole():
    # Clears all the elements (Username and password list) from the console
    global rightframelistbox
    for i in rightframelistbox.get_children():
        rightframelistbox.delete(i)



def rightClick(x):
    right_menu.tk_popup(x.x_root, x.y_root)

def leftClick(x):
    left_menu.tk_popup(x.x_root, x.y_root)

def modifyElements():
    pass



# Login Frame
loginFrame = Frame(windows, height=27, width=300, bg=bars)
loginFrame.place(x=width/2-150, y=80)
L_BOX = Entry(loginFrame,font=('monospace', 10))
L_BOX.insert(INSERT, 'Enter Master Password')
L_BOX.config(width=25, highlightthickness=1, highlightbackground='#0b5394')
L_BOX.place(x=10,y=3)
L_ico = PhotoImage(file='C:/Users/shawan049/Pictures/button_login.png')
L_Btn = Button(loginFrame, image=L_ico, bd=0, bg=bars, activebackground=bars, command=checkAuthentication)
L_Btn.place(x=200, y=2)

#-------------------------------------------------------------------------------------
#Title Frame
TitleFrame = Frame(root, height=70, width=200, bg=mainColor, highlightthickness=0)
TitleFrame.place(x=10,y=0)
ico1 = getICONS(keepsafe_ico)
head = Label(TitleFrame, image=ico1, borderwidth=0)
head.place(x=5,y=5)

#-------------------------------------------------------------------------------------
#Action Frame
AC_text = "#ffffff"
actionFrame = Frame(root, height=70, width=350, bg=mainColor, highlightthickness=0)
actionFrame.place(x=350, y=10)
icoadd = getICONS(addbutton)
icoedit = getICONS(modifybtn)
icodel = getICONS(deletebtn)
icoinfo = getICONS(infobtn)
icoclose = getICONS(closebtn)
addbtnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
addbtnFrame.place(x=0,y=0)
addbtn = Button(addbtnFrame, image=icoadd, bg=mainColor,activebackground=mainColor, borderwidth=0)
addbtn.place(x=4,y=0)
addbtntxt = Label(addbtnFrame, text="Add", bg=mainColor, fg=AC_text)
addbtntxt.place(x=10,y=45)
editbtnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
editbtnFrame.place(x=70,y=0)
editbtn = Button(editbtnFrame, image=icoedit, bg=mainColor,activebackground=mainColor, borderwidth=0)
editbtn.place(x=4,y=0)
editbtntxt = Label(editbtnFrame, text="Modify", bg=mainColor, fg=AC_text)
editbtntxt.place(x=3,y=45)
delbtnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
delbtnFrame.place(x=140,y=0)
delbtn = Button(delbtnFrame, image=icodel, bg=mainColor,activebackground=mainColor, borderwidth=0)
delbtn.place(x=4,y=0)
delbtntxt = Label(delbtnFrame, text="Delete", bg=mainColor, fg=AC_text)
delbtntxt.place(x=5,y=45)
info_btnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
info_btnFrame.place(x=210,y=0)
info_btn = Button(info_btnFrame, image=icoinfo, bg=mainColor,activebackground=mainColor, borderwidth=0)
info_btn.place(x=4,y=0)
info_btntxt = Label(info_btnFrame, text="Info", bg=mainColor, fg=AC_text)
info_btntxt.place(x=10,y=45)
close_btnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
close_btnFrame.place(x=280,y=0)
close_btn = Button(close_btnFrame, image=icoclose, bg=mainColor,activebackground=mainColor, borderwidth=0, command=close)
close_btn.place(x=4,y=0)
close_btntxt = Label(close_btnFrame, text="Close", bg=mainColor, fg=AC_text)
close_btntxt.place(x=8,y=45)

#-------------------------------------------------------------------------------------
# LEFT FRAME
leftframe = Frame(root, height=467, width=240)
leftframe.place(x=3, y=80)
# Listbox Frame
G = Frame(leftframe, height=27, width=240, bg=bars)
G.place(x=0,y=0)

leftframelistboxFrame = Frame(leftframe, height=425, width=222)
leftframelistboxFrame.place(x=0, y=28)
# ListBox
leftframelistbox = ttk.Treeview(leftframelistboxFrame, height=18)
leftframelistbox.configure(columns=('category'), show='headings')
leftframelistbox.heading(0, text='Category')
leftframelistbox.column(0,width=182)
leftframelistbox.pack(side='left', fill='y')

# Scrollbar
leftframelistboxscroll = Scrollbar(leftframelistboxFrame, orient='vertical')
leftframelistboxscroll.pack(side='right', fill='y')

# RIGHT CLICK Functionality for Left Frame
left_menu = Menu(leftframelistbox, tearoff=False)
left_menu.add_command(label='Get Data', command=lambda: getData(True))
leftframelistbox.bind("<Button-3>", leftClick)

#-------------------------------------------------------------------------------------
# Right Frame
rightframe = Frame(root, height=508, width=width-232, bg=bars)
rightframe.place(x=243, y=80)
# Listbox Frame
rightframelistboxFrame = Frame(rightframe, height=500, width=width-232)
rightframelistboxFrame.place(x=0, y=27)
# ListBox
global rightframelistbox
rightframelistbox = ttk.Treeview(rightframelistboxFrame) #(rightframelistboxFrame, height=30, width=92, borderwidth=0, bg='#f0f0f0')
rightframelistbox.config(columns=('id', 'usr', 'psw'), show='headings', height=18)
rightframelistbox.heading(0, text='ID')
rightframelistbox.heading(1, text='Username')
rightframelistbox.heading(2, text='Password')
rightframelistbox.column(0,width=30)
rightframelistbox.column(1,width=293)
rightframelistbox.column(2,width=230)
rightframelistbox.pack(side='left', fill='y')

# Scrollbar
rightframelistboxscroll = Scrollbar(rightframelistboxFrame, orient='vertical')
rightframelistboxscroll.pack(side='right', fill='y')

# RIGHT CLICK Functionality for Right Frame
right_menu = Menu(rightframelistbox, tearoff=False)
right_menu.add_command(label='...')
right_menu.add_command(label='View   ', command=view)
right_menu.add_command(label='Delete   ')
right_menu.add_command(label='Modify Username')
right_menu.add_command(label='Modify Password')
right_menu.add_separator()
right_menu.add_command(label='Close', command=resetConsole)
rightframelistbox.bind("<Button-3>", rightClick)



windows.mainloop()
