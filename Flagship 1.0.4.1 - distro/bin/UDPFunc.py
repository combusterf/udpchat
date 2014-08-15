#UDPFunc

import socket
import os
from Tkinter import *
from socket import *
import urllib
import re
import win32gui
import socket
import threading
import sys
import os
import winsound
import time
from ChatFns import *
from UDPSettings import *

def jlist(_list):
    b = 1
    c = len(_list)
    output = ""
    for a in _list:
        if b==c and b!=1:
            output=output+" and"
        output=output+" "+a
        if b!=c and c>2:
            output=output+","
        b+=1
    output = output[1:]
    return output
        
def _quit(QUIT):
    QUIT.set()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto("Terminate", ("127.0.0.1", UDP_PORT))
    sock.close()
def _add(_list, log):
    mesg="No Valid IPs"
    added = set([])
    for user in _list:
        if user.lower() in Users_l:
            UDP_IP2.add(Users[Users_l[user.lower()]][0])
            added.add(Users_l[user.lower()])
        elif user == "all":
            for a in Users:
                UDP_IP2.add(Users[a][0])
                added.add(a)
        else:
            iptest = user
            err = 0
            try:
                socket.inet_aton(iptest)
            except:
                mesg = "No valid IPs"
                err = 1
            if (err == 1):
                pass
            else:
                UDP_IP2.add(user)
                added.add(user)
    if len(added)!=0:
        mesg = "Added "+jlist(added)
    if len(mesg)!=0:
        log.write(mesg+'\n')
    return mesg
def _remove(_list, log):
    removed = set([])
    notin = set([])
    for user in _list:
        if user=="all":
            x=set(UDP_IP2)
            for a in x:
                UDP_IP2.remove(a)
                if a in IP_Lookup:
                    removed.add(IP_Lookup[a])
                else:
                    removed.add(a)
            del(x)
        elif user.lower() in Users_l and Users[Users_l[user.lower()]][0] in UDP_IP2:
            UDP_IP2.remove(Users[Users_l[user.lower()]][0])
            removed.add(Users_l[user.lower()])
        elif user in UDP_IP2:
            UDP_IP2.remove(user)
            removed.add(user)
        else:
            notin.add(user)
    mesg = ""
    if len(removed)!=0:
        mesg = "Removed "+jlist(removed)+' from conversation.'
    if len(notin)!=0:
        mesg = mesg+'\n'+jlist(notin)+" were not in conversation."
    if len(mesg)!=0:
        if log:
            log.write(mesg+'\n')
        print mesg
        return mesg
    else:
        return "Nobody Removed."
def _list():
    tlist = []
    for a in UDP_IP2:
        if a in IP_Lookup:
            tlist.append((IP_Lookup[a], a))
        else:
            tlist.append(a)
    return tlist
def _contacts():
    tlist = []
    for a in Users:
        if Users[a][0] not in UDP_IP2:
            tlist.append((a, Users[a][0]))
    return tlist
def _help(_list=['all']):
    rhelp = []
    for switch in _list:
        if switch == 'all':
            rhelp.append("Commands:"+jlist(functions.keys())+'.\n')
        elif switch in functions.keys():
            rhelp.append(str(switch)+": "+functions[switch]+'\n')
        else:
            rhelp.append(str(switch)+" is an Unknown Command. Commands are:"+jlist(functions.keys())+'.\n')
    mesg = ""
    for a in rhelp:
        mesg = mesg+a
    mesg = mesg[:-1]
    return mesg
def _new(_list, log=None):
    if len(_list)==2:
        [a,c] = _list[0:2]
        color = "#04B404"
    elif len(_list)==3:
        [a,c,color]=_list[0:3]
    else:
        return "Improper Syntax."
    print a
    print c
    if a.lower() not in Users_l and c not in IP_Lookup:
        Users[a]=(c,color)
        Users_l[a.lower()]=a
        IP_Lookup[c]=a
        with open('users.cfg', 'a') as U_File:
            U_File.write(str((a,(c,color)))+'\n')
        mesg = "Added "+a+" to contacts."
        if log:
            log.write("Added "+a+" to contacts.\n")
    elif c in IP_Lookup:
        del Users[IP_Lookup[c]]
        del Users_l[IP_Lookup[c].lower()]
        Users[a]=(c,color)
        Users_l[a.lower()]=a
        oldname = str(IP_Lookup[c])
        IP_Lookup[c]=a
        with open('userstemp.cfg', 'w') as U_File:
            for d in Users.items():
                U_File.write(str(d)+'\n')
        os.remove('users.cfg')
        with open('users.cfg', 'w') as U_File:
            for d in Users.items():
                U_File.write(str(d)+'\n')
        mesg = "Changed "+oldname+"'s name to "+a
        if log:
            log.write("Changed "+oldname+"'s name to "+a+'\n')
        del oldname
    else:
        UDP_IP2.remove(Users[a][0])
        del IP_Lookup[Users[a]][0]
        IP_Lookup[c]=a
        Users[a]=(c,color)
        Users_l[a.lower()]=a
        with open('userstemp.cfg', 'w') as U_File:
            for d in Users.items():
                U_File.write(str(d)+'\n')
        os.remove('users.cfg')
        with open('users.cfg', 'w') as U_File:
            for d in Users.items():
                U_File.write(str(d)+'\n')
        mesg = "Changed "+a+"'s IP to "+c
        if log:
            log.write("Changed "+a+"'s IP to "+c+'\n')
    UDP_IP2.add(c)
    if uname[0].lower()==a.lower():
        _remove([a],log)
    print mesg
    return mesg
