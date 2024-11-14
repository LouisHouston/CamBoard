import cv2
import dlib
import numpy as np
from imutils import face_utils
from sounds import play_sound
from scipy.spatial import distance
import time


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
MOUTH = list(range(48, 68))  

def mouth_aspect_ratio(landmarks):
    A = distance.euclidean(landmarks[62], landmarks[66])
    B = distance.euclidean(landmarks[60], landmarks[64])
    
    C = distance.euclidean(landmarks[48], landmarks[54])
    
    mar = (A + B) / (2.0 * C)
    return mar

MAR_THRESHOLD = 0.6

# just to track the time of the last sound played
last_played_time = time.time()
sound_delay = 1

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        #eye tracking shapes
        left_eye = shape[36:42]
        right_eye = shape[42:48]
        
        # establishing default mouth shape for opening
        mar = mouth_aspect_ratio(shape)

        for (x, y) in shape[48:68]:
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        left_eye_center = left_eye.mean(axis=0)
        right_eye_center = right_eye.mean(axis=0)

        delta_x = right_eye_center[0] - left_eye_center[0]
        delta_y = right_eye_center[1] - left_eye_center[1]
        angle = np.degrees(np.arctan2(delta_y, delta_x))

        sound_name = "Nothing playing"
        current_time = time.time()
        

        if angle > 36:
            sound_name = "Bone Crack playing"
            if current_time - last_played_time >= sound_delay:
                last_played_time = current_time
                play_sound(1)
        if mar > MAR_THRESHOLD:
            if current_time - last_played_time >= sound_delay:
                play_sound(3)
                last_played_time = current_time
                sound_name = "Wowwww playing"
                cv2.putText(frame, "Mouth Wide Open!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                last_played_time = current_time
        if abs(angle) < 36 :  # Looking at camera
            if current_time - last_played_time >= sound_delay:
                last_played_time = current_time
                play_sound(2)
                sound_name = "BOOM playing"
                cv2.putText(frame, "BOOM", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                last_played_time = current_time

        
        cv2.putText(frame, f"Sound Playing: {sound_name} ", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        for (x, y) in left_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 255), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 255), -1)


    cv2.imshow("Camboard", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()