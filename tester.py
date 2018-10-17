import os
import subprocess
current = os.getcwd()
os.chdir(r'C:\Users\Sayuj\Downloads')
projectName = 'lol'
ffmpegCall = (r'%s\ffmpeg' % current)
COMMAND = [ffmpegCall, "-f", "concat", "-safe", "0", "-i", "%s/filenames.txt" % (projectName), "-c", "copy", "%s/roughcut.mp4" % (projectName)]
subprocess.call(COMMAND, shell=True)
