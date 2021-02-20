''' 
    Main script for KeepSafe - Password Manager
    Author: Shawan Mandal
    
    MIT License, see LICENSE for more details.
    Copyright (c) 2021 Shawan Mandal
'''


import base64, sys, os
import handle_db as db
from tkinter import *
import tkinter as tk
import icons_base64 as sm
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle 
import information as inf
import config as conf
import encryption as crypt

# ICONS Init
keepsafe_ico = sm.MAIN_ICOTXT
addbutton = sm.ICO_ADD
viewbtn = sm.ICO_VIEW
deletebtn = sm.ICO_DEL
settingsbtn = sm.ICO_CONFIG
loginbtn = sm.ICO_LOGINBTN
infobtn = sm.ICO_INFO
closebtn = sm.ICO_CLOSE
licensebtn = sm.ICO_LICENSE

# GLOBAL VARIABLES
global U_BOX, P_BOX, T_BOX, C_BOX
global response, userAuthentication, currentCategory, hide, passwd, usernamee
currentCategory = C_BOX = T_BOX = U_BOX = P_BOX = L_BOX = passwd = usernamee = ""
userAuthentication = False
hide = True
response = False
clicked = False

# Window properties
height=550
width=1006

# Color init
bars = 'silver'
mainColor = '#212731'
    
#CONFIG File
cf = 'resources'
if not os.path.exists(cf):
    os.makedirs(cf)
fl = 'config.dat'
configFile = os.path.join(cf, fl)


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
styles.configure("Treeview", background='#f0f0f0', foreground = 'black',fieldbackground="#f0f0f0", font=(None, 10), relief = 'flat')
styles.configure("Treeview.Heading", font=(None, 11,'bold'))

def getICONS(icon):
    base64_img_bytes = icon.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    ico = PhotoImage(data=decoded_image_data)
    return ico

def checkAuthentication(w):
    global userAuthentication, passwd
    passwd = L_BOX.get()
    user = conf.getUsername(passwd) #Check if the master password can decrypt the config.json file and return response
    if user == 'error':
        messagebox.showerror('Error!', "Incorrect Password, Authentication Failed!")
    else:
        #Condition, what to do if there is error during decryption
        loginFrame.destroy()
        userAuthentication = True
        getData(False)
        w.title(f"KeepSafe - Logged in: {user['username']}")
        db.pswd = passwd
        conf.handle_message('welcome',w,'')
        #messagebox.showinfo('Authenticated!', f"Welcome {user['username']}!")

def getValues(category):
    ''' This function fetches all the values (rows and columns) from the table supplied as arguements in Variable "category"'''
    usr = []
    psw = []
    
    global rightframelistbox, currentCategory, userAuthentication
    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return

    fields = db.getElements(category)
    for i in fields.keys():
        usr.append(i)
    for i in fields.values():
        psw.append(i)
    getData(False)

    if usr == [] or psw == []: # IF CATEGORY TABLE IS EMPTY
        rightframelistbox.insert('', 'end', values=('1' + ".",currentCategory + " credentials","<Empty Field>", "<Empty Field>"))

    for i in range(len(usr)):
        decryptedPassword = crypt.decryptData(bytes(psw[i], 'utf-8'), db.pswd).decode()
        rightframelistbox.insert('', 'end', values=(str(i+1) + ".",currentCategory + " credentials",usr[i],len(decryptedPassword)*"*"))
    
    rightframelistbox.config(yscrollcommand=rightframelistboxscroll.set)
    rightframelistboxscroll.config(command=rightframelistbox.yview)


def getData(clicked): 
    '''This function fetches all the tables from the database'''
    
    tbl = []
    global leftframelistbox, rightframelistbox, userAuthentication, currentCategory
    if userAuthentication != True:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return
    else:
        pass
    #Get the name of the table/category and sort them
    tables = db.getTables()
    tables.sort()
    
    for table in tables:
        leftframelistbox.insert('', 'end', values=table)

    if clicked:
        currentSelectionLeft = leftframelistbox.focus()
        valueArray_2 = leftframelistbox.item(currentSelectionLeft)['values'] # CONTAINS ARRAY

        if valueArray_2 == "" or valueArray_2 == []:
            for i in leftframelistbox.get_children():
                leftframelistbox.delete(i)
            for table in tables:
                leftframelistbox.insert('', 'end', values=table)
            return
        else:
            for i in leftframelistbox.get_children():
                leftframelistbox.delete(i)
            for i in rightframelistbox.get_children():
                rightframelistbox.delete(i)
            currentCategory = valueArray_2[0]
            getValues(valueArray_2[0])

