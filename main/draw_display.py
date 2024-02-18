import cv2
import numpy as np
import time
from roboflow import Roboflow

# Function to draw basketball path and display dribble count and average dribble frequency
def draw_display(frame, dribble_count, dribble_times, basketball_path):
    cv2.putText(frame, "Dribbles: " + str(dribble_count), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    if dribble_times:
        avg_dribble_frequency = 1 / np.mean(dribble_times)
        cv2.putText(frame, f"Avg Dribble Frequency: {avg_dribble_frequency:.3f} Hz", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    if len(basketball_path) > 1:
        for i in range(1, len(basketball_path)):
            cv2.line(frame, basketball_path[i-1], basketball_path[i], (255, 0, 0), 2)

    return frame