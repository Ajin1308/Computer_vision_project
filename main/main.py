import cv2
import numpy as np
import time
from roboflow import Roboflow
from count_dribble import *
from draw_display import *


def main():
    cap = cv2.VideoCapture(r"main\WHATSAAP_ASSIGNMENT.mp4")
    rf = Roboflow(api_key="Fbj5tlim6K9fzD5s60Bg")
    project = rf.workspace("roboflowmodels").project("roboflow_models")
    model = project.version(1).model

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    previous_y = None
    is_dribbling = False
    dribble_count = 0
    previous_dribble_time = None
    dribble_times = []
    basketball_path = []

    while True:
        _, frame = cap.read()
        predictions = model.predict(frame, confidence=40, overlap=30).json()['predictions']
        
        # Calculate dribbles
        frame, previous_y, is_dribbling, dribble_count, previous_dribble_time, dribble_times, basketball_path = calculate_dribbles(
            predictions, model, frame, previous_y, is_dribbling, dribble_count, previous_dribble_time, dribble_times, basketball_path)
        
        # Draw basketball path and display dribble count and average dribble frequency
        frame = draw_display(frame, dribble_count, dribble_times, basketball_path)

        out.write(frame)
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


