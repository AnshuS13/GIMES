import cv2
from ultralytics import YOLO
import time

print("Loading YOLO11...")

model = YOLO("yolo11n.pt")

print("Opening video...")

cap = cv2.VideoCapture("crowd.mp4")

prev_time = time.time()

while True:

    success, frame = cap.read()

    if not success:
        break

    results = model(
        frame,
        classes=[0],
        conf=0.3,
        imgsz=960
    )

    for box in results[0].boxes:

        print(box.xyxy)

        print(box.cls)

        print(box.conf)

        print("----------------")

    annotated_frame = results[0].plot()

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