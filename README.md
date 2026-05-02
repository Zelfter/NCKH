# 🌱 Smart Farm Monitoring System (Web + IoT + AI)

## 📌 Giới thiệu

Smart Farm Monitoring System là một hệ thống giám sát và điều khiển nông trại thông minh, kết hợp **Web + IoT + AI** nhằm giúp người dùng theo dõi môi trường và điều khiển thiết bị từ xa một cách hiệu quả.

Hệ thống sử dụng **ESP32** để thu thập dữ liệu cảm biến và điều khiển thiết bị, kết hợp với **Web App** để hiển thị và thao tác, cùng với **AI** để phát hiện bất thường (ví dụ từ camera).

---

## ⚙️ Công nghệ sử dụng

### 🔌 IoT

* ESP32
* Cảm biến DHT (nhiệt độ, độ ẩm)
* Relay (điều khiển thiết bị)
* Servo SG90 (đóng/mở)
* Pump (tưới nước)

### 🌐 Backend

* Java (Spring Boot)
* Python (AI / xử lý video / camera streaming)
* MQTT (Pub/Sub communication)

### 💻 Frontend

* HTML, CSS, JavaScript
* Fetch API (gửi request)
* Responsive UI

---

## 🧩 Kiến trúc hệ thống

```
[ ESP32 ]
   ↓ (MQTT Publish)
[ MQTT Broker ]
   ↓
[ Backend (Java) ] ←→ [ AI Server (Python) ]
   ↓
[ Web App (Frontend) ]
```

---

## 🚀 Chức năng chính

### 📊 1. Giám sát môi trường

* Hiển thị nhiệt độ, độ ẩm từ cảm biến
* Cập nhật dữ liệu theo thời gian thực

### 🎥 2. Camera & AI

* Streaming video trực tiếp từ camera
* Phát hiện bất thường (AI cảnh báo)
* Hiển thị trạng thái cảnh báo trên UI

### 🎛️ 3. Điều khiển thiết bị

* Bật/tắt thiết bị (đèn, bơm nước, v.v.)
* Điều khiển servo (mở cửa, mái che)
* Có thể bật/tắt toàn bộ thiết bị

### ⚠️ 4. Hệ thống cảnh báo

* Hiển thị cảnh báo ở đầu trang
* Cảnh báo khi có bất thường từ AI hoặc cảm biến

### 📱 5. Giao diện người dùng

* Responsive (hỗ trợ mobile)
* Camera chiếm phần lớn diện tích
* Control panel có thể bật/tắt

---

## 🖥️ Cài đặt & chạy hệ thống

### 1. Clone project

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Chạy MQTT Broker

* Có thể dùng Mosquitto

```bash
mosquitto
```

### 3. Chạy Backend (Java)

```bash
cd backend
mvn spring-boot:run
```

### 4. Chạy AI Server (Python)

```bash
cd ai-server
pip install -r requirements.txt
python app.py
```

### 5. Chạy Frontend

* Dùng Live Server hoặc mở file HTML

```bash
cd frontend
```

---

## 🔗 API sử dụng

### 📤 Gửi điều khiển thiết bị

```
POST /sensor-control
Content-Type: application/json

{
  "device1": true,
  "device2": false
}
```

### 📥 Nhận dữ liệu cảm biến

* Qua MQTT topic (ví dụ):

```
sensor/data
```

---

## 📡 MQTT Topics

| Topic          | Mô tả               |
| -------------- | ------------------- |
| sensor/data    | Dữ liệu cảm biến    |
| device/control | Điều khiển thiết bị |
| warning        | Cảnh báo            |

---

## 🔧 Phần cứng đề xuất

* ESP32 DevKit
* Relay 2 kênh 5V
* DHT11/DHT22
* Servo SG90
* Mini Water Pump
* Camera (USB hoặc IP Camera)

---

## 📈 Hướng phát triển

* Thêm dashboard thống kê (biểu đồ)
* AI nâng cao (nhận diện sâu bệnh)
* Mobile App (Android/iOS)
* Tự động hóa (rule-based / AI)

---

## 👨‍💻 Tác giả

* Project phục vụ nghiên cứu (NCKH)

---

## 📄 License

MIT License

