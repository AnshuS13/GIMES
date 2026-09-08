import cv2
from ultralytics import YOLO
import time
import numpy as np

print("Loading YOLO11...")

model = YOLO("yolo11n.pt")

print("Opening video...")

cap = cv2.VideoCapture("crowd.mp4")

prev_time = time.time()

while True:

    success, frame = cap.read()

    if not success:
        break

    density_grid = np.zeros((3, 3), dtype=int)

    results = model(
        frame,
        classes=[0],
        conf=0.3,
        imgsz=960
    )

    person_count = len(results[0].boxes)

    zone_counts = [0] * 9

    annotated_frame = results[0].plot()

    for box in results[0].boxes:

        x1, y1, x2, y2 = box.xyxy[0]

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        frame_height, frame_width = frame.shape[:2]

        zone_width = frame_width // 3
        zone_height = frame_height // 3

        col = center_x // zone_width
        row = center_y // zone_height

        zone = row * 3 + col + 1

        zone_counts[zone - 1] += 1

        print(f"Zone: {zone}")

        cv2.circle(
            annotated_frame,
            (center_x, center_y),
            5,
            (0, 0, 255),
            -1
        )

        print(f"Center: ({center_x}, {center_y})")

        print(box.xyxy)

        print(box.cls)

        print(box.conf)

        print("----------------")

    print("Zone counts:", zone_counts)

    density_grid = np.array(zone_counts).reshape(3, 3)

    # Create 10-dimensional state vector
    vibration = 0.0

    state = np.append(density_grid.flatten(), vibration)

    print("State vector:", state)
    print("State shape:", state.shape)

    # Draw 3x3 density grid
    frame_height, frame_width = frame.shape[:2]

    zone_width = frame_width // 3
    zone_height = frame_height // 3

    for row in range(3):
        for col in range(3):

            zone = row * 3 + col + 1
            people = zone_counts[zone - 1]

        # Decide density level
            if people <= 2:
                density = "LOW"
            elif people <= 4:
                density = "MEDIUM"
            else:
                density = "HIGH"

                    # Choose color based on density
            if density == "LOW":
                color = (0, 255, 0)
            elif density == "MEDIUM":
                color = (0, 255, 255)
            else:
                color = (0, 0, 255)

        # Zone boundaries
            x1 = col * zone_width
            y1 = row * zone_height
            x2 = (col + 1) * zone_width
            y2 = (row + 1) * zone_height

        # Draw rectangle
            cv2.rectangle(
                annotated_frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

        # Display zone information
            text = f"Z{zone}: {people} - {density}"

            cv2.putText(
                annotated_frame,
                text,
                (x1 + 10, y1 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

    print("Density Grid:")
    print(density_grid)

    for row in range(3):

        for col in range(3):

            people = density_grid[row][col]

            if people <= 2:
                density = "LOW"

            elif people <= 4:
                density = "MEDIUM"

            else:
                density = "HIGH"

            zone = row * 3 + col + 1

            print(f"Zone {zone}: {people} people - {density}")

    cv2.putText(
        annotated_frame,
        f"People: {person_count}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.2f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("GIMES - YOLO11 Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()