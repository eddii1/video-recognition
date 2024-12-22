import cv2
import mediapipe as mp
import math


def calculare_unghi(a, b, c):

    # cream vectorii ab , bc
    ab = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    # produs scalar
    prod_scalar = ab[0] * bc[0] + ab[1] * bc[1]

    # modulul vectorilor
    modul_ab = math.sqrt(ab[0] ** 2 + ab[1] ** 2)
    modul_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    if modul_ab == 0 or modul_bc == 0:
        return 0.0

    cos_unghi = prod_scalar / (modul_ab * modul_bc)
    cos_unghi = max(-1.0, min(1.0, cos_unghi))

    unghi = math.degrees(math.acos(cos_unghi))
    return unghi


cap = cv2.VideoCapture("test2.mp4")
ret, frame = cap.read()

original_height, original_width, channels = frame.shape
aspect_ratio = original_height / original_width

new_width = 1440
new_height = int(new_width * aspect_ratio)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

fps = cap.get(cv2.CAP_PROP_FPS)
frame_duration = 1 / fps
under_90_seconds = 0.0
over_90_seconds = 0.0

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
            # mp_drawing.draw_landmarks(
            #     resized_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            # )
            landmarks = results.pose_landmarks.landmark

            cv2.circle(resized_frame, (int(
                landmarks[13].x * new_width), int(landmarks[13].y * new_height)), 15, (0, 255, 0), -1)

            umar = (landmarks[11].x * new_width, landmarks[11].y * new_height)
            cot = (landmarks[13].x * new_width, landmarks[13].y * new_height)
            incheietura = (landmarks[15].x * new_width,
                           landmarks[15].y * new_height)

            unghi = calculare_unghi(umar, cot, incheietura)

            if unghi < 90:
                under_90_seconds += frame_duration
            else:
                over_90_seconds += frame_duration

            cv2.putText(
                resized_frame,
                f"Unghi: {int(unghi)}",
                (50, 100),
                cv2.FONT_HERSHEY_COMPLEX,
                1.5,
                (255, 255, 255),
                3,
                cv2.LINE_AA
            )

            cv2.putText(
                resized_frame,
                f"< 90 grade: {int(under_90_seconds)}",
                (50, 150),
                cv2.FONT_HERSHEY_COMPLEX,
                1.5,
                (255, 255, 255),
                3,
                cv2.LINE_AA
            )

            cv2.putText(
                resized_frame,
                f"> 90 grade: {int(over_90_seconds)}",
                (50, 200),
                cv2.FONT_HERSHEY_COMPLEX,
                1.5,
                (255, 255, 255),
                3,
                cv2.LINE_AA
            )

        cv2.imshow("Algoritm Recunoastere Video", resized_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
