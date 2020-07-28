import cv2 as cv
import imutils
import numpy as np

#------- Reading an image using imread-----------#
# img = cv.imread("myimage.jpg")
# cv.imshow("output window",img)
# cv.waitKey()

#---------Reading a video using VideoCapture------#
video = cv.VideoCapture("video.mp4")
# print(video)
# ret, frame = video.read()
# print(ret)
# print(frame)

#--------code for writing the video to disk------#
# fourcc = cv.VideoWriter_fourcc(*"MJPG")
# out = cv.VideoWriter("output.avi",fourcc, 30, (W,H))

#--------Step1--------#
for i in range(55):
    ret, background = video.read()
# cv.imshow("background", background)

#-------Step2--------#
# Loop through all the frames in the video
while True:

    ret, frame = video.read()
    if not ret:
        break

    # Convert the frame to HSV color model
    framehsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # capture green color
    lowerGreen = np.array([60,65,20])
    upperGreen = np.array([90,255,255])
    
    # create the mask
    filter1 = cv.inRange(framehsv,lowerGreen,upperGreen)

    # Removing the noises from the mask using morphology
    filter1 = cv.morphologyEx(filter1, cv.MORPH_OPEN, np.ones((3,3),np.uint8))
    filter1 = cv.morphologyEx(filter1, cv.MORPH_DILATE,np.ones((3,3),np.uint8))

    # segment the green area, i.e cut it
    inverted_filter1 = cv.bitwise_not(filter1)

    #Segmenting the cloth out of the frame using bitwise_and & inverted mask
    segmented_frame = cv.bitwise_and(frame,frame,mask = inverted_filter1)

    # Background frame
    bg_frame = cv.bitwise_and(background,background,mask = filter1 )

    # Superimpose the 2 frames
    final_output = cv.addWeighted(segmented_frame,1,bg_frame,1,0)

    # show the frame as output
    cv.imshow("Output", final_output)
    # out.write(final_output)

    # stop the video if 'q' is pressed
    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        print("[INFO] Video Stopped...")
        break

# release the video pointer 
video.release()
# destroy all the open windows
cv.destroyAllWindows()