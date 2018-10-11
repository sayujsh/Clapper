import os

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

root = Tk()
frame = Frame(root)
frame.pack()

Title = root.title( "Clapper" )
label = ttk.Label(root, text ="Welcome to Clapper",foreground="black",font=("Helvetica", 16))
label.pack()

current = os.getcwd()
inputFile = current

def OpenFile():
    global inputDir
    global inputVideo
    # Get the file
    file = askopenfilename(initialdir=current)
    # Split the filepath to get the directory
    inputDir = os.path.split(file)[0]
    inputVideo = os.path.split(file)[1]


def show_entry_fields():
    global projectName
    projectName = (User_input.get())
    quit()
    print("Project Name: %s" % projectName)


button = Button(frame, 
                   text="Browse", 
                   fg="black",
                   font=("Helvetica", 8),
                   command=OpenFile)
button.pack(side=LEFT)

User_input = Entry(root)
User_input.pack()

Button(root, text='Show', command=show_entry_fields).pack()


root.mainloop()

print(inputDir)
print(inputVideo)
