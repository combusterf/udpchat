#UDPChat

#TODO:  Create atexit command
#       Make GUI - BAM DONE
#       Make bot
#       Teach bot to love
#       Profit

import socket
import threading
import sys
import os
import time
import UDPFunc
import tkMessageBox
from Tkinter import *
from ChatFns import *
from UDPSettings import *
from UDPFunc import *
from PIL import *
from PIL import ImageTk
import tkHyperlinkManager
import webbrowser
import urllib2
import PIL.Image
import Queue

pubip = urllib2.urlopen('http://ip.42.pl/raw').read()
done = 0
nline = 0
nonl = 0
test = "test"

global display
display = 0

#Writes a log to logs folder in the form 'logYYYY-MM-DD HHMMSS.txt'
#When there is no path, it creates one
if not os.path.exists("./logs"):
    os.makedirs("./logs")
log = open("./logs/log"+time.strftime("%Y-%m-%d %H%M%S")+".txt", 'w')
talk = "Talking with "

class Packet:
    def __init__(self, data, addr):
        self.mData = data
        self.mAddress = addr

global eventqueue
eventqueue = Queue.Queue()

def listen():
    #Main listen loop, QUIT is an event set by either typing /quit or clicking the x
    while not QUIT.isSet():
        #Listener function
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(2048) # buffer size is 2048 bytes
        sock.close()
        # put packets straight on the queue
        print "received: " + data
        packet = Packet(data, addr)
        eventqueue.put(packet)
    return

def handle():
    #print "handler"
    while eventqueue.qsize():
        packet = eventqueue.get(0)
        data = packet.mData
        addr = packet.mAddress
        print "processing: " + data
        #Listener interpreter, runs if QUIT is not set
        if not QUIT.isSet():
            if (data != ""): #checks if message is not blank
                if data[0]!="/": #checks if it is a listener-side command
                    #winsound.PlaySound("*", winsound.SND_ALIAS|winsound.SND_ASYNC)
                    if addr[0] in IP_Lookup: #checks if sender IP is in contacts
                        Name = IP_Lookup[addr[0]]
                        if Name == "192.168.1.1":
                            Name = "localhost"
                        LoadOtherEntry(ChatLog, data, Name) #Displays Message
                        log.write(IP_Lookup[addr[0]]+": "+data+'\n')
                    else:
                        Name = str(addr[0])
                        if Name == "192.168.1.1":
                            Name = "localhost"
                        LoadOtherEntry(ChatLog, data, Name) #Displays Message
                        log.write(str(addr[0])+": "+data+'\n')
                else:
                    #FIX: Update these command outputs
                    if data[1:4]=="new":
                        print data[5:]
                        mesg = UDPFunc._new(data[5:].split(),log)
                        Servermesg(ChatLog, mesg)
                    elif data[1:6]=="color":
                        mesg = UDPFunc._color(data[7:].split(),log)
                        print mesg
                        #Servermesg(ChatLog, mesg)
                    elif data[1:4]=="sys":
                        #Make it display whose computer needs updating
                        Servermesg(ChatLog, addr[0]+": "+data[5:])
                        log.write(data[5:]+'\n')
                    elif data[1:5]=="ping":
                        print addr[0]
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.sendto("/rping", (addr[0], UDP_PORT2))
                        sock.close()
                    elif data[1:6]=="rping":
                        if addr[0] in IP_Lookup:
                            tvar = IP_Lookup[addr[0]]
                        else:
                            tvar = addr[0]
                        Servermesg(ChatLog, tvar+" is online")
                        del(tvar)
                    else:
                        #If it is an unknown command, replies that it didn't work and prints that you likely need a new client
                        Servermesg(ChatLog, "Tried "+data)
                        Servermesg(ChatLog, "Your chat client might need to be updated.")
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.sendto("/sys Command didn't work.", (addr[0], UDP_PORT2))
                        sock.close()
            log.flush()
        del(packet)
    return


