import cv2
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
#from matplot import function_plot


count1 = 1

#cascPath = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')#sys.argv[1]
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')#cascPath)

# video_capture = cv2.VideoCapture('/home/shubham/Desktop/noflicker-ideal-from-0.83333-to-1-alpha-50-level-4-chromAtn-1.avi')#0)
video_capture = cv2.VideoCapture('data/after running the stairs-ideal-from-1.6667-to-1.8333-alpha-50-level-4-chromAtn-1.avi')#0)

detector = cv2.SimpleBlobDetector()

file_object = open('sample.txt', 'w')

# for graph
graph_count = []
graph_beat = []

count_y = 0
count_x = 0
# ------------

while (video_capture.isOpened()):

    count1 = count1 + 5
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE


    )


    keypoints = detector.detect(frame)
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)



    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
    nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)


        count = 1
        for (ex,ey,ew,eh) in eyes:
            if (count%2 == 1 ):

                count= count+1

                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                x_cord = (x+ex)/3
                y_cord = (y+ey+h+eh)/3


                cv2.circle(roi_color,( x_cord,y_cord), 25, (0,255,255), -1)

            else:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


                x_cord = (x+ex+w+ew)/3
                y_cord = (y+eh+ey+h)/3

                cv2.circle(roi_color,( x_cord,y_cord), 25, (0,255,255), -1)



    #        nose = nose_cascade.detectMultiScale(roi_gray)
     #       for (nx,ny,nw,nh) in nose:
      #          cv2.rectangle(roi_color,(nx,ny),(nx+nw,ny+nh),(0,0,255),2)

     #       mouth = mouth_cascade.detectMultiScale(roi_gray)
      #      for (mx,my,mw,mh) in mouth:
       #         if (my > ny+(nh/2)):
    #             cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(255,0,0),2)

    region = frame[y:y+h,x:x+w]
    # print(region.mean())

    # graph
    count_x += 1
    count_y = region.mean()
    graph_beat.append(count_y)
    graph_count.append(count_x)
    # -----
    if (count % 2 ==0):
        # Make a random plot...
        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.plot(graph_count, graph_beat)
        # fig.add_subplot(111)

        # If we haven't already shown or saved the plot, then we need to
        # draw the figure first...
        fig.canvas.draw()

        # Now we can save it to a numpy array.
        data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    ##########


    file_object.write(str(count1)+"," +str(int(region.mean()))+'\n')
    #plt.plot(time.time(), region.mean(), linewidth=2.0)
    #plt.show()

    # Display the resulting frame
    cv2.imshow('Video', data)
    cv2.imshow('Video2', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




# When everything is done, release the capture
file_object.close()
video_capture.release()
cv2.destroyAllWindows()
