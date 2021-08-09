# Import the necessary packages
import csv
import datetime as dt
import os
import sys
import time
from datetime import datetime
import shutil

import cv2
import dlib
import imutils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from imutils import face_utils
from matplotlib import style
from scipy.spatial import distance as dist

from EAR_calculator import *
from gaze_tracking import GazeTracking

import mysql.connector

style.use('fivethirtyeight')
# Creating the dataset


def assure_path_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


# all eye and mouth aspect ratio with time
ear_list = []
total_ear = []
mar_list = []
total_mar = []
ts = []
total_ts = []


# Arrays for Report CSV
report_timestamp = []
report_types = []
report_count = []

#arrays for focus csv
# report_timestamp = []
fr_types = []
fr_count = []

# Declare a constant which will work as the threshold for EAR value, below which it will be regared as a blink
EAR_THRESHOLD = 0.48
# Declare another costant to hold the consecutive number of frames to consider for a blink
EYE_AR_CONSEC_FRAMES = 2
# Another constant which will work as a threshold for MAR value
MAR_THRESHOLD = 0.5

# Initialize two counters
BLINK_COUNT = 0
FRAME_COUNT = 0

gaze = GazeTracking()
# Now, intialize the dlib's face detector model as 'detector' and the landmark predictor model as 'predictor'
print("[INFO]Loading the predictor.....")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Grab the indexes of the facial landamarks for the left and right eye respectively
(lstart, lend) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rstart, rend) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
# (mStart, mEnd) gets us the first and last coordinates for the mouth.
(mstart, mend) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# Now start the video stream and allow the camera to warm-up
print("[INFO]Loading Camera.....")
vs = cv2.VideoCapture(0)
# time.sleep(1.0)

