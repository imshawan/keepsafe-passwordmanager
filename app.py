import base64, sys
import handle_db
from tkinter import *
import tkinter as tk
import icons_base64 as sm
from tkinter import messagebox
from tkinter import ttk

keepsafe_ico = sm.MAIN_ICOTXT
addbutton = sm.ICO_ADD
modifybtn = sm.ICO_MODIFY
deletebtn = sm.ICO_DEL
infobtn = sm.ICO_INFO
closebtn = sm.ICO_CLOSE

height=610 
width=805
bars = 'grey'
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
B = Frame(root, height=25, width=width, bg=bars)
B.place(x=0, y=height-25)


def getICONS(icon):
    base64_img_bytes = icon.encode('utf-8')
    decoded_image_data = base64.decodebytes(base64_img_bytes)
    ico = PhotoImage(data=decoded_image_data)
    return ico

def close():
    sys.exit()

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
leftframe = Frame(root, height=507, width=230)
leftframe.place(x=0, y=80)
# Listbox Frame
G = Frame(leftframe, height=27, width=230, bg=bars)
G.place(x=0,y=0)
#leftframelistboxText = Label(leftframe, text='All Items', font=('Franklin Gothic Medium', 12))
#leftframelistboxText.place(x=50,y=50)
leftframelistboxFrame = Frame(leftframe, height=425, width=222)
leftframelistboxFrame.place(x=0, y=90)
# ListBox
leftframelistbox = Listbox(leftframelistboxFrame, height=26, width=34, borderwidth=0, bg='#f0f0f0')
leftframelistbox.pack(side='left', fill='y')
# Scrollbar
leftframelistboxscroll = Scrollbar(leftframelistboxFrame, orient='vertical')
leftframelistboxscroll.pack(side='right', fill='y')

#-------------------------------------------------------------------------------------
# Right Frame
rightframe = Frame(root, height=508, width=width-232, bg='grey')
rightframe.place(x=230, y=80)
# Listbox Frame
rightframelistboxFrame = Frame(rightframe, height=500, width=width-232)
rightframelistboxFrame.place(x=0, y=27)
# ListBox
rightframelistbox = Listbox(rightframelistboxFrame, height=30, width=92, borderwidth=0, bg='#f0f0f0')
rightframelistbox.pack(side='left', fill='y')
# Scrollbar
rightframelistboxscroll = Scrollbar(rightframelistboxFrame, orient='vertical')
rightframelistboxscroll.pack(side='right', fill='y')


windows.mainloop()