def getCurrentValues(r):
    ''' Takes the TreeView-Box as arguements and returns the Usernames and Passwords depending upon current selection '''
    global userAuthentication

    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return
    currentSelectionRight = r.focus()
    valueArray_1 = r.item(currentSelectionRight)['values']
    username = valueArray_1[2]
    passwrd = valueArray_1[3]
    return username, passwrd 

def RefreshValues():
    '''Refresh the current items'''

    global currentCategory, userAuthentication

    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return

    if currentCategory == '':
        return

    for i in leftframelistbox.get_children():
        leftframelistbox.delete(i)
    for i in rightframelistbox.get_children():
        rightframelistbox.delete(i)
    getValues(currentCategory)
    

def addCategory():
    ''' This function enables the user to add a new category as the name describes '''

    global T_BOX, currentCategory, userAuthentication
    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return

    def add(win):
        global T_BOX, currentCategory
        category = T_BOX.get()
        if category == "":
            messagebox.showerror("Error!", "No values was entered!")
            win.focus_set()
            return
        db.create_DB(category)
        messagebox.showinfo("Information!", f"{category} Category Created Successfully!")
        currentCategory = category
        RefreshValues()
        win.destroy()

    width = 500
    height = 130
    win = tk.Toplevel()
    win.wm_title("KeepSafe - Add Category")
    screen_width = windows.winfo_screenwidth()
    screen_height = windows.winfo_screenheight()

    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    win.geometry("{}x{}+{}+{}".format(width, height, x, y))
    win.resizable(False, False)
    mainICO = getICONS(sm.ICO_MAIN)
    win.iconphoto(False, mainICO)
    win.focus_set()

    win_root = Frame(win, height=height-20, width=width-20)
    win_root.place(x=10, y=10)

    #USERNAME Frame
    U_FRAME = Frame(win_root, height=70, width=450)
    U_FRAME.place(x=15,y=5)
    u = Label(U_FRAME, text='Category Name: (Without Spaces)',font=(None, 14, 'bold'))
    u.place(x=0, y=0)

    T_BOX = Entry(U_FRAME,font=('monospace', 11))
    T_BOX.config(width=55, highlightthickness=1, highlightbackground='#0b5394')
    T_BOX.place(x=2,y=35)

    bs = Button(win, text='Add Category', font=(None, 10, 'bold'), bd=0, bg=bars, width=15, activebackground=bars, command=lambda: add(win))
    bs.config(highlightbackground='blue', highlightthickness=1)
    bs.config(highlightcolor="red")
    bs.place(x=185, y=height-40)

def delete_Category():
    ''' This function deletes the category depending upon the user selection '''

    global leftframelistbox, userAuthentication

    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return

    currentSelectionLeft = leftframelistbox.focus()
    valueArray_2 = leftframelistbox.item(currentSelectionLeft)['values'] # CONTAINS ARRAY
    if valueArray_2 == "":
        return

    ans = messagebox.askokcancel("Warning!", f"Are you sure to delete category {valueArray_2[0]}?")
    if ans:
        try:
            db.delTable(valueArray_2[0])
            messagebox.showinfo("Information!", f"{valueArray_2[0]} was deleted successfully!")
            RefreshCategory()
        except RuntimeError as err:
            messagebox.showerror("Error!", err)

def RefreshCategory():
    ''' Refreshes the category table on the left frame '''
    global userAuthentication
    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return

    for i in leftframelistbox.get_children():
        leftframelistbox.delete(i)
    for i in rightframelistbox.get_children():
        rightframelistbox.delete(i)
    getData(False)