def send(EntryText):
        MESSAGE = EntryText
        #ChatLog.insert(END,  ""
        if len(MESSAGE) <= 0:
            pass
        elif (MESSAGE[0]) == "/":
            tlist = MESSAGE[1:].split()
            switch = tlist[0]
            if len(tlist)>1:
                args = tlist[1:]
            else:
                args = []
            if switch=="quit":
                UDPFunc._quit(QUIT)
                log.write("--QUITTING NOW--"+'\n')
                base.quit()
            elif switch=="add":
                mesg = UDPFunc._add(args,log)
                Servermesg(ChatLog, mesg)
            elif switch=="remove":
                mesg = UDPFunc._remove(args,log)
                #print mesg
                #print isinstance(mesg, basestring)
                if isinstance(mesg, basestring) == False:
                    for a in mesg:                             
                        Servermesg(ChatLog, mesg[a])
                        log.write("Removed "+IP_Lookup[a]+'\n')
                else:
                    Servermesg(ChatLog, mesg)
            elif switch=="list":
                b = UDPFunc._list()
                for a in b:
                    if type(a)==tuple:
                        mesg = a[0]+': '+a[1]
                        Servermesg(ChatLog, mesg)
                    else:
                        Servermesg(ChatLog, str(a))
            elif switch=="contacts":
                b = UDPFunc._contacts()
                for a in b:
                    if type(a)==tuple:
                        mesg = a[0]+': '+a[1]
                        Servermesg(ChatLog, mesg)
                    else:
                        Servermesg(ChatLog, str(a))
            elif switch=="?" or switch=="help":
                if len(args)==0:
                    mesg = UDPFunc._help()
                else:
                    mesg = UDPFunc._help(args)
                Servermesg(ChatLog, mesg)
            elif switch=="new":
                mesg = UDPFunc._new(args,log)
                Servermesg(ChatLog, mesg+'\n')
            elif switch=="kill":
                mesg = UDPFunc._kill(args,log)
                Servermesg(ChatLog, mesg+'\n')
            elif switch=="send":
                mesg = UDPFunc._send(args,log)
                Servermesg(ChatLog, mesg+'\n')
            elif switch=="colors":
                b = UDPFunc._colors()
                for a in b:
                    if type(a)==tuple:
                        mesg = a[0]+': '+a[1]
                        Servermesg(ChatLog, mesg)
                    else:
                        Servermesg(ChatLog, str(a))
            elif switch=="color":
                mesg = UDPFunc._color(args,log)
                Servermesg(ChatLog, mesg+'\n')
            elif switch=="mycolor":
                mesg = UDPFunc._mycolor(args,log)
                Servermesg(ChatLog, mesg)
            elif switch=="ping":
                if len(args)==0:
                    mesg = UDPFunc._ping()
                else:
                    mesg = UDPFunc._ping(args)
                Servermesg(ChatLog, mesg)
            elif switch=="iam":
                mesg = UDPFunc._iam(args,log)
                Servermesg(ChatLog, mesg)
            else:
                Servermesg(ChatLog, 'Unknown Command. Commands are:'+UDPFunc.jlist(functions.keys()))
        else:
            for a in UDP_IP2:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(MESSAGE, (a, UDP_PORT2))
                sock.close()
            log.write('\n'+uname[0]+": "+MESSAGE+'\n')
        log.flush()


