import os
import cv2
from datetime import datetime
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from moviepy.editor import *

start_time = datetime.now()

timeStamps = {}
video = 'self.mp4'
cap = cv2.VideoCapture(video)

fps = cap.get(cv2.CAP_PROP_FPS)

success, image = cap.read()
frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
count = 0
success = True

while (success):

    cv2.imwrite('tester.jpg', frame)
    success,frame = cap.read()
    count += 1
    data = decode(cv2.imread('tester.jpg'), symbols=[ZBarSymbol.QRCODE])

    if (data == []):
        continue
    else:
        dataClean = (data[0].data).decode('utf8')
        timeStamps[dataClean] = count


end_time = datetime.now()
os.remove('tester.jpg')
print(timeStamps)

print('Duration: {}'.format(end_time - start_time))

cap.release()
cv2.destroyAllWindows()

# trimmer = VideoFileClip('self.mp4')
# trimmed = trimmer.subclip(t_start=second)
# trimmed.write_videofile('trim.mp4', codec = 'libx264')

