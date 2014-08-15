from Tkinter import *

#---------------------------------------------------#
#-----------------GRAPHICS MANAGEMENT---------------#
#---------------------------------------------------#

class chatWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("Chat!")

class mainGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        try:
            import UDPSettings
        except ImportError:
            self.UDPSettings = None
        else:
            self.UDPSettings = UDPSettings
        try:
            import UDPFunc
        except ImportError:
            self.UDPFunc = None
        else:
            self.UDPFunc = UDPFunc
        self.pack(fill=BOTH, expand=True)
        self.master.title("S.S. Anne")
        self.master.geometry("400x40")
        self.master.resizable(width=TRUE, height=TRUE)
        self.master.iconbitmap(default='iconfile.ico')
        self.createMenus()
        self.createToolbar()
        self.display = 0
        self.toolbarDrop = Frame(self)

    def shit(self):
        print "Hello There"

    def createMenus(self):
        self.menubar = Menu(self)
        
        #all menus
        
        self.menubar.filemenu = Menu(self.menubar, tearoff=1)
        self.menubar.editmenu = Menu(self.menubar, tearoff=1)
        self.menubar.formatmenu = Menu(self.menubar, tearoff=1)
        self.menubar.contactsmenu = Menu(self.menubar, tearoff=1)
        self.menubar.viewmenu = Menu(self.menubar, tearoff=1)
        self.menubar.contactsmenu.addcontactmenu = Menu(self.menubar.contactsmenu, tearoff=1)
        self.menubar.filemenu.status = Menu(self.menubar.filemenu, tearoff=1)

        #Menu Bar items
        
        self.menubar.add_cascade(label="File", menu=self.menubar.filemenu)
        self.menubar.add_cascade(label="Contacts", menu=self.menubar.contactsmenu)
        self.menubar.add_cascade(label="Edit", menu=self.menubar.editmenu)
        self.menubar.add_cascade(label="Format", menu=self.menubar.formatmenu)
        self.menubar.add_cascade(label="View", menu=self.menubar.viewmenu)

        #File Menu items

        self.menubar.filemenu.add_cascade(label="Online Status", menu=self.menubar.filemenu.status) # "Online", "Do Not Disturb", "Invisible", "Away"
        self.menubar.filemenu.add_command(label="Ping Room", command=None) # command=UDPFunc._ping
        self.menubar.filemenu.add_separator()
        self.menubar.filemenu.add_command(label="Exit Flagship", command=self.quit)
        

        #Edit Menu items

        self.menubar.editmenu.add_command(label="My Picture") # Change and edit your display picture.
        self.menubar.editmenu.add_command(label="My Profile") # Profile Editor - change public profile.
        self.menubar.editmenu.add_command(label="My Post Defaults") # Adjust settings for posting defaults.
        self.menubar.editmenu.add_command(label="My Preferences") # Adjust client-side settings.

        #Format Menu items

        self.menubar.formatmenu.add_command(label="Fonts") #import, remove, and change font settings
        self.menubar.formatmenu.add_command(label="Change my color")
        self.menubar.formatmenu.add_command(label="Change friend color") # Enter friend name, enter desired hex value, profit

        #Contacts Menu items
        self.menubar.contactsmenu.add_cascade(label="Add Contact", menu=self.menubar.contactsmenu.addcontactmenu) # Cascade menu, to allow for multiple methods of adding new contacts.
        self.menubar.contactsmenu.add_command(label="Remove Contact") # Enter user ID to remove them from contact list - entering ID not in contact list returns prompt.
        self.menubar.contactsmenu.add_command(label="Import Contacts...") #Imports contacts from *.fsc file.
        self.menubar.contactsmenu.add_command(label="Export Contacts...") #Exports contacts to *.fsc file.
        self.menubar.contactsmenu.add_command(label="Start New Private Chat") #begins IM with one selected user.
        self.menubar.contactsmenu.add_command(label="Create New Group") # Opens new group chat window.
        self.menubar.contactsmenu.add_command(label="Join Existing Group...") # Enter Group ID to join existing group.

        #View Menu items

        self.menubar.viewmenu.add_command(label="Image Viewer") # View images from database. BASIC VIEWER. NO EDITING CAPABILITY. Not streamed publically.
        self.menubar.viewmenu.add_command(label="Object Viewer") # View 3D models from databasewith basic zoom and rotation controls. Not streamed publically.
        self.menubar.viewmenu.add_command(label="Text Viewer") # View text files from database in read-only. Not streamed publically.

        #Add Contact submenu items

        self.menubar.contactsmenu.addcontactmenu.add_command(label="Add Individual", command=self.addUser) # Add a contact via username, IP, e-mail, or other unique ID.
        self.menubar.contactsmenu.addcontactmenu.add_command(label="Add from Skype") # Import contacts from your Skype friend list.
        self.menubar.contactsmenu.addcontactmenu.add_command(label="Add from Facebook")
        
        #Online Status Submenu
        self.menubar.filemenu.status.add_command(label="Online")
        self.menubar.filemenu.status.add_command(label="Do Not Disturb")
        self.menubar.filemenu.status.add_command(label="Invisible")
        self.menubar.filemenu.status.add_command(label="Away")
        
        self.master.config(menu=self.menubar)

    def createToolbar(self):
        self.toolbar=Frame(self)
        self.toolbar.pack(side=TOP, fill=X)
        self.toolbar.b=Button(self.toolbar, text="New Group", width=8, command=self.newgchat)
        self.toolbar.b.pack(side=LEFT, padx=2, pady=2)
        self.toolbar.test123 = StringVar()
        self.toolbar.w=OptionMenu(self.toolbar,self.toolbar.test123,"Contact List", "Group List", "Directory Tree", "Tool Chest",command=self.func)
        self.toolbar.w.pack(side=TOP, padx=2, pady=2)

    def newgchat(self):
        self.cBase = Toplevel(self)
        self.chat = chatWindow(self.cBase)
        #Finish doing GUI things
        #Handle in chatWindow class above

    def func(self,val):
        if val == "Contact List" and self.display!=1:
            self.master.geometry("400x400")
            self.toolbarDrop.destroy()
            self.toolbarDrop = Frame(self)
            self.toolbarDrop.pack({"fill":"both","expand":True})
            self.display = 1
            print "Contact List selected."
            #test = test + '\n' + test
            #self.master.geometry("400x400")
            self.toolbarDrop.CList = Canvas(self.toolbarDrop, bd=0, bg="white")
            self.toolbarDrop.CList.Buttons = []
            self.toolbarDrop.photo = PhotoImage(file="temp.gif")
            self.toolbarDrop.CList.pics = []
            for a in self.UDPSettings.Users:
                self.toolbarDrop.CList.Buttons.append(Button(self.toolbarDrop.CList,{"text":a+": "+self.UDPSettings.Users[a][0], "bg":"white", "bd":0, "command":lambda IP=self.UDPSettings.Users[a][0]:self.baka(IP), "compound":"right", "image":self.toolbarDrop.photo}))
            for a in self.toolbarDrop.CList.Buttons:
                a.pack({"side":"top","fill":"x"})
            #self.toolbarDrop.CList.config(state=DISABLED)
            self.toolbarDrop.CList.place(x=6, y=0, width=350, height=350)
            

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

            
            #self.toolbarDrop.photo = PhotoImage(file="temp.gif")
            #self.toolbarDrop.label = Label(self.toolbarDrop.CList, image = self.toolbarDrop.photo)
            #self.toolbarDrop.label.image = self.toolbarDrop.photo
            #self.toolbarDrop.label.pack(side=RIGHT)

            
        elif val == "Directory Tree" and self.display !=2:
            self.toolbarDrop.destroy()
            self.toolbarDrop = Frame(self)
            self.master.geometry("400x400")
            self.toolbarDrop.pack({"fill":"both","expand":True})
            self.display = 2
            print "Directory Tree selected."
        elif val == "Tool Chest" and self.display !=3:
            self.toolbarDrop.destroy()
            self.toolbarDrop = Frame(self)
            self.master.geometry("400x400")
            self.toolbarDrop.pack({"side":"bottom","fill":"x"})
            self.display = 3
            print "Tool Chest selected."
            self.toolbarDrop.toolbox = Frame(self.toolbarDrop)
            self.toolbarDrop.toolbox.b = Button(self.toolbarDrop.toolbox, text="Dice Roller", width=10, command=self.shit)
            self.toolbarDrop.toolbox.pack(side=BOTTOM, fill=X)
            self.toolbarDrop.toolbox.b.pack({"side":"left"})



        elif val == "Group List" and self.display!=4:
            self.toolbarDrop.destroy()
            self.toolbarDrop = Frame(self)
            self.master.geometry("400x400")
            self.toolbarDrop.pack({"fill":"both","expand":True})
            self.display = 4
            print "Group List selected."

        else:
            print "Already displaying that."

    def addUser(self):
        self.addBase = Toplevel(self)
        self.addBase.geometry("200x75")
        self.addBase.title("Add User")
        self.addBase.adder = Frame(self.addBase)
        self.addBase.adder.pack({"fill":"both","expand":True})
        self.addBase.adder.Name = Frame(self.addBase.adder)
        self.addBase.adder.Name.pack({"fill":"x"})
        self.addBase.adder.Name.Label = Label(self.addBase.adder.Name,{"text":"Name:"})
        self.addBase.adder.Name.Label.pack({"side":"left"})
        self.addBase.adder.Name.Box = Entry(self.addBase.adder.Name)
        self.addBase.adder.Name.Box.pack({"side":"left","expand":True})
        self.addBase.adder.IPAddr = Frame(self.addBase.adder)
        self.addBase.adder.IPAddr.pack({"fill":"x"})
        self.addBase.adder.IPAddr.Label = Label(self.addBase.adder.IPAddr,{"text":"IP Address:"})
        self.addBase.adder.IPAddr.Label.pack({"side":"left"})
        self.addBase.adder.IPAddr.Box = Entry(self.addBase.adder.IPAddr)
        self.addBase.adder.IPAddr.Box.pack({"side":"left","expand":True})
        self.addBase.adder.Buttons = Frame(self.addBase.adder)
        self.addBase.adder.Buttons.pack({"side":"top"})
        self.addBase.adder.Buttons.OK = Button(self.addBase.adder.Buttons,{"text":"OK","command":lambda:self.addButton([self.addBase.adder.Name.Box.get(),self.addBase.adder.IPAddr.Box.get()])})
        self.addBase.adder.Buttons.OK.pack({"side":"left"})
        self.addBase.adder.Buttons.Cancel = Button(self.addBase.adder.Buttons, {"text":"Cancel","command":self.addBase.destroy})
        self.addBase.adder.Buttons.Cancel.pack({"side":"left"})

    def addButton(self, args, log=None):
        self.UDPFunc._new(args,log)
        self.addBase.destroy()
        
    def baka(self, ipaddr):
        print ipaddr
    

base = Tk()
main = mainGUI(base)
base.protocol("WM_DELETE_WINDOW", main.quit)
main.mainloop()
base.destroy()
