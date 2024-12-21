import cv2
import mediapipe as mp

cap = cv2.VideoCapture("test2.mp4")
ret, frame = cap.read()

original_height, original_width, channels = frame.shape
aspect_ratio = original_height / original_width

new_width = 640
new_height = int(new_width * aspect_ratio)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

if not cap.isOpened():
    print("Eroare: Nu putem deschide videoul.")
    exit()
else:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Finalul videoului || nu putem citi frame")
            break

        resized_frame = cv2.resize(frame, (new_width, new_height))
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

        results = pose.process(
            rgb_frame)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                resized_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

        cv2.imshow("Video Frame", resized_frame)

        if cv2.waitKey(30) == 27:
            break

cap.release()
cv2.destroyAllWindows()
