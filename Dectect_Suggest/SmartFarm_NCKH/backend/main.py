from fastapi import FastAPI, requests
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import time
import random
from core.ai_engine import SmartFarmAI
from core.expert_logic import get_expert_recommendation

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "models", "weights", "best.pt")
# KHÔNG dùng ".." nữa


app = FastAPI(title="Smart Farm API - HaUI")

# Cho phép Frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_engine = SmartFarmAI(model_path)

# Biến toàn cục lưu trữ trạng thái khuyến nghị để Frontend lấy
current_recommendation = "Đang khởi tạo hệ thống..."

def get_mock_iot_data():
    """Giả lập dữ liệu từ ESP32"""
    return {
        "deviceId": "esp32-01",
        "temperature": round(random.uniform(28.0, 36.0), 1),
        "humidity": random.randint(50, 90),
        "soilMoisture": random.randint(300, 600),
        "light": random.randint(700, 1000),
        "timestamp": int(time.time())
    }

import requests

# def get_mock_iot_data():
#     """Lấy dữ liệu thật từ Java backend"""
#     try:
#         response = requests.get("http://localhost:8080/sensor-data")

#         if response.status_code == 200:
#             return response.json()
#         else:
#             print("API error:", response.status_code)
#             return None

#     except Exception as e:
#         print("Connection error:", e)
#         return None


@app.get("/api/iot")
async def get_iot():
    iot_data = get_mock_iot_data()
    return {
        "iot": iot_data,
        "recommendation": current_recommendation
    }

def generate_video_stream():
    global current_recommendation
    cap = cv2.VideoCapture(0) # Mở camera
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
                
            # Lấy dữ liệu IoT hiện tại
            iot_data = get_mock_iot_data()
            
            # Chạy AI nhận diện
            ai_label, processed_frame = ai_engine.detect_plant(frame)
            
            # Kết hợp AI + IoT để ra quyết định
            current_recommendation = get_expert_recommendation(ai_label, iot_data)
            
            # Nén frame để gửi qua web
            _, buffer = cv2.imencode('.jpg', processed_frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    finally:
        # CỰC KỲ QUAN TRỌNG: Tắt hẳn camera khi người dùng ngắt kết nối
        cap.release()

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 cho phép tất cả các thiết bị trong mạng Wi-Fi truy cập vào
    uvicorn.run(app, host="0.0.0.0", port=8000)