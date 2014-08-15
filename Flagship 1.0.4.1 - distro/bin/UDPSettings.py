#UDPSettings

Users = {}
with open("users.cfg", 'r') as U_File:
    #Users = {}
    for line in U_File:
        a = eval(line[:-1])
        Users[a[0]]=a[1]
IP_Lookup = {}
Users_l = {}
for k in Users:
    Users_l[k.lower()]=k
for(k,v) in Users.iteritems():
    IP_Lookup[v[0]] = k 
UDP_IP = "0.0.0.0"
UDP_PORT = 6000
UDP_IP2 = set([])
UDP_PORT2 = 6000
at = 0
functions = {"quit":"Safely quits message system.",
             "add":"Adds contact or IP address to conversation.",
             "remove":"Removes contact/IP from conversation.",
             "list":"Lists currently active IPs/contacts.",
             "contacts":"Lists contacts not in conversation.",
             "new":"Adds a new contact.",
             "kill":"Deletes contact from contacts list and removes it from conversation.",
             "send":"Sends a contact. Syntax: name IP\nIt only works like this for now. We are working on a system to send contacts with just a name.",
             "color":"Sets color of a user on your computer.",
             "mycolor":"Sets your color on all connected computers.",
             "colors":"Displays colors of all users in contacts."}
colors = {"aqua":"#00FFFF","black":"#000000","blue":"#0000FF","fuchsia":"#FF00FF","gray":"#808080","green":"#008000","lime":"#00FF00","maroon":"#800000",
          "navy":"#000080","olive":"#808000","purple":"#800080","red":"#FF0000","silver":"#C0C0C0","teal":"#008080","white":"#FFFFFF","yellow":"#FFFF00"}
uname = ["Jacob","#00FFFF"]
FirstRun = 0