def view():
    ''' Right-click "View" function '''
    global rightframelistbox, userAuthentication, hide, currentCategory
    hide = True

    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return

    username =''
    passwrd = ''
    try:
        username, passwrd = getCurrentValues(rightframelistbox)
    except:
        pass

    if username == '' and passwrd == '' or username == '<Empty Field>':
        messagebox.showerror("Error!", "Selected value is an empty field!")
        return
    passwrd = db.getA_Password(currentCategory, username)
    passwrd = crypt.decryptData(bytes(passwrd, 'utf-8'), db.pswd).decode()

    def showORhide(s, psBOX, pswrd):
        global hide

        if hide:
            s.config(text='Hide')
            psBOX.delete(0, END)
            psBOX.insert(INSERT, pswrd)
            hide = False
        else:
            s.config(text='Show')
            psBOX.delete(0, END)
            psBOX.insert(INSERT, len(pswrd) * "*")
            hide = True


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
    mainICO = getICONS(sm.ICO_MAIN)
    win.iconphoto(False, mainICO)
    
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
    P_BOX.insert(INSERT, len(passwrd) * "*")
    P_BOX.config(width=55, highlightthickness=1, highlightbackground='#0b5394')
    P_BOX.place(x=2,y=35)

    #BUTTONS 

    #SHOW / HIDE BUTTON
    sh = Button(win, text='Show', bd=0, bg=bars, width=10, activebackground=bars, command=lambda: showORhide(sh, P_BOX, passwrd))
    sh.place(x=160, y=height-48)

    #CLOSE BUTTON
    bs = Button(win, text='Close',bd=0, bg=bars, width=10, activebackground=bars, command=win.destroy)
    bs.config(highlightbackground='blue', highlightthickness=1)
    bs.config(highlightcolor="red")
    bs.place(x=270, y=height-48)


def resetConsole():
    ''' Clears all the elements (Username and password list) from the console'''
    global rightframelistbox
    for i in rightframelistbox.get_children():
        rightframelistbox.delete(i)