assure_path_exists("dataset/")
assure_path_exists(os.path.join("dataset", "lost_focus"))
assure_path_exists(os.path.join("dataset", "drowsy"))
assure_path_exists(os.path.join("dataset", "yawn"))
assure_path_exists(os.path.join("dataset", "attentive"))
count_sleep = 0
count_yawn = 0
count_focus = 0
count_lossfocus = 0
# Now, loop over all the frames and detect the faces
while True:
    # Extract a frame
    _, frame = vs.read()
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, "PRESS 'q' TO EXIT", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # Resize the frame
    frame = imutils.resize(frame, width=750)
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces
    # rects = detector(frame, 1)
    rects = detector(gray, 0)
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    if(len(rects) == 0):
        cv2.putText(frame, "-----Face Not Detected-----", (85, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else:
        # Now loop over all the face detections and apply the predictor
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            # Convert it to a (68, 2) size numpy array
            shape = face_utils.shape_to_np(shape)

            # Draw a rectangle over the detected face
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            # attention_percent = ((len(shape) - total_del)*100)/(len(shape)+0.1)
            # _,confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Put a number
            cv2.putText(frame, "Student", (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # for headpose
            # 2D image points. If you change the image, you need to change vector
            image_points = np.array([
                (shape[30, :]),         # Nose tip
                (shape[8, :]),          # Chin
                (shape[36, :]),         # Left eye left corner
                (shape[45, :]),         # Right eye right corner
                (shape[48, :]),         # Left Mouth corner
                (shape[54, :])          # Right mouth corner
            ], dtype="double")

            # 3D model points.
            model_points = np.array([
                (0.0, 0.0, 0.0),                 # Nose tip
                (0.0, -330.0, -65.0),            # Chin
                (-225.0, 170.0, -135.0),         # Left eye left corner
                (225.0, 170.0, -135.0),          # Right eye right corner
                (-150.0, -150.0, -125.0),        # Left Mouth corner
                (150.0, -150.0, -125.0)          # Right mouth corner
            ])
            # Camera internals
            size = frame.shape
            focal_length = size[1]
            center = (size[1]//2, size[0]//2)
            camera_matrix = np.array(
                [[focal_length, 0, center[0]],
                 [0, focal_length, center[1]],
                 [0, 0, 1]], dtype="double"
            )
            #print ("Camera Matrix :\n {0}".format(camera_matrix))

            dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
            (success, rotation_vector, translation_vector) = cv2.solvePnP(
                model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
            #print ("Rotation Vector:\n {0}".format(rotation_vector))
            #print ("Translation Vector:\n {0}".format(translation_vector))

            # Project a 3D point (0, 0, 1000.0) onto the frame.
            # We use this to draw a line sticking out of the nose
            (nose_end_point2D, jacobian) = cv2.projectPoints(np.array(
                [(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

            for p in image_points:
                cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)
            # x1, x2 = head_pose_points(frame, rotation_vector, translation_vector, camera_matrix)
            p0 = (int(image_points[0][0]), int(image_points[0][1]) - 2)
            p1 = (int(image_points[0][0]), int(image_points[0][1]))
            p2 = (int(nose_end_point2D[0][0][0]),
                  int(nose_end_point2D[0][0][1]))
            cv2.line(frame, p1, p2, (255, 0, 0), 2)
            # cv2.line(frame, tuple(x1), tuple(x2), (255, 255, 0), 2)
            angle = cal_angle(p0, p1, p2)

            # calc euler angle
            rotation_mat, _ = cv2.Rodrigues(rotation_vector)
            pose_mat = cv2.hconcat((rotation_mat, translation_vector))
            _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(
                pose_mat)

            # for eye
            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lstart:lend]
            rightEye = shape[rstart:rend]
            # for mouth
            mouth = shape[mstart:mend]

            # Compute the EAR for both the eyes
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # Take the average of both the EAR(eye aspect ratio)
            EAR = (leftEAR + rightEAR) / 2.0
            # live datawrite in csv
            ear_list.append(EAR)
            # print(ear_list)

            ts.append(dt.datetime.now().strftime('%H:%M:%S'))
            # Compute the convex hull for both the eyes and then visualize it
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            # Draw the contours
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [mouth], -1, (0, 255, 0), 1)

            MAR = mouth_aspect_ratio(mouth)
            mar_list.append(MAR)

            if gaze.is_center and (-10 <= euler_angle[2, 0] and euler_angle[2, 0] <= 10):
                count_focus += 1
                cv2.putText(frame, "ATTENTIVE!", (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imwrite("dataset/attentive/attentive.jpg", frame)
                report_timestamp.append(
                    dt.datetime.now().strftime('%H:%M:%S.%f'))
                report_types.append('attentive')
                report_count.append(count_focus)

            else:
                count_lossfocus += 1
                cv2.putText(frame, "** LOST FOCUS! **", (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imwrite("dataset/lost_focus/lost_focus%d.jpg" %
                            count_lossfocus, frame)
                report_timestamp.append(
                    dt.datetime.now().strftime('%H:%M:%S.%f'))
                report_types.append('lost_focus')
                report_count.append(count_lossfocus)

                # Check if EAR < EAR_THRESHOLD, if so then it indicates that a blink is taking place
                # Thus, count the number of frames for which the eye remains closed
                if EAR < EAR_THRESHOLD:
                    FRAME_COUNT += 1
                    cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
                    cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

                    # Add the frame to the dataset as a proof of drowsy driving
                    if FRAME_COUNT >= EYE_AR_CONSEC_FRAMES:
                        count_sleep += 1
                        cv2.putText(frame, "** DROWSINESS ALERT! **", (270, 55),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        # Add the frame to the dataset ar a proof of drowsy student
                        cv2.imwrite("dataset/drowsy/drowsy%d.jpg" %
                                    count_sleep, frame)
                        report_timestamp.append(
                            dt.datetime.now().strftime('%H:%M:%S.%f'))
                        report_types.append('drowsy')
                        report_count.append(count_sleep)
                else:
                    FRAME_COUNT = 0

                cv2.putText(frame, "E.A.R: {:.2f}".format(EAR),
                 (600, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Check if the student is yawning
                if MAR > MAR_THRESHOLD:
                    FRAME_COUNT += 1
                    count_yawn += 1
                    cv2.drawContours(frame, [mouth], -1, (0, 0, 255), 1)
                    cv2.putText(frame, "YAWNING!", (300, 75),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    # Add the frame to the dataset ar a proof of drowsy studnet
                    cv2.imwrite("dataset/yawn/yawn%d.jpg" % count_yawn, frame)
                    report_timestamp.append(
                        dt.datetime.now().strftime('%H:%M:%S.%f'))
                    report_types.append('yawn')
                    report_count.append(count_yawn)

                else:
                    FRAME_COUNT = 0
                cv2.putText(frame, "M.A.R : {:.2f}".format(MAR), (600, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        # total data collection for plotting
        for i in ear_list:
            total_ear.append(i)
        for i in mar_list:
            total_mar.append(i)
        for i in ts:
            total_ts.append(i)
        
    # display the frame
    cv2.imshow("Output", frame)
    key = cv2.waitKey(50) & 0xff

    if key == 27:
        exit()

    if key == ord('q') or FRAME_COUNT >= 10:
        break
    # elif FRAME_COUNT >= 10: # Take 10 face sample and stop video
    #      break


a = total_ear[:30]
b = total_mar[:30]
# c = total_ang
d = total_ts[:30]
# print(total_ang)
df = pd.DataFrame({"EAR": a, "MAR": b, "TIME": d})

df.to_csv("op_webcam.csv", index=False)
df = pd.read_csv("op_webcam.csv")

report_csv = pd.DataFrame(
    {"timestamp": report_timestamp, "type": report_types, "count": report_count})
report_csv.to_csv("report.csv", index=False)

df.plot(x='TIME', y=['EAR', 'MAR'])
plt.xticks(rotation=45, ha='right')

plt.subplots_adjust(left=0.140, bottom=0.30, right= 0.880, top= 0.905)
plt.title('EAR & MAR calculation over time of webcam')
plt.ylabel('EAR & MAR')
plt.xlabel('Time')

plt.savefig('report_chart.png')
# plt.show()



y = dt.datetime.now()
x = y.strftime('%d_%m_%Y_%H_%M_%S')
os.makedirs('static/assets/Reports/'+x)
shutil.move('dataset', 'static/assets/Reports/'+x)
shutil.move('report.csv', 'static/assets/Reports/'+x+'/report.csv')

shutil.move('report_chart.png', 'static/assets/Reports/'+x+'/report_chart.png')

print('[INFO]Report folder created and all reports Moved...')



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pythonlogin"
)

mycursor = mydb.cursor()
sql = "INSERT INTO reports (userid, folder_string, timestamp) VALUES (%s, %s, %s)"
val = (sys.argv[3], x, y)
mycursor.execute(sql, val)
mydb.commit()

cv2.destroyAllWindows()
vs.release()