def _kill(_list, log):
    killed = set([])
    for user in _list:
        if user.lower() in Users_l:
            if Users[Users_l[user.lower()]][0] in UDP_IP2:
                UDP_IP2.remove(Users[Users_l[user]][0])
            if Users[Users_l[user.lower()]][0] in IP_Lookup:
                del IP_Lookup[Users[user][0]]
            del Users[Users_l[user.lower()]]
            del Users_l[user.lower()]
            with open('userstemp.cfg', 'w') as U_File:
                for d in Users.items():
                    U_File.write(str(d)+'\n')
            os.remove('users.cfg')
            with open('users.cfg', 'w') as U_File:
                for d in Users.items():
                    U_File.write(str(d)+'\n')
            killed.add(user)
        elif user in UDP_IP2:
            UDP_IP2.remove(user)
            killed.add(user)
        else:
            pass
    mesg = "Removed "+jlist(killed)+" from contacts and conversation."
    return mesg
def _send(user, log):
    word = ""
    for a in user.split():
        word = word+" "+a    
    x = set(UDP_IP2)
    for a in x:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("/new"+word, (a, UDP_PORT2))
        sock.close()
    del x
    return "Sent "+user[0]+" to everyone"
def _color(_list, log):
    if len(_list)==2:
        [a,c] = _list[0:2]
    else:
        return "Improper Syntax."
    if a.lower() == 'me':
        if c in colors:
            uname[1]=colors[c]
        elif c[0]!='#':
            c='#'+c
            uname[1]=c
        elif c[0]=='#':
            uname[1]=c
        else:
            return "Improper Syntax."
        print "..........wut."
        with open("UDPSettings.py","r") as U_File:
            with open("USettemp.txt","w+") as U2:
                for line in U_File:
                    b = re.sub('uname\s?=\s?\[".*",\s?".*"\]',r'uname = ["'+uname[0]+'","'+uname[1]+'"]',line)
                    U2.write(b)
        with open("USettemp.txt","r") as U_File:
            with open("UDPSettings.py","w+") as U2:
                for line in U_File:
                    U2.write(line)
        os.remove('USettemp.txt')
        return "Changed color to "+c
    elif a.lower() in Users_l and c in colors:
        Users[Users_l[a.lower()]]=(Users[Users_l[a.lower()]][0],colors[c])
        with open('userstemp.cfg', 'w') as U_File:
            for d in Users.items():
                U_File.write(str(d)+'\n')
        os.remove('users.cfg')
        with open('users.cfg', 'w') as U_File:
            for d in Users.items():
                U_File.write(str(d)+'\n')
        mesg = "Changed "+a+"'s color to "+c
    elif a.lower() in Users_l:
        if c[0] != '#':
            c = '#'+c
        Users[Users_l[a.lower()]]=(Users[Users_l[a.lower()]][0],c)
        with open('userstemp.cfg', 'w') as U_File:
            for d in Users.items():
                U_File.write(str(d)+'\n')
        os.remove('users.cfg')
        with open('users.cfg', 'w') as U_File:
            for d in Users.items():
                U_File.write(str(d)+'\n')
        mesg = "Changed "+a+"'s color to "+c
    else:
        mesg = "Error: Does not Compute"
    return mesg
def _mycolor(_list, log):
    color = _list[0]
    x = set(UDP_IP2)
    for a in x:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("/color "+uname[0]+" "+color, (a, UDP_PORT2))
        sock.close()
    del x
    _color(['me',color],log)
    return 'set color to '+color
def _colors():
    tlist = []
    for a in Users:
        tlist.append((a, Users[a][1]))
    return tlist
def _ping(_list=['list']):
    for user in _list:
        if user == 'all':
            x = set(UDP_IP2)
            x.update(Users.values())
            for a in x:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto("/ping", (a, UDP_PORT2))
                sock.close()
            del(x)
            #return "Pinged everybody."
        if user == 'list':
            for a in UDP_IP2:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto("/ping", (a, UDP_PORT2))
                sock.close()
            #return "Pinged active list."
        elif user == 'contacts':
            for a in Users:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto("/ping", (Users[a][0], UDP_PORT2))
                sock.close()
            #return "Pinged contact list."
        elif user.lower() in Users_l:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto("/ping", (Users[Users_l[user.lower()]][0], UDP_PORT2))
            sock.close()
            #return "Pinged "+user
        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto("/ping", (user, UDP_PORT2))
                sock.close()
                #return "Pinged "+user
            except:
                print "Bad IP"
                #return "Bad IP"
    return "Pinged "+jlist(_list)+"."
def _iam(_list,log):
    oldname = uname[0]
    uname[0]=_list[0]
    with open("UDPSettings.py","r") as U_File:
        with open("USettemp.txt","w+") as U2:
            for line in U_File:
                b = re.sub('uname\s?=\s?\[".*",\s?".*"\]',r'uname = ["'+uname[0]+'","'+uname[1]+'"]',line)
                U2.write(b)
    with open("USettemp.txt","r") as U_File:
        with open("UDPSettings.py","w+") as U2:
            for line in U_File:
                U2.write(line)
    os.remove('USettemp.txt')
    _new([uname[0],Users[Users_l[oldname.lower()]][0]],log)
    _send([uname[0],Users[Users_l[uname[0].lower()]][0],uname[1]],log)
    return "Changed name to "+_list[0]
