def get_expert_recommendation(ai_label: str, iot_data: dict) -> str:
    """
    Phân tích kết hợp giữa nhãn bệnh (AI) và dữ liệu môi trường (IoT)
    """
    temp = iot_data.get("temperature", 0)
    soil = iot_data.get("soilMoisture", 0)
    humid = iot_data.get("humidity", 0)

    # Trường hợp 1: Cây khỏe mạnh
    if ai_label == 'healthy':
        if soil < 400:
            return "Cảnh báo IoT: Đất quá khô (Soil < 400). Khuyến nghị: Bật hệ thống tưới nước ngay."
        elif temp > 35:
            return "Cảnh báo IoT: Nhiệt độ môi trường rất cao. Khuyến nghị: Bật quạt thông gió hoặc phun sương."
        return "Trạng thái tối ưu: Cây khỏe mạnh, điều kiện môi trường lý tưởng."

    # Trường hợp 2: Phát hiện bệnh lý
    else:
        advice = f"Cảnh báo AI: Phát hiện bệnh '{ai_label}'. "
        
        if ai_label == 'powdery_mildew' and humid > 80:
            advice += "Độ ẩm cao (>80%) làm nấm phấn trắng lây lan nhanh. Khuyến nghị: Giảm tưới, bật quạt gió và phun thuốc diệt nấm."
        elif ai_label in ['leaf_blight', 'leaf_spot']:
            advice += "Khuyến nghị: Cắt bỏ lá bệnh, cách ly và sử dụng thuốc bảo vệ thực vật phù hợp."
        elif ai_label == 'leaf_rust':
            advice += "Khuyến nghị: Phun thuốc trị rỉ sắt vào sáng sớm, tránh tưới nước trực tiếp lên lá."
        else:
            advice += "Khuyến nghị: Theo dõi sát sao và tham khảo chuyên gia nông nghiệp."
            
        return advice