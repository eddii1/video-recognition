import cv2


# img = cv2.imread('example.jpg')
# while cv2.waitKey(10) != 27:
#     cv2.imshow('img', img)

cap = cv2.VideoCapture("test.mp4")
ret,frame = cap.read()

original_height, original_width, _ = frame.shape
aspect_ratio = original_height / original_width

new_width= 300
new_height= int(new_width * aspect_ratio)


if not cap.isOpened():
    print("Eroare: Nu putem deschide videoul.")
    exit()
else:
    while True:
        ret, frame=cap.read()

        if not ret:
            print("Finalul videoului || nu putem citi frame")
            break
        
        resized_frame=cv2.resize(frame, (new_width,new_height))
        cv2.imshow("Video Frame",resized_frame)

        if cv2.waitKey(30) == 27:
            break

cap.release()
cv2.destroyAllWindows()