def modify_Elements(modificationType):
    global rightframelistbox, currentCategory, userAuthentication, usernamee

    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return

    usernamee =''
    passwrd = ''
    try:
        usernamee, passwrd = getCurrentValues(rightframelistbox)
    except:
        pass
    
    if usernamee == '' and passwrd == '':

        if modificationType == 'new':
            pass
        else:
            messagebox.showwarning("Warning!", "You need to select a record!") 
            return  
    else:
        pass
    def edit(table, editType, currentvalue, newvalue, win):
        global U_BOX, P_BOX, C_BOX, currentCategory
        if table == "":
            table = C_BOX.get()

        if table == "":
            messagebox.showerror("Error!", "Category type cannot be blank")
            win.focus_set()

        elif editType == 'new':
            try:
                username = U_BOX.get()
                passwrd = P_BOX.get()
                if username == "" or passwrd == "":
                    messagebox.showerror("Error!", "No values was entered!")
                    return
                
                db.addElements(table, username, passwrd)
                messagebox.showinfo("Information!", "Values added!")
                currentCategory = table
                RefreshValues()
                win.destroy()
            except RuntimeError as err:
                err = str(err)
                try:
                    err = err.replace("table", "category")
                except:
                    pass
                messagebox.showerror("Error!", err)
                win.focus_set()
        else:
            #currentvalue = U_BOX.get()
            newvalue = P_BOX.get()
            if newvalue == "":
                messagebox.showerror("Error!", "No values was entered!")
                return
            try:
                if editType == 'password':
                    # Encrypting the plain password
                    newvalue = crypt.encryptData(bytes(newvalue, 'utf-8'), db.pswd).decode()
                    # Getting the current encrypted-password
                    currentvalue = db.getA_Password(table, usernamee)

                db.modifyElements(table, editType, currentvalue, newvalue)
                messagebox.showinfo("Information!", "Values modified successfully!")
                RefreshValues()
                win.destroy()
            except RuntimeError as err:
                err = str(err)
                try:
                    err = err.replace("table", "category")
                except:
                    pass
                messagebox.showerror("Error!", err)
                win.focus_set()

    def editVal(table, editType, currentvalue, newvalue):
        if currentvalue == '<Empty Field>':
            messagebox.showerror("Error!", "Selected value is an empty field!")
            return

        global currentCategory, usernamee
        e = editType[0].upper()
        e = e + editType[1:]
        width = 500
        height = 300
        win = tk.Toplevel()
        win.wm_title(f"KeepSafe - Edit your {editType}")
        screen_width = windows.winfo_screenwidth()
        screen_height = windows.winfo_screenheight()

        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2))

        win.geometry("{}x{}+{}+{}".format(width, height, x, y))
        win.resizable(False, False)
        mainICO = getICONS(sm.ICO_MAIN)
        win.iconphoto(False, mainICO)

        win.focus_set()

        win_root = Frame(win, height=height-20, width=width-20)
        win_root.place(x=10, y=10)

        global U_BOX, P_BOX, C_BOX

        # TABLE/CATEGORY NAME
        C_FRAME = Frame(win_root, height=70, width=450)
        C_FRAME.place(x=15,y=5)
        c = Label(C_FRAME, text=f'{e} Category:',font=(None, 14, 'bold'))
        c.place(x=0, y=0)
        C_BOX = Entry(C_FRAME,font=('monospace', 11))
        C_BOX.insert(INSERT, currentCategory)
        C_BOX.config(width=55, highlightthickness=1, highlightbackground='#0b5394')
        C_BOX.place(x=2,y=35)

        #USERNAME Frame
        U_FRAME = Frame(win_root, height=70, width=450)
        U_FRAME.place(x=15,y=80)
        u = Label(U_FRAME, text=f'Your Current {editType}:',font=(None, 14, 'bold'))
        u.place(x=0, y=0)
        U_BOX = Entry(U_FRAME,font=('monospace', 11))
        if editType.lower() == 'password':
            currpswd = db.getA_Password(currentCategory, usernamee)
            currpswd = crypt.decryptData(bytes(currpswd, 'utf-8'), db.pswd).decode()
            U_BOX.insert(INSERT, currpswd)
        else:
            U_BOX.insert(INSERT, currentvalue)
        U_BOX.config(width=55, highlightthickness=1, highlightbackground='#0b5394')
        U_BOX.place(x=2,y=35)

        #PASSWORD Frame
        P_FRAME = Frame(win_root, height=70, width=450)
        P_FRAME.place(x=15,y=160)
        p = Label(P_FRAME, text=f'Your new {editType}:', font=(None, 14, 'bold'))
        p.place(x=0, y=0)
        P_BOX = Entry(P_FRAME,font=('monospace', 11))
        P_BOX.config(width=55, highlightthickness=1, highlightbackground='#0b5394')
        P_BOX.place(x=2,y=35)
        
        bs = Button(win,bd=0, bg=bars, width=15, activebackground=bars)
        bs.config(highlightbackground='blue', highlightthickness=1, font=(None, 10, 'bold'))
        bs.place(x=190, y=height-48)

        if editType == 'new':
            win.wm_title("KeepSafe - Add Credentials")
            c.config(text='Enter Category Name')
            u.config(text='Enter Username')
            p.config(text='Enter Password')
            U_BOX.delete(0, END)
            U_BOX.insert(INSERT, "Your Username")
            P_BOX.delete(0, END)
            P_BOX.insert(INSERT, "Your Password")
            if currentCategory != "":
                C_BOX.configure(state='disabled')

            bs.config(text='Add Values',command=lambda: edit(currentCategory, 'new', usernamee, passwrd, win))            
        else:
            U_BOX.configure(state='disabled')
            C_BOX.configure(state='disabled')
            bs.config(text='Change Values', command=lambda: edit(currentCategory, editType, currentvalue, newvalue, win))
            bs.place(x=185, y=height-48)

    
    if modificationType == '':
        return
    elif modificationType == 'usr':
        editVal(currentCategory, 'username', usernamee, 'newvalue')
    elif modificationType == 'psw':
        editVal(currentCategory, 'password', passwrd, 'newvalue')
    elif modificationType == 'new':
        editVal('tablename', 'new', 'username', 'password')

