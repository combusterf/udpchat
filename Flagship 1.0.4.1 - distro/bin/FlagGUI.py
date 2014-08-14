from Tkinter import *
from UDPSettings import *
import UDPFunc

'''def func(val):
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
    	print "Already displaying that."'''

#---------------------------------------------------#
#-----------------GRAPHICS MANAGEMENT---------------#
#---------------------------------------------------#


class mainGUI(Frame):
    def shit(self):
        print "Hello There"
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.master.title("Hi there")
        self.master.geometry("400x40")
        self.master.resizable(width=TRUE, height=TRUE)
        self.master.iconbitmap(default='iconfile.ico')
        self.createMenus()
        self.createToolbar()
        self.display = 0
        self.toolbarDrop = Frame(self)
        self.toolbarDrop.pack()

    def createMenus(self):
        self.menubar = Menu(self)
        
        #all menus
        
        self.menubar.filemenu = Menu(self.menubar, tearoff=1)
        self.menubar.editmenu = Menu(self.menubar, tearoff=1)
        self.menubar.formatmenu = Menu(self.menubar, tearoff=1)
        self.menubar.contactsmenu = Menu(self.menubar, tearoff=1)
        self.menubar.viewmenu = Menu(self.menubar, tearoff=1)
        self.menubar.contactsmenu.addcontactmenu = Menu(self.menubar.contactsmenu, tearoff=1)

        #Menu Bar items
        
        self.menubar.add_cascade(label="File", menu=self.menubar.filemenu)
        self.menubar.add_cascade(label="Contacts", menu=self.menubar.contactsmenu)
        self.menubar.add_cascade(label="Edit", menu=self.menubar.editmenu)
        self.menubar.add_cascade(label="Format", menu=self.menubar.formatmenu)
        self.menubar.add_cascade(label="View", menu=self.menubar.viewmenu)

        #File Menu items

        self.menubar.filemenu.add_command(label="Online Status") # "Online", "Do Not Disturb", "Invisible", "Away"
        self.menubar.filemenu.add_command(label="Ping Room") # command=UDPFunc._ping
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

        self.menubar.contactsmenu.addcontactmenu.add_command(label="Add Individual") # Add a contact via username, IP, e-mail, or other unique ID.
        self.menubar.contactsmenu.addcontactmenu.add_command(label="Add from Skype") # Import contacts from your Skype friend list.
        self.menubar.contactsmenu.addcontactmenu.add_command(label="Add from Facebook")

        self.master.config(menu=self.menubar)

    def createToolbar(self):
        self.toolbar=Frame(self)
        self.toolbar.b=Button(self.toolbar, text="New Group", width=8, command=self.newgchat)
        self.toolbar.b.pack(side=LEFT, padx=2, pady=2)
        self.toolbar.pack(side=TOP, fill=X)
        self.toolbar.test123 = StringVar()
        self.toolbar.w=OptionMenu(self.toolbar,self.toolbar.test123,"Contact List", "Group List", "Directory Tree", "Tool Chest",command=self.func)
        self.toolbar.w.pack(side=TOP, padx=2, pady=2)

    def newgchat():
        pass

    def func(self,val):
        if val == "Contact List" and self.display!=1:
            self.toolbarDrop.destroy()
            self.toolbarDrop = Frame(self)
            self.master.geometry("400x400")
            self.display = 1
            self.toolbarDrop.pack({"side":"bottom"})
            print "Contact List selected."
            #test = test + '\n' + test
            #self.master.geometry("400x400")
            self.toolbarDrop.CList = Text(self.toolbarDrop, bd=0, bg="white", font="Arial",)
            self.toolbarDrop.CList.insert(END, 'test')
            self.toolbarDrop.CList.config(state=DISABLED)
            self.toolbarDrop.CList.place(x=6, y=35, width=350, height=350)
            self.toolbarDrop.CList.pack()

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

            
            self.toolbarDrop.photo = PhotoImage(file="temp.gif")
            self.toolbarDrop.label = Label(self.toolbarDrop.CList, image = self.toolbarDrop.photo)
            self.toolbarDrop.label.image = self.toolbarDrop.photo
            self.toolbarDrop.label.pack(side=RIGHT)

            
        elif val == "Directory Tree" and self.display !=2:
            self.toolbarDrop.destroy()
            self.toolbarDrop = Frame(self)
            self.master.geometry("400x400")
            self.toolbarDrop.pack()
            self.display = 2
            print "Directory Tree selected."
        elif val == "Tool Chest" and self.display !=3:
            self.toolbarDrop.destroy()
            self.toolbarDrop = Frame(self)
            self.master.geometry("400x400")
            self.toolbarDrop.pack()
            self.display = 3
            print "Tool Chest selected."
            self.toolbarDrop.toolbox = Frame(self.toolbarDrop)
            self.toolbarDrop.toolbox.b = Button(self.toolbarDrop.toolbox, text="Dice Roller", width=10, command=self.shit)
            self.toolbarDrop.toolbox.pack(side=BOTTOM, fill=X)
            self.toolbarDrop.toolbox.b.pack(side=LEFT)



        elif val == "Group List" and self.display!=4:
            self.toolbarDrop.destroy()
            self.toolbarDrop = Frame(self)
            self.master.geometry("400x400")
            self.toolbarDrop.pack({"side":"bottom"})
            self.display = 4
            print "Group List selected."

        else:
            print "Already displaying that."


'''toolbar = Frame(base)

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



base.protocol("WM_DELETE_WINDOW", handler)'''

base = Tk()
main = mainGUI(base)
main.mainloop()
base.destroy()

'''#Create a window
base = Tk()
base.title(WindowTitle)
base.geometry("400x40")
base.resizable(width=TRUE, height=TRUE)
base.iconbitmap(default='iconfile.ico')

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

base.config(menu=menubar)'''