#import atexit Needs to be implemented
ChatTitle = 'Flagship Group Chat'
WindowTitle = 'Flagship Alpha 1.0.3 v. "LOL WAKARIMASEN"'
def ClickAction():
    global done
    global ChatLog
    global EntryBox
    global LineNumber
    global nline
    global nonl
    if 'FirstRun' in globals():
        global FirstRun
    else:
        FirstRun = 1
    if FirstRun != 0:
        global uname
    #Write message to chat window
    EntryText = FilteredMessage(EntryBox.get("0.0",END))
    if nonl == 0:
        EntryText = EntryText.replace("\n", "")
        print "shit"             
    if 'uname' not in globals():
            with open('UDPSettings.py', 'a') as U_File:
                nameput = "uname = "+'["'+EntryText+'","#808080"]'
                U_File.write(str(nameput)+'\n')
                U_File.write("FirstRun = 0" +'\n')
                EntryBox.delete("0.0",END)
                ChatLog.config(state=DISABLED)
                log.write("Left chat at "+time.strftime("%Y-%m-%d %H:%M:%S")+'\n')
                log.close()
                QUIT.set()
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto("Terminate", ("127.0.0.1", UDP_PORT))
                sock.close()
                base.quit()
                sys.exit()
    if FirstRun == 0:
        client = EntryText
    else:
        EntryBox.delete("0.0",END)
        FirstRun = 0
        return
    EntryBox.delete("0.0",END)
    if done == 1:
        LoadMyEntry(ChatLog, EntryText, uname[0])     
    ChatLog.yview(END)
    if done != 1:               
        if client.lower() == "done":
            EntryText = ""
            done = 1
            tlist = []
            for tvar in UDP_IP2:
                if tvar in IP_Lookup:
                    tlist.append(IP_Lookup[tvar])
                else:
                    tlist.append(tvar)
            talk="Talking with "+UDPFunc.jlist(tlist)
            del(tlist)
            log.write(talk+'.\n')
            Servermesg(ChatLog, talk+'\n')
        elif client.lower() == "all":
            for a in Users:
                EntryText = ""
                UDP_IP2.add(Users[a][0])
                done = 1
                tlist = []
            for tvar in UDP_IP2:
                if tvar in IP_Lookup:
                    tlist.append(IP_Lookup[tvar])
                else:
                    tlist.append(tvar)
            talk="Talking with "+UDPFunc.jlist(tlist)
            del(tlist)
            log.write(talk+'.\n')
            Servermesg(ChatLog, talk+'\n')
        elif client == "/quit":
            base.quit()
        else:
            mesg = UDPFunc._add(client.split(), log)
            Servermesg(ChatLog, mesg)
    if done == 1:
        if nonl == 0:
            EntryText = EntryText.replace("\n", "")
            print "shit"
        nonl = 0
        send(EntryText)
    ChatLog.config(state=DISABLED)
    return
def PressAction(event):
    global nline
    global reset
    EntryBox.config(state=NORMAL)
    if nline == 1:
        global nonl
        print "test2"
        nline = 0
        nonl = 1
        return
    else:
        EntryBox.bind("<Return>", DisableEntry)
        ClickAction()
    
def DisableEntry(event):
    EntryBox.config(state=DISABLED)
def newline(null):
    global nline
    print "test"
    EntryBox.insert(END, '')
    nline = 1
    return
def handler():
    result = tkMessageBox.askokcancel("Exit Flagship?", "Do you really want to use the escape pod?", icon = 'warning')
    print result
    if result == True:
        log.write("Left chat at "+time.strftime("%Y-%m-%d %H:%M:%S")+'\n')
        log.close()
        QUIT.set()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("Terminate", ("127.0.0.1", UDP_PORT))
        sock.close()
        base.quit()
        sys.exit()


def shit():
    print "Button Pressed."

