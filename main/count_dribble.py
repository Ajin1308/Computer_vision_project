import cv2
import numpy as np
import time
from roboflow import Roboflow

# Function to calculate dribble count and average dribble frequency
def calculate_dribbles(predictions, model, frame, previous_y, is_dribbling, dribble_count, previous_dribble_time, dribble_times, basketball_path):
    for prediction in predictions:
        class_name = prediction['class']
        if class_name == 'Basketball':
            x, y, w, h = prediction['x'], prediction['y'], prediction['width'], prediction['height']
            confidence = prediction['confidence']
            x1 = x - (w/2)
            y1 = y - (h/2)
            x2 = x + (w/2)
            y2 = y + (h/2)
            box = ((x1, y1), (x2, y2))
            ball_pos = ((x1 + x2) / 2, (y1 + y2) / 2)
            
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            if previous_y is not None:
                velocity = ball_pos[1] - previous_y
                
                # Check for dribble motion
                if velocity > 0 and not is_dribbling:
                    is_dribbling = True
                    if previous_dribble_time:
                        dribble_interval = time.time() - previous_dribble_time
                        dribble_times.append(dribble_interval)
                    previous_dribble_time = time.time()
                elif velocity < 0 and is_dribbling:
                    dribble_count += 1
                    print("Total Dribbles:", dribble_count)
                    is_dribbling = False
            previous_y = ball_pos[1]
            
            basketball_path.append((int(ball_pos[0]), int(ball_pos[1])))

    return frame, previous_y, is_dribbling, dribble_count, previous_dribble_time, dribble_times, basketball_path