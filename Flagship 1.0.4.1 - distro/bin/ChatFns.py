#ChatFns

from Tkinter import *
from socket import *
import urllib
import re
import socket
import threading
import sys
import os
import time
import UDPFunc
from ChatFns import *
from UDPSettings import *
import tkHyperlinkManager
import webbrowser


def kickassfunc(EntryText, ChatLog, Name):
    global LineNumber
    hyperlink = tkHyperlinkManager.HyperlinkManager(ChatLog)
    ln1 = 0
    ln1 = len(Name)
    ln1 = 0.1 * ln1
    print ChatLog
    EntryText = EntryText.split()
    pos = [ i for i, word in enumerate(EntryText) if word.startswith('http') ]
    http = EntryText[pos[0]]

    illi = 0
    if "," in http:
        print "EntryText"
        http = http.replace(',', '')
        illi = 1
    part1 = EntryText[0:pos[0]]
    p1=""
    p2=""
    for a in part1:
        p1 = p1+a+" "
    part2 = EntryText[pos[0]+1:]
    for a in part2:
        p2 = p2+a+" "
    if illi != 1:
        ChatLog.insert(END, Name + ": " + str(p1)) , 
        ChatLog.insert(INSERT, http, hyperlink.add(lambda:callback(http), http))
        ChatLog.insert(INSERT, " " + p2 + '\n')
        ChatLog.tag_add(Name, LineNumber, LineNumber+ln1)
        if Name in Users:
            ChatLog.tag_config(Name, foreground=Users[Name][1], font=("Arial", 12, "bold"))
        else:
            ChatLog.tag_config(Name, foreground="#04B404", font=("Arial", 12, "bold"))
        ChatLog.yview(END)
    else:
        ChatLog.insert(END, Name + ": " + str(p1)) , 
        ChatLog.insert(INSERT, http, hyperlink.add(lambda:callback(http), http))
        ChatLog.insert(INSERT, ", " + p2 + '\n')
        ChatLog.tag_add(Name, LineNumber, LineNumber+ln1)
        if Name in Users:
            ChatLog.tag_config(Name, foreground=Users[Name][1], font=("Arial", 12, "bold"))
        else:
            ChatLog.tag_config(Name, foreground="#04B404", font=("Arial", 12, "bold"))
        ChatLog.yview(END)
    return

def kickassfunc2(EntryText, ChatLog, name):
    global LineNumber
    hyperlink = tkHyperlinkManager.HyperlinkManager(ChatLog)
    ln2 = len(name)
    ln2 = 0.1 * ln2
    LineNumber = float(ChatLog.index('end'))-1.0
    print ChatLog
    EntryText = EntryText.split()
    pos = [ i for i, word in enumerate(EntryText) if word.startswith('http') ]
    http = EntryText[pos[0]]
    illi = 0
    if "," in http:
        print "EntryText"
        http = http.replace(',', '')
        illi = 1
    part1 = EntryText[0:pos[0]]
    p1=""
    p2=""
    for a in part1:
        p1 = p1+a+" "
    part2 = EntryText[pos[0]+1:]
    for a in part2:
        p2 = p2+a+" "
    if illi != 1:
        ChatLog.insert(END, name + ": " + str(p1)) , 
        ChatLog.insert(INSERT, http, hyperlink.add(lambda:callback(http), http))
        ChatLog.insert(INSERT, " " + p2 + '\n')
        ChatLog.tag_add(name, LineNumber, LineNumber+ln2)
        ChatLog.tag_config(name, foreground=uname[1], font=("Arial", 12, "bold"))
        ChatLog.yview(END)
    else:
        ChatLog.insert(END, name + ": " + str(p1)) , 
        ChatLog.insert(INSERT, http, hyperlink.add(lambda:callback(http), http))
        ChatLog.insert(INSERT, ", " + p2 + '\n')
        ChatLog.tag_add(name, LineNumber, LineNumber+ln2)
        ChatLog.tag_config(name, foreground=uname[1], font=("Arial", 12, "bold"))
        ChatLog.yview(END)
    return 

def callback(url):
    webbrowser.open(url)
    
def FlashMyWindow(title):
    ID = win32gui.FindWindow(None, title)
    win32gui.FlashWindow(ID,True)

def FlashMyWindow2(title2):
    ID2 = win32gui.FindWindow(None, title2)
    win32gui.FlashWindow(ID2,True)    

def GetExternalIP():
    url = "http://checkip.dyndns.org"
    request = urllib.urlopen(url).read()
    return str(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request))

def GetInternalIP():
    return str(gethostbyname(getfqdn()))
    
def FilteredMessage(EntryText):
    """
    Filter out all useless white lines at the end of a string,
    returns a new, beautifully filtered string.
    """
    EndFiltered = ''
    for i in range(len(EntryText)-1,-1,-1):
        if EntryText[i]!='\n':
            EndFiltered = EntryText[0:i+1]
            break
    for i in range(0,len(EndFiltered), 1):
            if EndFiltered[i] != "\n":
                    return EndFiltered[i:]+'\n'
    return ''
	
def LoadConnectionInfo(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            ChatLog.insert(END, EntryText+'\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

def LoadMyEntry(ChatLog, EntryText, name):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            ln2 = len(name)
            ln2 = 0.1 * ln2
            if "http" not in EntryText:
                LineNumber = float(ChatLog.index('end'))-1.0
                ChatLog.insert(END, name + ": " + EntryText + '\n')
                ChatLog.tag_add(name, LineNumber, LineNumber+ln2)
                ChatLog.tag_config(name, foreground=uname[1], font=("Arial", 12, "bold"))
                ChatLog.yview(END)
            else:
                EntryText = str(EntryText)
                kickassfunc2(EntryText, ChatLog, name)


def LoadOtherEntry(ChatLog, EntryText, Name):
    global LineNumber
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if "http" not in EntryText:
            if ChatLog.index('end') != None:
                try:
                    LineNumber = float(ChatLog.index('end'))-1.0
                except:
                    pass
                ln1 = 0
                ln1 = len(Name)
                ln1 = 0.1 * ln1
                print ln1
                print LineNumber
                if Name == "localhost" or Name == "Localhost":
                    ChatLog.insert(END, Name + ': ' + EntryText + '\n')
                    ChatLog.tag_add(Name, LineNumber, LineNumber+ln1)
                    ChatLog.tag_config(Name, foreground=Users[Users_l['localhost']][1], font=("Arial", 12, "bold"))
                    
                    ChatLog.yview(END)
                else:
                    ChatLog.insert(END, Name + ': ' + EntryText + '\n')
                    ChatLog.tag_add(Name, LineNumber, LineNumber+ln1)
                    if Name in Users:
                        ChatLog.tag_config(Name, foreground=Users[Name][1], font=("Arial", 12, "bold"))
                    else:
                        ChatLog.tag_config(Name, foreground="#04B404", font=("Arial", 12, "bold"))
                    ChatLog.yview(END)
        else:
             if ChatLog.index('end') != None:
                try:
                    LineNumber = float(ChatLog.index('end'))-1.0
                except:
                    pass
                EntryText = str(EntryText)
                kickassfunc(EntryText, ChatLog, Name)
                
def Servermesg(ChatLog, EntryText):
    if EntryText != '':
        ChatLog.config(state=NORMAL)
        if ChatLog.index('end') != None:
            try:
                LineNumber = float(ChatLog.index('end'))-1.0
            except:
                pass
            ChatLog.insert(END, EntryText+'\n')
            
            ChatLog.yview(END)
            
