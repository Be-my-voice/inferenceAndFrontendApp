import cv2
import mediapipe as mp
import numpy as np
import time

CLOUD = "http://4.247.22.145:8000/endpoint"
LOCAL = ""

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.7)

cap= cv2.VideoCapture(0)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(frame_width, frame_height)
width = 480
height = 480
rescale_width = 720
rescale_height = 720

writer= cv2.VideoWriter('basicvideo.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (rescale_width,rescale_height))

left = (frame_width - width) // 2
top = (frame_height - height) // 2
right = left + width
bottom = top + height


# Record video for 3 seconds
start_time = cv2.getTickCount()

while True:
    elapsed_seconds = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

    ret,frame= cap.read()

    frameToRec = frame

    frame = cv2.flip(frame, 1)
    frameToRec = cv2.flip(frameToRec, 1)

    frame = cv2.resize(frame, (720, 720))
    frameToRec = cv2.resize(frameToRec, (720, 720))

    if(elapsed_seconds >= 9 ):
        break
    
    if elapsed_seconds >5 and elapsed_seconds < 9:
        # Add overlay text with the elapsed seconds
        text = "Elapsed seconds: {} : recording.....".format(elapsed_seconds)
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cropped_frame = frameToRec[top:bottom, left:right]
        resized_frame = cv2.resize(cropped_frame, (rescale_width, rescale_height))
        writer.write(resized_frame)

    if elapsed_seconds <= 5:
        # Add overlay text with the elapsed seconds
        text = "Elapsed seconds: {} : get ready.....".format(elapsed_seconds)
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    # Check if the user pressed 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
writer.release()
cv2.destroyAllWindows()

# identifying the skeleton

cap= cv2.VideoCapture("basicvideo.avi")

while cap.isOpened():
    ret,frameToIdentify= cap.read()
    # print(ret)

    results = pose.process(frameToIdentify)

    mp_drawing.draw_landmarks(frameToIdentify, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
    cv2.imshow('frame', frameToIdentify)

    cv2.waitKey(1)

cap.release()

cv2.destroyAllWindows()

headers = {'Content-Type': 'application/json'}

# Send the POST request
response = requests.post(CLOUD, data=payload, headers=headers)
print("sent")

# Check the response status code
if response.status_code == 200:
    print("Request successful!")
    print(response.content)
else:
    print("Request failed with status code:", response.status_code)
