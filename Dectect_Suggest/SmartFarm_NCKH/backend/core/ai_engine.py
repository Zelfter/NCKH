import cv2
from ultralytics import YOLO


class SmartFarmAI:
    def __init__(self, model_path="models/weights/best.pt"):
        try:
            self.model = YOLO(model_path)
            # 5 nhãn AI
            self.classes = ['healthy', 'leaf_blight', 'leaf_rust', 'leaf_spot', 'powdery_mildew']
        except Exception as e:
            print(f"Lỗi tải mô hình AI: {e}")

    def detect_plant(self, frame):
        # Chạy nhận diện với ngưỡng tin cậy 0.5
        results = self.model(frame, conf=0.5, verbose=False)[0]
        
        detections = []
        # Mặc định là khỏe mạnh nếu không thấy bệnh
        primary_label = 'healthy' 
        
        for box in results.boxes:
            cls_id = int(box.cls[0])
            primary_label = self.classes[cls_id]
            conf = float(box.conf[0])
            
            # Vẽ Bounding Box trực tiếp lên frame
            coords = box.xyxy[0].cpu().numpy().astype(int)
            cv2.rectangle(frame, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 2)
            cv2.putText(frame, f"{primary_label} ({conf:.2f})", (coords[0], coords[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            detections.append({"label": primary_label, "confidence": conf})
            
        return primary_label, frame