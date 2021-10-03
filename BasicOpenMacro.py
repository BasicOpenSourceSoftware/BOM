#BasicOpenMacro#
#This macro was made by BasicOpenSourceSoftware to be as basic as can be#
#Check me out on GitHub#

import tkinter.scrolledtext as scrolledtext
from tkinter import *
from tkinter import messagebox
import win32api
import win32com.client
import win32con
import time
import json
import os
import threading

root = Tk()

#----Create the varibles----#

typetoscreen = win32com.client.Dispatch("WScript.Shell")
ctrlpressed=0
altpressed=0
keyindict = ''
savereload = False
key2text = {'H': 'Hello','R': 'Goodbye'}
filesavefolder = os.getenv('LOCALAPPDATA')+"\\BasicOpenSourceSoftware\\BasicOpenMacro"
filenameandloc = filesavefolder+"\\SavedBinds.boss"
xa=0
startvar=0

#user set vars#
typedelay = 0.3
newbind = ''
newtext = ''
typedelayentry=StringVar()
typedelayentry2=0.3

#Window vars#
winwidth=800
winheight=400
winheiwid=str(winwidth)+'x'+str(winheight)
textsetvar=StringVar()
bindsetvar=StringVar()
textboxtextofdict=''

bindtextdisplay = scrolledtext.ScrolledText(root, wrap="none")

#----Get Keybinds and Text from file----#

def readfiles():
    global key2text
    if os.path.exists(filenameandloc):
        try:
            with open(filenameandloc) as f:
                data = f.read()
            key2text=json.loads(data)
            print('Keybinds file was found and read')
        except:
            print("Keybinds file is empty")
            key2text.clear()

    else:
        try:
            os.makedirs(filesavefolder)
        except:
            print('Making folder failed')
        f = open(filenameandloc,"w")
        f.close()
        print("Keybinds file now exsists")

def savefiles():
    with open(filenameandloc, 'w') as convert_file:
        convert_file.write(json.dumps(key2text))
        print('saved')

#----Do on input----#
def wegotinput(keyindict):
    global typedelay
    valu=key2text.get(keyindict)
    time.sleep(typedelay)
    try:
        typetoscreen.SendKeys(valu)
    except:
        print('The '+keyindict+' key does not have a bind.')

#----Wait for input----#
def ctrlalt():
    while True:
        global ctrlpressed
        global altpressed
        ctrlpressed = win32api.GetAsyncKeyState(win32con.VK_CONTROL)
        altpressed = win32api.GetAsyncKeyState(win32con.VK_MENU)
        time.sleep(0.015)
        if savereload == True:
            raise SystemExit
        
def watchforkeypress(keyindict):
    while True:
        state1 = win32api.GetAsyncKeyState(ord(keyindict)) #this is all the set keys
        time.sleep(0.015)
        if ctrlpressed != 0 and altpressed != 0 and state1 !=0:
            wegotinput(keyindict)
            time.sleep(0.5)
        if savereload == True:
            raise SystemExit

#----Threads and which keys are bound----#

def threadmaker():
    global savereload
    savereload=False
    x=threading.Thread(target=ctrlalt)
    x.start()
    for key, keyindict in key2text.items():
        keyindict=key
        x=threading.Thread(target=watchforkeypress, args=[keyindict],)
        x.start()

#----Save Reload and exit----#
def checkifreload(x):
    while x==0:
        if savereload==True:
            reloadtime()

def reloadtime():
    time.sleep(0.5)
    readfiles()
    threadmaker()

def savetime():
    savefiles()
    global savereload
    savereload=True
    reloadtime()

def exittime():
    raise SystemExit
    time.sleep(0.2)

def onclosing():
    global savereload
    savereload=True
    root.destroy()
    raise SystemExit
    

#----Add/remove to directory/keybinds----#

def putthekeystogether(ke,va):
    global textboxtextofdict
    global xa
    if xa==0:
        textboxtextofdict=textboxtextofdict+ke+'-->'+va
        xa=1
    else:
        textboxtextofdict=textboxtextofdict+'\n'+ke+'-->'+va

