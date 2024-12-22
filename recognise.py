import cv2
import mediapipe as mp

cap = cv2.VideoCapture("test2.mp4")
ret, frame = cap.read()

original_height, original_width, channels = frame.shape
aspect_ratio = original_height / original_width

new_width= 1020
new_height= int(new_width * aspect_ratio)

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

        umar_stang = results.pose_landmarks.landmark[11]

        x_pixel = int(umar_stang.x * new_width)
        y_pixel = int(umar_stang.y * new_height)

        cv2.putText(
            resized_frame,                      # Image to draw on
            f"Umar Stang: (x:{x_pixel}, y:{y_pixel})",                      # Text
            (50, 100),                  # Bottom-left corner of the text
            cv2.FONT_HERSHEY_COMPLEX,   # Font type
            1.5,                        # Font scale
            (255, 255, 255),            # Color (white)
            3,                          # Thickness
            cv2.LINE_AA                 # Line type (anti-aliased)
        )

        cv2.circle(resized_frame, (x_pixel, y_pixel), 15, (0,255,0), -1)

        cv2.imshow("Algoritm Recunoastere Video", resized_frame)

        if cv2.waitKey(30) == 27:
            break

cap.release()
cv2.destroyAllWindows()
