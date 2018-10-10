import os
import cv2
import shutil
from datetime import datetime
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import subprocess

start_time = datetime.now()

def trim(start,end,input,output):
	str = 'ffmpeg -i ' + input + " -ss  " + start + " -to " + end + " -c copy " + output
	subprocess.call(str)

timeStamps = {}
video = r'test_files\QRTest.mov'
cap = cv2.VideoCapture(video)

fps = cap.get(cv2.CAP_PROP_FPS)

success, image = cap.read()
frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
count = 0
success = True
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

                if not (os.path.exists('output/Scene %d' % (sceneNum))):
                    os.makedirs('output/Scene %d' % (sceneNum))
                dirName = ('output/Scene %d' % (sceneNum)) + ('/Take %d' % (takeNum)) + '.mp4'
                shutil.move(fileName, dirName)


    else:
        success,frame = cap.read()
        count += 1

trim( str(frame1/fps), str(count/fps), video, fileNameFinal)
if not (os.path.exists('output/Scene %d' % (sceneNumFinal))):
    os.makedirs('output/Scene %d' % (sceneNumFinal))
dirNameFinal = ('output/Scene %d' % (sceneNumFinal)) + ('/Take %d' % (takeNumFinal)) + '.mp4'
shutil.move(fileNameFinal, dirNameFinal)
os.remove('tester.jpg')

cap.release()
cv2.destroyAllWindows()

#DOES EVERYTHING IT NEEDS TO BY THIS LINE

# Finding the files again and sorting them
os.chdir('output')
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
command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "output/filenames.txt", "-c", "copy", "output/roughcut.mp4"]
subprocess.call(command)
os.remove('output/filenames.txt')

# Timer for keeping track of performance
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))