def newgchat():
    global pubip
    global SendButton
    global EntryBox
    global ChatLog
    global scrollbar
    global uname
    gchat = Tk()
    gchat.title(ChatTitle) 
    gchat.geometry("400x500")
    gchat.resizable(width=TRUE, height=TRUE)
    if "nt" == os.name:
        gchat.iconbitmap(bitmap = 'iconfile.ico')
    else:
        gchat.iconbitmap(bitmap = '@iconfile.xbm')
    
    #Create the Button to send message
    SendButton = Button(gchat, font=30, text="Send", width="12", height=5,
                        bd=0, bg="#FFBF00", activebackground="#FACC2E",
                        command=ClickAction)
    
    #Create the box to enter message
    EntryBox = Text(gchat, bd=0, bg="white",width="29", height="5", font="Arial")
    EntryBox.bind("<Control-Return>", newline)
    EntryBox.bind("<Shift-Return>", newline)
    
    EntryBox.bind("<KeyRelease-Return>", PressAction)
    pubip = pubip.replace('[', "")
    pubip = pubip.replace("'", "")
    pubip = pubip.replace(']', "")
    #Create a Chat window
    if 'uname' in globals():
        ChatLog = Text(gchat, bd=0, bg="white", height="8", width="50", font="Arial",)
        ChatLog.insert(END, "This is your public IP: "+pubip+'\n'+'\n')
        ChatLog.insert(END, "Welcome "+uname[0]+'\n'+'\n')
        for a in Users.keys():
            ChatLog.insert(END,  a +": "+ Users[a][0]+'\n')
        ChatLog.insert(END, '\n'+"Who would you like to talk to? (Type all for everyone)"+'\n'+'\n')
        ChatLog.insert(END, "----Type done when finished----"+'\n'+'\n')
        ChatLog.config(state=DISABLED)
    else:
        ChatLog = Text(gchat, bd=0, bg="white", height="8", width="50", font="Arial",)
        ChatLog.insert(END, "Please Enter Your Name:"+'\n')
        ChatLog.insert(END, "Then, please re-open Flagship after it closes.")

    #Bind a scrollbar to the Chat window
    scrollbar = Scrollbar(gchat, command=ChatLog.yview, cursor="heart")
    ChatLog['yscrollcommand'] = scrollbar.set

    #Place all components on the screen
    scrollbar.place(x=376,y=6, height=386)
    ChatLog.place(x=6,y=6, height=386, width=370)
    EntryBox.place(x=128, y=401, height=90, width=265)
    SendButton.place(x=6, y=401, height=90)

    

    gchat.mainloop()

def func(val):
    global test
    global display
    if val == "Contact List" and display!=1:
        display = 1
        print "Contact List selected."
        #test = test + '\n' + test
        base.geometry("400x400")
        CList = Text(base, bd=0, bg="white", font="Arial",)
        CList.insert(END, test)
        CList.config(state=DISABLED)
        CList.place(x=6, y=35, width=350, height=350)

        """
        file_in = 'testimg.jpg'
        pil_image = PIL.Image.open(file_in)
        image50x50 = pil_image.resize((50, 50))
        file_out = 'temp.jpg'
        image50x50.save(file_out)
        tk_image2 = ImageTk.PhotoImage(image50x50)
        label2 = Label(CList,image=tk_image2)
        label2.pack(padx=5, pady=5)
        """

        
        photo = PhotoImage(file="temp.gif")
        label = Label(CList, image = photo)
        label.image = photo
        label.pack(side=RIGHT)

        
    elif val == "Directory Tree" and display !=2:
        display = 2
        print "Directory Tree selected."
    elif val == "Tool Chest" and display !=3:
        display = 3
        print "Tool Chest selected."
        base.geometry("400x400")
        toolbox = Frame(base)
        b = Button(toolbox, text="Dice Roller", width=10, command=shit)
        b.pack(side=LEFT)
        toolbox.pack(side=BOTTOM, fill=X)



    elif val == "Group List" and display!=4:
        display = 4
        print "Group List selected."

    else:
        print "Already displaying that."



#---------------------------------------------------#
#-----------------GRAPHICS MANAGEMENT---------------#
#---------------------------------------------------#



#Create a window
base = Tk()
base.title(WindowTitle)
base.geometry("400x40")
base.resizable(width=TRUE, height=TRUE)
if "nt" == os.name:
    base.iconbitmap(bitmap = 'iconfile.ico')
else:
    base.iconbitmap(bitmap = '@iconfile.xbm')

QUIT=threading.Event()
QUIT.clear()

# create event handler
def pollingloop():
    global QUIT
    handle()
    if not QUIT.isSet():
        base.after(100, pollingloop)

