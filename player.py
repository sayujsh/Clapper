import os
import cv2
from datetime import datetime
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

start_time = datetime.now()

timeStamps = {}
video = 'QRTest.mov'
cap = cv2.VideoCapture(video)

fps = cap.get(cv2.CAP_PROP_FPS)

success, image = cap.read()
frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
count = 0
success = True
frameArray = []
while (success):
    frameArray.append(frame)
    if((count%fps) == 0):
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


os.remove('tester.jpg')
print(timeStamps)

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
    if not (os.path.exists('Scene %d' % (key))):
        os.makedirs('Scene %d' % (key))
    os.chdir('Scene %d' % (key))
    for i, subKey in enumerate(timeStampsCleaned[key]):
        # if(subKey != len(timeStampsCleaned)-1) :
        print(subKey)
        print(i)
        out = cv2.VideoWriter('Take_%d.mp4' % subKey, fourcc, fps, (1920, 1080))

        t1 = (timeStampsCleaned[key][subKey])
        t2 = 0
        if (i < len(timeStampsCleaned[key]) - 1):
            t2 = (timeStampsCleaned[key][subKey+1])
        else:
            t2 = len(frameArray) - 1

        for i in range(t1, t2):
            out.write(frameArray[i])
        out.release()
        # trimmed = original.subclip(3, 6)

        # # trimmed = original.subclip(t1,t2)

        # trimmed.write_videofile('Take_%d.mp4' % subKey, codec = 'libx264')

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

