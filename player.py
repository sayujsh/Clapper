import os
import cv2
from datetime import datetime
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from moviepy.editor import *
import math

start_time = datetime.now()

timeStamps = {}
video = 'QRTest.mov'
cap = cv2.VideoCapture(video)

fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)

success, image = cap.read()
frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
count = 0
success = True
frameArray = []
while (success):
    frameArray.append(frame)
    if((count%5) == 0):
        cv2.imwrite('tester.jpg', frame)
        success,frame = cap.read()
        count += 1
        data = decode(cv2.imread('tester.jpg'), symbols=[ZBarSymbol.QRCODE])

        if (data == []):
            continue
        else:
            dataClean = (data[0].data).decode('utf8')
            timeStamps[dataClean] = count
    else:
        success,frame = cap.read()
        count += 1


print(len(frameArray))

end_time = datetime.now()
os.remove('tester.jpg')
print(timeStamps)

print('Duration: {}'.format(end_time - start_time))

cap.release()
cv2.destroyAllWindows()



timeStampsCleaned = {}
for key in timeStamps:
    sceneNum = int(key.split(':')[0])
    takeNum = int(key.split(':')[1])
    try:
        timeStampsCleaned[sceneNum][takeNum] = timeStamps[key]
    except:
        timeStampsCleaned[sceneNum] = {}
        timeStampsCleaned[sceneNum][takeNum] = timeStamps[key]
print(timeStampsCleaned)

timeStampsCleaned = {1: {1: 166, 2: 321, 3: 471, 4: 636}}
fps = 30.0
fourcc = cv2.VideoWriter_fourcc(*'VXID')
for key in timeStampsCleaned:
    os.makedirs('Scene %d' % (key))
    os.chdir('Scene %d' % (key))
    for i, subKey in enumerate(timeStampsCleaned[key]):
        # if(subKey != len(timeStampsCleaned)-1) :
        print(subKey)
        print(i)
        out = cv2.VideoWriter('Take_%d.mp4' % subKey, fourcc, fps, (1920, 1080))
        for i in range(166, 321):
            out.write(frameArray[i])
        out.release()
        # trimmed = original.subclip(3, 6)


        # # t1 = round((timeStampsCleaned[key][subKey])/fps, 2)
        # # t2 = round((timeStampsCleaned[key][subKey+1])/fps-1, 2)
        # # trimmed = original.subclip(t1,t2)

        # trimmed.write_videofile('Take_%d.mp4' % subKey, codec = 'libx264')

