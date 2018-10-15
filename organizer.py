import os
import shutil
import time
from datetime import datetime
import subprocess
from tkinter import Tk, ttk, Frame, Button, Entry, Label, HORIZONTAL
from tkinter.filedialog import askopenfilename
import cv2
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import threading

current = os.getcwd()

class Window(Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Clapper")
        self.master.geometry('400x250+450+200')
        self.master.config(bg="#1b1b1b")
        self.master.resizable(0,0)
        self.AddWidgets()

    def AddWidgets(self):
        global User_input
        fontColor = '#f8bbd0'
        bgColor = '#1b1b1b'
        fontColorDull = '#c29ca5'

        self.TopFrame = Frame(self.master, bg=bgColor, width=400, height=50)
        self.TopFrame.grid(row=1, column=0)

        self.TextLabel = Label(self.master, text="Welcome to Clapper", font="Laksaman", fg=fontColor, bg=bgColor)
        self.TextLabel.grid(row=1, column=0, padx=10, pady=10)

        self.TextLabel = Label(self.master, text="Project Title", font="Laksaman", fg=fontColor, bg=bgColor)
        self.TextLabel.grid(row=2, sticky='W', padx=10, pady=10)

        self.TextLabel = Label(self.master, text="Video File", font="Laksaman", fg=fontColor, bg=bgColor)
        self.TextLabel.grid(row=3, sticky='W', padx=10, pady=10)

        self.TextLabel = Label(self.master, text="Organization:", font="Laksaman", fg=fontColor, bg=bgColor)
        self.TextLabel.grid(row=4, sticky='W', padx=10, pady=10)

        self.User_input = ttk.Entry(self.master, width=15)
        self.User_input.grid(row=2, column=0)
        User_input = self.User_input

        self.button = ttk.Button(self.master, text="Browse", cursor="hand2", width=10, command=self.OpenFile)
        self.button.grid(row=3, column=0, padx=10, pady=10)

        self.processButton = ttk.Button(self.master, text="Start", cursor="hand2", width=10, command=self.Process)
        self.processButton.grid(row=4, column=0, padx=10, pady=10)

        # Hidden Initially

        self.OrgLabel = Label(self.master, text="Organizing...", font=("Laksaman", 12), fg=fontColorDull, bg=bgColor)

        self.CutLabel = Label(self.master, text="Compiling...", font=("Laksaman", 12), fg=fontColorDull, bg=bgColor)

        self.RoughLabel = Label(self.master, text="Rough Cut:", font="Laksaman", fg=fontColorDull, bg=bgColor)

        self.CutButton = ttk.Button(self.master, text="Start", cursor="hand2", width=10, command=self.CompileCut)

        self.progress = ttk.Progressbar(self.master, orient=HORIZONTAL,length=100,  mode='determinate')

    def OpenFile(self):
        global inputDir
        global inputVideo
        # Get the file
        file = askopenfilename(initialdir=current)
        # Split the filepath to get the directory
        inputDir = os.path.split(file)[0]
        inputVideo = os.path.split(file)[1]

    def Process(self):
        global projectName
        projectName = (User_input.get())
        print("Project Name: %s" % projectName)
        self.Organize()

    def Organize(self):
        # Timer for keeping track of performance
        START_TIME = datetime.now()

        def org_thread():
            self.processButton.grid_forget()
            self.OrgLabel.grid(row=4, column=0, padx=10, pady=10)
            self.progress.grid(row=4, sticky='E', padx=10, pady=10)
            self.progress.start()

            print("CHECK")

            os.chdir(inputDir)

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

            while success:
                if(count%(fps/2)) == 0:
                    cv2.imwrite('tester.jpg', frame)
                    success, frame = cap.read()
                    count += 1
                    data = decode(cv2.imread('tester.jpg'), symbols=[ZBarSymbol.QRCODE])
                    if data == []:
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
                            self.trim(str(frame1/fps), str(frame2/fps - 1), video, fileName)
                            sceneNum = int(timeStamp1.split(':')[0])
                            takeNum = int(timeStamp1.split(':')[1])

                            timeStamp1 = dataClean
                            frame1 = count
                            fileNameFinal = timeStamp1.split(':')[0] + '.' + timeStamp1.split(':')[1] + '.mp4'
                            sceneNumFinal = int(timeStamp1.split(':')[0])
                            takeNumFinal = int(timeStamp1.split(':')[1])

                            if not os.path.exists('%s/Scene %d' % (projectName, sceneNum)):
                                os.makedirs('%s/Scene %d' % (projectName, sceneNum))
                            dirName = ('%s/Scene %d' % (projectName, sceneNum)) + ('/Take %d' % (takeNum)) + '.mp4'
                            shutil.move(fileName, dirName)


                else:
                    success, frame = cap.read()
                    count += 1

            self.trim(str(frame1/fps), str(count/fps), video, fileNameFinal)
            if not os.path.exists('%s/Scene %d' % (projectName, sceneNum)):
                os.makedirs('%s/Scene %d' % (projectName, sceneNum))
            dirNameFinal = ('%s/Scene %d' % (projectName, sceneNum)) + ('/Take %d' % (takeNumFinal)) + '.mp4'
            shutil.move(fileNameFinal, dirNameFinal)
            os.remove('tester.jpg')
            cap.release()
            cv2.destroyAllWindows()

            self.progress.stop()
            self.progress.grid_forget()
            self.OrgLabel['text'] = "Organized!"
            self.CutButton.grid(row=5, column=0, padx=10, pady=10)
            self.RoughLabel.grid(row=5, sticky='W', padx=10, pady=10)


        orgthread = threading.Thread(target=org_thread)
        orgthread.start()


        # Timer for keeping track of performance
        END_TIME = datetime.now()
        print('Duration to Organize: {}'.format(END_TIME - START_TIME))


    def CompileCut(self):

        def cut_thread():
            self.CutButton.grid_forget()
            self.CutLabel.grid(row=5, column=0, padx=10, pady=10)
            self.progress.grid(row=5, sticky='E', padx=10, pady=10)
            self.progress.start()

            # Finding the files again and sorting them
            os.chdir(projectName)
            files = os.listdir()
            folders = []
            for item in files:
                if not "." in item:
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
            ffmpegCall = (r'%s\ffmpeg' % current)
            COMMAND = [ffmpegCall, "-f", "concat", "-safe", "0", "-i", "%s/filenames.txt" % (projectName), "-c", "copy", "%s/roughcut.mp4" % (projectName)]
            subprocess.call(COMMAND, shell=True)
            os.remove('%s/filenames.txt' % (projectName))

            self.progress.stop()
            self.progress.grid_forget()
            self.CutLabel['text'] = "Generated!"

        cutthread = threading.Thread(target=cut_thread)
        cutthread.start()


    # Edits a given video by the starting and ending points of the video
    # Uses subprocess to call ffmpeg application to edit the video
    # As long as it is in the same folder as this python script it will work
    def trim(self, start, end, inputVid, outputVid):
        ffmpegCall = (r'"%s\ffmpeg"' % current)
        trim_command = ffmpegCall + ' -i ' + inputVid + " -ss  " + start + " -to " + end + " -c copy " + outputVid
        subprocess.call(trim_command)


root = Tk()
# root.tk.call('tk', 'scaling', 3.0)
Window = Window(root)
root.mainloop()