def displaykeybindstotextbox():
    global textboxtextofdict
    global xa
    bindtextdisplay.config(state='normal')
    for ke,va in key2text.items():
        putthekeystogether(ke,va)
    bindtextdisplay.delete(1.0,END)
    bindtextdisplay.insert(1.0,textboxtextofdict)
    textboxtextofdict=''
    xa=0
    bindtextdisplay.config(state='disabled')

def addingbindsandtext():
    global key2text
    global newbind
    global newtext
    global startvar
    newbind=bindsetvar.get()
    newtext=textsetvar.get()
    if newtext!='' and newbind!='' or startvar==0:
        if startvar==1:
            key2text[newbind]=newtext
        displaykeybindstotextbox()
        startvar=1
    else:
        print('Nothing in fields')

def deletekeybind():
    global key2text
    newbind=bindsetvar.get()
    try:
        del key2text[newbind]
        displaykeybindstotextbox()
    except:
        print(newbind+' Keybind does not exsist.')

#----Options----#

def setdelay():
    global typedelay
    typedelayentry=delayseter.get()
    typedelay=float(typedelayentry)

def helppopup():
    messagebox.showinfo('Help','For documentation please vist: https://github.com/BasicOpenSourceSoftware/BOM')

#----Window and widget making part----#
def windowmaker():
    global bindtextdisplay
    
    root.wm_title("BasicOpenMacro")
    root.resizable(0, 0)
    root.geometry(winheiwid)
    #root.pack_propagate(False)
    
    #bindtextdisplay = scrolledtext.ScrolledText(root, wrap="none")
    bindtextdisplay['font'] = ('calibre', '12')
    bindtextdisplay.pack(expand=True, fill='both')
    bindtextdisplay.place(x=120,y=5,width=655,height=355, in_=root)
    bindtextdisplay.insert(1.0,"testing")
    bindtextdisplay.config(state=NORMAL)
    #bindtextdisplay.config(state='disabled')


    bindset = Entry(root,textvariable = bindsetvar)
    bindset['font'] = ('calibre', '12')
    bindset.pack(expand=True, fill='both')
    bindset.place(x=120,y=370, width=20,height=25, in_=root)

    textset = Entry(root,textvariable = textsetvar)
    textset['font'] = ('calibre', '12')
    textset.pack(expand=True, fill='both')
    textset.place(x=155,y=370,width=620,height=25, in_=root)
    
    startbutton=Button(root,text = 'Start', command=threadmaker, font = ('calibre',18))
    startbutton.place(x=5,y=5,width=100,height=100, in_=root)
    
    savebutton=Button(root,text = 'Save', command=savetime, font = ('calibre',18))
    savebutton.place(x=5,y=110,width=100,height=100, in_=root)
    
    delaybutton=Button(root, text='Set Delay', command=setdelay, font = ('calibre',12))
    delaybutton.place(x=5,y=215,width=100,height=25, in_=root)
    
    delayseter = Entry(root)#,textvariable = typedelayentry
    delayseter['font'] = ('calibre', '12')
    delayseter.pack(expand=True, fill='both')
    delayseter.place(x=5,y=240,width=100,height=25, in_=root)
    
    helpbutton=Button(root,text = '?', command=helppopup, font = ('calibre',18))
    helpbutton.place(x=5,y=270,width=100,height=65, in_=root)
    
    removebindbutton=Button(root,text = 'Remove Bind', command=deletekeybind, font = ('calibre',12))
    removebindbutton.place(x=5,y=340,width=100,height=25, in_=root)
    
    addbutton=Button(root,text = 'Add Bind', command=addingbindsandtext, font = ('calibre',12))
    addbutton.place(x=5,y=370,width=100,height=25, in_=root)
    root.mainloop()
#textset.see('end')
#def otherthread():
    #root.mainloop()
#x=threading.Thread(target=otherthread())
#x.start()
#----Start the program here----#

readfiles()
addingbindsandtext()
root.protocol("WM_DELETE_WINDOW", onclosing)
windowmaker()
