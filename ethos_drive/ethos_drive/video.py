"""Optional video analysis. Bounding boxes do NOT imply known distance/speed."""
from .models import Observation

ALLOWED_LABELS = {"person", "bicycle", "car", "motorcycle", "bus", "truck", "traffic light", "stop sign"}

def analyze_video(path, max_frames=30, stride=15, model_name="yolov8n.pt"):
    try:
        import cv2
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Video mode requires: pip install -r requirements-video.txt") from exc
    model = YOLO(model_name)  # First use may download pretrained weights; internet may be needed.
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("Cannot open video. Try an MP4 with a supported codec.")
    frames = []
    frame_number = 0
    try:
        while len(frames) < max_frames:
            ok, frame = cap.read()
            if not ok:
                break
            if frame_number % stride == 0:
                result = model.predict(frame, verbose=False, conf=.25)[0]
                observations = []
                for box in result.boxes:
                    label = result.names[int(box.cls[0])]
                    if label in ALLOWED_LABELS:
                        observations.append(Observation(label, float(box.conf[0]), None, None, "video", tuple(float(v) for v in box.xyxy[0].tolist())))
                annotated = result.plot()
                frames.append((frame_number, observations, cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)))
            frame_number += 1
    finally:
        cap.release()
    return frames
