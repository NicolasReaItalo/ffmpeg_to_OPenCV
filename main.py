import cv2
import subprocess as sp
import numpy

from package import timecode

FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
        '-i', './videos/TEST.mov',             # fifo is the named pipe
        '-pix_fmt', 'bgr24',      # opencv requires bgr24 pixel format.
        '-vcodec', 'rawvideo',
        '-an','-sn',              # we want to disable audio processing (there is no audio)
        '-f', 'image2pipe', '-']    
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

starting_timecode = '01:00:00:00'
h,m,s,f = timecode.tc_split(starting_timecode)
img_number =  1 #timecode.tc_to_frame(h,m,s,f,24)
while True:
    # Capture frame-by-frame
    raw_image = pipe.stdout.read(1920*1080*3)
    # transform the byte read into a numpy array
    image =  numpy.frombuffer(raw_image, dtype='uint8')
    image = image.reshape((1080,1920,3))          # Notice how height is specified first and then width
    if image is not None:

        b = image.item(540,0,0)
        g = image.item(540,0,1)
        r = image.item(540,0,2)
    #    if r == 0 & g == 0 & b == 0:
     #       print(f"image: {timecode.frame_to_tc_02(img_number,24)} -> ({r}:{g}:{b})")
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY)
        #if ret:
        #cv2.imshow('Video', thresh1)

        if img_number == 251:
            #thumbnail = image.reshape(108,192,3)
            cv2.imwrite("thumbnail.png",image)

        img_number += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    pipe.stdout.flush()

cv2.destroyAllWindows()