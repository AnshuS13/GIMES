from ultralytics import YOLO

print("Loading YOLO11 model...")

model = YOLO("yolo11n.pt")

print("Model loaded successfully!")

results = model("https://ultralytics.com/images/bus.jpg")

results[0].show()