def delete_Elements():
    ''' Deletes values of a particular username upon user condition '''
    global rightframelistbox, currentCategory, userAuthentication

    if userAuthentication:
        pass
    else:
        messagebox.showerror('Error!', "Authenticate yourself first!")
        return

    usr =''
    psw = ''
    try:
        usr, psw = getCurrentValues(rightframelistbox)
    except:
        pass
    
    if usr == '' and psw == '':
        messagebox.showwarning("Warning!", "Select a field first!")
        return
    elif usr == '<Empty Field>' or psw == '<Empty Field>':
        messagebox.showerror("Error!", "Selected value is an empty field!")
        return
        
    ans = messagebox.askokcancel("Warning!", f"Are you sure to delete values of {usr}?")
    if ans:
        try:
            db.delElements(currentCategory, usr)
            RefreshValues()
            messagebox.showinfo("Success!", f"Values of '{usr}'' has been deleted!")
        except RuntimeError as err:
            messagebox.showerror("Error!", err)
    else:
        return

def delete():
    currentSelection1 = leftframelistbox.focus()
    valueArray_1 = leftframelistbox.item(currentSelection1)['values'] # CONTAINS ARRAY
    if valueArray_1 == "":
        pass

    currentSelection2 = rightframelistbox.focus()
    valueArray2 = rightframelistbox.item(currentSelection2)['values']
    if valueArray2 == "":
        pass

def rightClick(x):
    right_menu.tk_popup(x.x_root, x.y_root)

def leftClick(x):
    left_menu.tk_popup(x.x_root, x.y_root)

def logincheckbox():
    global configured, L_BOX
    loginBox = Frame(loginFrame, height=27, width=360, bg=bars)
    loginBox.place(x=340,y=0)
    L_BOX = Entry(loginBox,font=('monospace', 10))
    L_BOX.insert(INSERT, 'Enter Master Password')
    L_BOX.config(width=30, highlightthickness=1, highlightbackground='#0b5394')
    L_BOX.place(x=10,y=3)
    L_Btn = Button(loginBox, image=button_login, bd=0, bg=bars, activebackground=bars, command=lambda: checkAuthentication(windows))
    L_Btn.place(x=235, y=2)
    configured = True

#-------------------------------------------------------------------------------------

# Login Frame
loginFrame = Frame(windows, height=27, width=width, bg=bars)
loginFrame.place(x=0, y=80)
button_login = getICONS(loginbtn)
configured = False

#Check for 'config.json' and if found then check for its contents... IF empty, proceed re-configuration
try:
    with open(configFile, 'r') as f:
        dat = f.read()
except:
    pass

if not os.path.isfile(configFile) or dat == 'null' or dat == '':
    configured = False
    nosetup = Frame(loginFrame, height=25, width=width-100, bg=bars)
    nosetup.place(x=250,y=3)
    txtLbl = Label(nosetup, text="It looks like you're using this application for the first time,", bg=bars)
    txtLbl.place(x=0,y=0)
    setupbtn = Button(nosetup,bd=0, text='Set up', cursor="hand2", fg='blue', bg=bars, activebackground=bars, command=lambda: conf.config(windows, configured, 'newuser'))
    setupbtn.place(x=306,y=0)
    textlbl = Label(nosetup, text='your account to continue', bg=bars)
    textlbl.place(x=343,y=0)
    
else:
    logincheckbox()


# APPLICATION MAIN ICON
mainICO = getICONS(sm.ICO_MAIN)
windows.iconphoto(False, mainICO)

#-------------------------------------------------------------------------------------
#Title Frame
TitleFrame = Frame(root, height=70, width=200, bg=mainColor, highlightthickness=0)
TitleFrame.place(x=10,y=0)
ico1 = getICONS(keepsafe_ico)
head = Label(TitleFrame, image=ico1, borderwidth=0)
head.place(x=5,y=5)

#-------------------------------------------------------------------------------------
#Action Frame
placeframe = 0
AC_text = "#ffffff"
actionFrame = Frame(root, height=70, width=500, bg=mainColor, highlightthickness=0)
actionFrame.place(x=370, y=10)
icoadd = getICONS(addbutton)
icoview = getICONS(viewbtn)
icosettings = getICONS(settingsbtn)
icoinfo = getICONS(infobtn)
icoclose = getICONS(closebtn)
icolic = getICONS(licensebtn)
addbtnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
addbtnFrame.place(x=placeframe,y=0)
addbtn = Button(addbtnFrame, image=icoadd, bg=mainColor,activebackground=mainColor, borderwidth=0, command=lambda: modify_Elements('new'))
addbtn.place(x=4,y=0)
addbtntxt = Label(addbtnFrame, text="Add", bg=mainColor, fg=AC_text)
addbtntxt.place(x=10,y=45)

