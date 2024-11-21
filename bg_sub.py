import cv2
import numpy as np

# Initialize background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

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

# Main video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for consistency
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply background subtraction
    fg_mask = bg_subtractor.apply(gray)

    # Initialize a blank mask for debugging hot zones
    hot_zone_debug = np.zeros_like(fg_mask)

    # Process each hot zone
    for zone in hot_zones:
        x, y, w, h = zone["coords"]
        # Extract the region of interest (ROI)
        roi = fg_mask[y:y + h, x:x + w]
        # Count non-zero pixels (motion)
        motion_level = cv2.countNonZero(roi)

        # Visualize motion level (debug)
        hot_zone_debug[y:y + h, x:x + w] = roi

        # Trigger action if motion exceeds threshold
        if motion_level > motion_threshold:
            print(f"{zone['name']} triggered!")

    # Draw hot zones on the original frame
    draw_hot_zones(frame, hot_zones)

    # Display the frames
    cv2.imshow("Hot Zones", frame)
    cv2.imshow("Foreground Mask", fg_mask)
    cv2.imshow("Hot Zone Debug", hot_zone_debug)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()