base.after(100, pollingloop)



menubar = Menu(base)

#all menus

filemenu = Menu(menubar, tearoff=1)
editmenu = Menu(menubar, tearoff=1)
formatmenu = Menu(menubar, tearoff=1)
contactsmenu = Menu(menubar, tearoff=1)
viewmenu = Menu(menubar, tearoff=1)
addcontactmenu = Menu(contactsmenu, tearoff=1)

#Menu Bar items

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Contacts", menu=contactsmenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="Format", menu=formatmenu)
menubar.add_cascade(label="View", menu=viewmenu)

#File Menu items

filemenu.add_command(label="Online Status") # "Online", "Do Not Disturb", "Invisible", "Away"
filemenu.add_command(label="Ping Room") # command=UDPFunc._ping
filemenu.add_separator()
filemenu.add_command(label="Exit Flagship", command=handler)

#Edit Menu items

editmenu.add_command(label="My Picture") # Change and edit your display picture.
editmenu.add_command(label="My Profile") # Profile Editor - change public profile.
editmenu.add_command(label="My Post Defaults") # Adjust settings for posting defaults.
editmenu.add_command(label="My Preferences") # Adjust client-side settings.

#Format Menu items

formatmenu.add_command(label="Fonts") #import, remove, and change font settings
formatmenu.add_command(label="Change my color")
formatmenu.add_command(label="Change friend color") # Enter friend name, enter desired hex value, profit

#Contacts Menu items

contactsmenu.add_cascade(label="Add Contact", menu=addcontactmenu) # Cascade menu, to allow for multiple methods of adding new contacts.
contactsmenu.add_command(label="Remove Contact") # Enter user ID to remove them from contact list - entering ID not in contact list returns prompt.
contactsmenu.add_command(label="Import Contacts...") #Imports contacts from *.fsc file.
contactsmenu.add_command(label="Export Contacts...") #Exports contacts to *.fsc file.
contactsmenu.add_command(label="Start New Private Chat") #begins IM with one selected user.
contactsmenu.add_command(label="Create New Group") # Opens new group chat window.
contactsmenu.add_command(label="Join Existing Group...") # Enter Group ID to join existing group.

#View Menu items

viewmenu.add_command(label="Image Viewer") # View images from database. BASIC VIEWER. NO EDITING CAPABILITY. Not streamed publically.
viewmenu.add_command(label="Object Viewer") # View 3D models from databasewith basic zoom and rotation controls. Not streamed publically.
viewmenu.add_command(label="Text Viewer") # View text files from database in read-only. Not streamed publically.

#Add Contact submenu items

addcontactmenu.add_command(label="Add Individual") # Add a contact via username, IP, e-mail, or other unique ID.
addcontactmenu.add_command(label="Add from Skype") # Import contacts from your Skype friend list.
addcontactmenu.add_command(label="Add from Facebook") 

base.config(menu=menubar)

toolbar = Frame(base)

#b = Button(toolbar, text="Add Contact", width=10, command=shit)
#b.pack(side=LEFT, padx=2, pady=2)

b = Button(toolbar, text="New Group", width=8, command=newgchat)
b.pack(side=LEFT, padx=2, pady=2)

#b = Button(toolbar, text="Join Group", width=9, command=shit)
#b.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

#Option Dropdown Menu

test123 = StringVar()
w = OptionMenu(toolbar, test123, "Contact List", "Group List", "Directory Tree", "Tool Chest", command=func)
w.pack(side=TOP, padx=2, pady=2)



base.protocol("WM_DELETE_WINDOW", handler)



l=threading.Thread(target=listen)
#s=threading.Thread(target=send)
# set thread to daemon ('ok' won't be ChatLog.insert(END, ed in this case)
l.start()
#s.start()
base.mainloop()

        
while l.isAlive():
    pass
log.write("Left chat at "+time.strftime("%Y-%m-%d %H:%M:%S")+'\n')
log.close()
base.quit()
sys.exit()