placeframe  += 70
viewbtnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
viewbtnFrame.place(x=placeframe,y=0)
viewbtnn = Button(viewbtnFrame, image=icoview, bg=mainColor,activebackground=mainColor, borderwidth=0, command=view)
viewbtnn.place(x=4,y=0)
viewbtntxt = Label(viewbtnFrame, text="View", bg=mainColor, fg=AC_text)
viewbtntxt.place(x=9,y=45)


placeframe += 70
settingsFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
settingsFrame.place(x=placeframe, y=0)
settingsbtnn = Button(settingsFrame, image=icosettings, bg=mainColor, activebackground=mainColor, borderwidth=0, command=lambda: conf.config(windows, configured, userAuthentication))
settingsbtnn.place(x=4, y=0)
settingstxt = Label(settingsFrame, text='Control', bg=mainColor, fg=AC_text)
settingstxt.place(x=1,y=45)

placeframe += 70
close_btnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
close_btnFrame.place(x=placeframe,y=0)
close_btn = Button(close_btnFrame, image=icoclose, bg=mainColor,activebackground=mainColor, borderwidth=0, command=windows.destroy)
close_btn.place(x=4,y=0)
close_btntxt = Label(close_btnFrame, text="Close", bg=mainColor, fg=AC_text)
close_btntxt.place(x=8,y=45)

placeframe += 70
info_btnFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
info_btnFrame.place(x=placeframe,y=0)
info_btn = Button(info_btnFrame, image=icoinfo, bg=mainColor,activebackground=mainColor, borderwidth=0, command=lambda: inf.aboutwindow(windows))
info_btn.place(x=4,y=0)
info_btntxt = Label(info_btnFrame, text="About", bg=mainColor, fg=AC_text)
info_btntxt.place(x=6,y=45)

placeframe += 70
info_licFrame = Frame(actionFrame, height=70, width=50, bg=mainColor)
info_licFrame.place(x=placeframe,y=0)
lic_btn = Button(info_licFrame, image=icolic, bg=mainColor,activebackground=mainColor, borderwidth=0, command=lambda: inf.licenses(windows))
lic_btn.place(x=4,y=1)
lic_btntxt = Label(info_licFrame, text="License", bg=mainColor, fg=AC_text)
lic_btntxt.place(x=2,y=45)

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
left_menu.add_command(label='...')
left_menu.add_command(label='Open', command=lambda: getData(True))
left_menu.add_command(label='Refresh', command=RefreshCategory)
left_menu.add_command(label='Add Category', command=addCategory)
left_menu.add_command(label='Delete Category', command=delete_Category)
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
rightframelistbox.config(columns=('id', 'Type', 'usr', 'psw'), show='headings', height=18)
rightframelistbox.heading(0, text='ID')
rightframelistbox.heading(1, text='Type')
rightframelistbox.heading(2, text='Username')
rightframelistbox.heading(3, text='Password')
rightframelistbox.column(0,width=30, anchor='e')
rightframelistbox.column(1, width=150)
rightframelistbox.column(2,width=293)
rightframelistbox.column(3,width=230)
rightframelistbox.pack(side='left', fill='y')

# Scrollbar
rightframelistboxscroll = Scrollbar(rightframelistboxFrame, orient='vertical')
rightframelistboxscroll.pack(side='right', fill='y')

# RIGHT CLICK Functionality for Right Frame
right_menu = Menu(rightframelistbox, tearoff=False)
right_menu.add_command(label='...')
right_menu.add_command(label='View   ', command=view)
right_menu.add_command(label='Delete   ', command=delete_Elements)
right_menu.add_command(label='Refresh   ', command=RefreshValues)
right_menu.add_command(label='Modify Username', command=lambda: modify_Elements('usr'))
right_menu.add_command(label='Modify Password', command=lambda: modify_Elements('psw'))
right_menu.add_separator()
right_menu.add_command(label='Close', command=resetConsole)
rightframelistbox.bind("<Button-3>", rightClick)

#-------------------------------------------------------------------------------------
# END of the program
windows.mainloop()
