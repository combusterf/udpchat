import re

#a = 'uname = ["dude","#808080"]'
#b = re.sub('".*"',"abc",a)

with open("UDPSettings.txt","r") as U_File:
    with open("USET.txt","w+") as U2:
        for line in U_File:
            b = re.sub('uname\s?=\s?\["(.*)",\s?"(.*)"\]',r'uname = ["abc","\2"]',line)
            U2.write(b)
