# Using mediapipe to detect hand
# Check if it is hand to be in the hot zone, if it is hand, then trigger action
# If it is not hand, then do not trigger action

import cv2
import numpy as np
import mediapipe as mp

# Initialize background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define the hot zones (Command areas)
hot_zones = [
    {"name": "Command 1", "coords": (50, 50, 200, 100)},  # x, y, w, h
    {"name": "Command 2", "coords": (50, 200, 200, 100)},
    {"name": "Command 3", "coords": (50, 350, 200, 100)}
]

# Threshold for motion detection
motion_threshold = 5000  # Number of changed pixels in the zone

# Function to draw hot zones
def draw_hot_zones(frame, zones):
    for zone in zones:
        x, y, w, h = zone["coords"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, zone["name"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# Check if a point is inside a rectangle
def is_point_in_rect(point, rect):
    x, y, w, h = rect
    return x <= point[0] <= x + w and y <= point[1] <= y + h

# Main video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally to disable mirroring
    frame = cv2.flip(frame, 1)  # Flip code 1 means flipping around the y-axis (horizontal flip)

    # Resize frame for consistency
    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Apply background subtraction
    fg_mask = bg_subtractor.apply(frame)

    # Detect hands using MediaPipe
    results = hands.process(rgb_frame)

    # Draw hot zones on the original frame
    draw_hot_zones(frame, hot_zones)

    # Process each detected hand
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the hand's bounding box
            x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * frame.shape[1])
            y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * frame.shape[0])
            x_max = int(max([lm.x for lm in hand_landmarks.landmark]) * frame.shape[1])
            y_max = int(max([lm.y for lm in hand_landmarks.landmark]) * frame.shape[0])

            # Center of the hand
            hand_center = ((x_min + x_max) // 2, (y_min + y_max) // 2)

            # Check if the hand center is inside any hot zone
            for zone in hot_zones:
                if is_point_in_rect(hand_center, zone["coords"]):
                    print(f"{zone['name']} triggered by hand!")

            # Draw the hand bounding box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            cv2.circle(frame, hand_center, 5, (255, 0, 0), -1)

    # Display the frames
    cv2.imshow("Hot Zones", frame)
    cv2.imshow("Foreground Mask", fg_mask)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()