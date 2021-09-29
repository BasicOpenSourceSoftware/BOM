#BasicOpenMacro#
#This macro was made by BasicOpenSourceSoftware to be as basic as can be#
#Check me out on GitHub#

import win32api
import win32com.client
import win32con
import time
import json
import os
import threading

#----Create the varibles----#

typetoscreen = win32com.client.Dispatch("WScript.Shell")

ctrlpressed=0
altpressed=0
keyindict = ''
#keyalt = win32con.VK_MENU
#keyctrl = win32con.VK_CONTROL
savereload = False
#value=''

key2text = {'H': 'Hello','R': 'Goodbye'}
#keystowatch = {1: 'H'}

filesavefolder = os.getenv('LOCALAPPDATA')+"\\BasicOpenSourceSoftware\\BasicOpenMacro"
filenameandloc = filesavefolder+"\\SavedBinds.boss"
#textfilename = filesavefolder+"\\SavedText.boss"
#----Get Keybinds and Text from file----#
    #--get keybinds from file--#
def readfiles():
    global key2text
    if os.path.exists(filenameandloc):
        try:
            with open(filenameandloc) as f:
                data = f.read()
            key2text=json.loads(data)
            print('Keybinds file was found and read')
            print(key2text)

        except:
            print("Keybinds file is empty")
            key2text.clear()

    else:
        os.makedirs(filesavefolder)
        f = open(filenameandloc,"w")
        f.close()
        print("Keybinds file now exsists")

def savefiles():
    with open(filenameandloc, 'w') as convert_file:
        convert_file.write(json.dumps(key2text))
        print('saved')

#----Do on input----#
def wegotinput(keyindict):
    print("Keybinds have been pressed "+ keyindict)
    '''
    In here use the keyindict to get the value and then use #typetoscreen.SendKeys(keyindict.getvalue) to type it
    '''

#----Wait for input----#
def ctrlalt():
    while True:
        global ctrlpressed
        global altpressed
        ctrlpressed = win32api.GetAsyncKeyState(win32con.VK_CONTROL)
        altpressed = win32api.GetAsyncKeyState(win32con.VK_MENU)
        time.sleep(0.015)
        #print(ctrlpressed)
        if savereload:
            raise SystemExit
        
def watchforkeypress(keyindict):
    while True:
        #print("yourkeyis"+keyindict)
        state1 = win32api.GetAsyncKeyState(ord(keyindict)) #this is all the set keys
        time.sleep(0.015)
        #print (ctrlpressed)
        if ctrlpressed != 0 and altpressed != 0 and state1 !=0:
            print ("hey you got here")
            wegotinput(keyindict)
            time.sleep(0.5)
            
            #time.sleep(1)
        if savereload == True:
            raise SystemExit
            #reloadtime()

#----Threads and which keys are bound----#

def threadmaker():
    x=threading.Thread(target=ctrlalt)
    x.start()
    
    for key, keyindict in key2text.items():
        keyindict=key
        print(keyindict)
        x=threading.Thread(target=watchforkeypress, args=[keyindict],)
        x.start()

#----Save Reload and exit----#
def checkifreload(x):
    while x=0:
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
    

#----Add to directory/keybinds----#

def keybindadded():
    global key2text
    print('not setup yet')

#----Window making part----#



#----Start the program here----#

readfiles()
print(key2text)
