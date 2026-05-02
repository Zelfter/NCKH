// const API_URL = 'http://localhost:8000/api/iot'; (Đây là API ban đầu)
const API_URL = 'http://192.168.1.209:8000/api/iot'; // Đây là local máy tính 

// API bên Java là: /sensor-data

async function updateDashboard() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        // 1. Cập nhật các thông số IoT
        document.getElementById('val-temp').innerText = `${data.iot.temperature}°C`;
        document.getElementById('val-humid').innerText = `${data.iot.humidity}%`;
        document.getElementById('val-soil').innerText = data.iot.soilMoisture;
        document.getElementById('val-light').innerText = data.iot.light;
        document.getElementById('device-id').innerText = data.iot.deviceId;

        // 2. Cập nhật khuyến nghị từ hệ chuyên gia
        const recText = data.recommendation;
        const recBox = document.getElementById('rec-box');
        const recDisplay = document.getElementById('recommendation-text');
        
        recDisplay.innerText = recText;

        // 3. Đổi màu thanh khuyến nghị nếu phát hiện bệnh hoặc cảnh báo
        if (recText.includes("Cảnh báo") || !recText.includes("khỏe mạnh")) {
            recBox.classList.add('is-warning');
        } else {
            recBox.classList.remove('is-warning');
        }

        // 4. Cập nhật thời gian hệ thống
        const date = new Date(data.iot.timestamp * 1000);
        document.getElementById('timestamp').innerText = date.toLocaleTimeString();

    } catch (error) {
        console.error("Không thể kết nối đến Backend:", error);
        document.getElementById('recommendation-text').innerText = "Lỗi kết nối Server...";
    }
}

// Cập nhật dữ liệu mỗi 1 giây
setInterval(updateDashboard, 1000);

// Khởi chạy ngay khi load trang
updateDashboard();

// Biến lưu trạng thái camera
let isCameraOn = false;

// ĐỊA CHỈ IP MÁY TÍNH CỦA BẠN (Cập nhật lại cho đúng)
const VIDEO_STREAM_URL = 'http://192.168.1.209:8000/video_feed'; 

function toggleCamera() {
    const btn = document.getElementById('toggle-cam-btn');
    const videoStream = document.getElementById('video-stream');
    const icon = btn.querySelector('i');
    const text = btn.querySelector('span');

    isCameraOn = !isCameraOn;

    if (isCameraOn) {
        // Hành động: Bật Camera
        videoStream.src = VIDEO_STREAM_URL; // Kết nối tới Backend
        videoStream.style.display = "block"; // Hiện khung hình
        
        // Đổi giao diện nút thành Báo Đỏ (Để tắt)
        btn.className = "btn-cam on";
        icon.className = "fas fa-video";
        text.innerText = "Tắt Camera";
    } else {
        // Hành động: Tắt Camera
        videoStream.src = ""; // Xóa link => Ngắt kết nối với Backend
        videoStream.style.display = "none"; // Ẩn khung hình
        
        // Đổi giao diện nút thành Xanh (Để bật)
        btn.className = "btn-cam off";
        icon.className = "fas fa-video-slash";
        text.innerText = "Bật Camera";
        
        // Trả lại trạng thái mặc định cho lời khuyên
        document.getElementById('recommendation-text').innerText = "Camera đã tắt. Chờ bật camera để phân tích AI...";
    }
}

function openControlPanel(flag, event) {
    if (event) event.stopPropagation();

    const area = document.getElementById("areaControl");
    const control = document.getElementById("control");

    if (flag === 1) {
        area.classList.add("show");
        control.classList.add("show");
    } else {
        area.classList.remove("show");
        control.classList.add("show");
    }
}
// Hàm gửi MQTT
    function sendMultipleControls(devices) {

        fetch("http://192.168.1.209:8080/sensor-control", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(devices)
        })
        .then(res => res.text())
        .then(data => console.log("Server:", data))
        .catch(err => console.error(err));
    }

    // Hàm delay để tránh gửi quá nhiều yêu cầu khi người dùng thay đổi nhanh các switch
    function debounce(func, delay) {
        let timer;

        return function (...args) {
            clearTimeout(timer);

            timer = setTimeout(() => {
                func.apply(this, args);
            }, delay);
        };
    }

    // Hàm delay trước khi gửi MQTT
    const sendControlDebounced = debounce(() => {
        sendMultipleControls(collectDevices());
    }, 1000);

    
    // bắt sự kiện switch
    function collectDevices(){

        const devices = {};
        
        document.querySelectorAll("#switches input[type=checkbox]:not(#all)")
        .forEach(sw => {
            devices[sw.id] = sw.checked ? 1 : 0;
        });
        
        return devices;
    }
    
    // gửi dữ liệu đến hàm delay
    document.querySelectorAll("#switches input[type='checkbox']").forEach(sw => {
        sw.addEventListener("change", function () {
            sendControlDebounced();
        });
    });
    
    //Xử lý việc đồng bộ giữa các nút điều khiển Acurator và nút all
    const allSwitch = document.getElementById("all");
    const switches = document.querySelectorAll("#switches input[type='checkbox']:not(#all)");

    // Khi bật/tắt ALL
    allSwitch.addEventListener("change", function () {
        switches.forEach(sw => {
            sw.checked = allSwitch.checked;
        });
    });

// Khi thay đổi từng switch con
    switches.forEach(sw => {
        sw.addEventListener("change", function () {
            // Kiểm tra xem tất cả có đang bật không
            const allChecked = [...switches].every(s => s.checked);

            // Nếu tất cả bật -> ALL bật
            // Nếu có ít nhất 1 cái tắt -> ALL tắt
            allSwitch.checked = allChecked;
        });
    });