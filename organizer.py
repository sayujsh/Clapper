import os
import cv2
import shutil
from datetime import datetime
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import subprocess

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
    print("Project Name: %s" % projectName)
    root.destroy()


button = Button(frame, 
                   text="Browse", 
                   fg="black",
                   font=("Helvetica", 8),
                   command=OpenFile)
button.pack(side=LEFT)

User_input = Entry(root)
User_input.pack()

Button(root, text='Process', command=show_entry_fields).pack()


root.mainloop()








start_time = datetime.now()



# Edits a given video by the starting and ending points of the video
# Uses subprocess to call ffmpeg application to edit the video
# As long as it is in the same folder as this python script it will work
def trim(start,end,input,output):
	str = 'ffmpeg -i ' + input + " -ss  " + start + " -to " + end + " -c copy " + output
	subprocess.call(str)

shutil.copy(inputDir+'/'+inputVideo, current)
# os.chdir(inputDir)

timeStamps = {}
video = inputVideo
cap = cv2.VideoCapture(video)

fps = cap.get(cv2.CAP_PROP_FPS)

success, frame = cap.read()

success = True
count = 0
frame1 = 0
switch = 0
timeStamp1 = ''

while (success):
    if((count%(fps/2)) == 0):
        cv2.imwrite('tester.jpg', frame)
        success,frame = cap.read()
        count += 1
        data = decode(cv2.imread('tester.jpg'), symbols=[ZBarSymbol.QRCODE])
        if (data == []):
            continue
        else:
            dataClean = (data[0].data).decode('utf8')
            timeStamps[dataClean] = count
            if switch == 0:
                timeStamp1 = dataClean
                frame1 = count
                switch += 1
            if dataClean != timeStamp1:
                frame2 = count
                fileName = timeStamp1.split(':')[0] + '.' + timeStamp1.split(':')[1] + '.mp4'
                trim( str(frame1/fps), str(frame2/fps - 1), video, fileName)
                sceneNum = int(timeStamp1.split(':')[0])
                takeNum = int(timeStamp1.split(':')[1])

                timeStamp1 = dataClean
                frame1 = count
                fileNameFinal = timeStamp1.split(':')[0] + '.' + timeStamp1.split(':')[1] + '.mp4'
                sceneNumFinal = int(timeStamp1.split(':')[0])
                takeNumFinal = int(timeStamp1.split(':')[1])

                if not (os.path.exists('%s/Scene %d' % (projectName,sceneNum))):
                    os.makedirs('%s/Scene %d' % (projectName, sceneNum))
                dirName = ('%s/Scene %d' % (projectName,sceneNum)) + ('/Take %d' % (takeNum)) + '.mp4'
                shutil.move(fileName, dirName)


    else:
        success,frame = cap.read()
        count += 1

trim( str(frame1/fps), str(count/fps), video, fileNameFinal)
if not (os.path.exists('%s/Scene %d' % (projectName,sceneNum))):
    os.makedirs('%s/Scene %d' % (projectName,sceneNum))
dirNameFinal = ('%s/Scene %d' % (projectName,sceneNum)) + ('/Take %d' % (takeNumFinal)) + '.mp4'
shutil.move(fileNameFinal, dirNameFinal)
os.remove('tester.jpg')
cap.release()
cv2.destroyAllWindows()
os.remove(video)

#DOES EVERYTHING IT NEEDS TO BY THIS LINE

# Finding the files again and sorting them
os.chdir(projectName)
files = os.listdir()
folders = []
for item in files:
    if not ("." in item):
        folders.append(item)
folders.sort()

filenames = open("filenames.txt", "w")

# Add all the file names to a txt for concatenation
for folder in folders:
    os.chdir(folder)
    vidfiles = os.listdir()
    vidfiles.sort()
    for item in vidfiles:
        filenames.write('file \'' + folder + '/' + item + '\'\n')
    os.chdir("..")

filenames.close()

# Concatenate and remove the txt file
os.chdir("..")
command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "%s/filenames.txt" % (projectName), "-c", "copy", "%s/roughcut.mp4" % (projectName)]
subprocess.call(command)
os.remove('%s/filenames.txt' % (projectName))

# Timer for keeping track of performance
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))