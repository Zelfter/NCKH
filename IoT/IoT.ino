#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>     // xử lý JSON
#include <ESP32Servo.h>      // điều khiển servo
#include "DHT.h"

/* ---------- WIFI ---------- */
const char* ssid = "Zenos";
const char* password = "23072005";

/* ---------- MQTT ---------- */
const char* mqtt_server = "172.20.10.7";
const int mqtt_port = 1883;

// Topic publish & subscribe
#define PUB_TOPIC "esp32/hanangthai/sensor/data"
#define SUB_TOPIC "esp32/hanangthai/sensor/control"

/* ---------- PIN SENSOR ---------- */
#define MOISTURE_PIN 35
#define LDR_AO 34
#define LDR_DO 16
#define DHTPIN 4
#define DHTTYPE DHT11

/* ---------- PIN ACTUATOR ---------- */
#define RELAY_LIGHT 26   // relay đèn
#define RELAY_PUMP  27   // relay bơm
#define SERVO_PIN   25   // servo cửa

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);
Servo windowServo;

/* ---------- TRẠNG THÁI THIẾT BỊ ---------- */
int lightState = 0;
int pumpState = 0;
int windowState = 0;

/* ==================================================
                WIFI CONNECT
   -> Kết nối ESP32 vào mạng WiFi
================================================== */
void setup_wifi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

/* ==================================================
                MQTT CALLBACK
   -> Hàm này chạy khi ESP32 nhận dữ liệu từ MQTT
   -> Dùng để điều khiển relay và servo
================================================== */
void callback(char* topic, byte* payload, unsigned int length) {

  Serial.println("\n=== NHẬN LỆNH ĐIỀU KHIỂN ===");

  // chuyển payload sang string
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';

  Serial.print("JSON nhận: ");
  Serial.println(message);

  // parse JSON
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, message);

  if (error) {
    Serial.println("❌ Lỗi parse JSON");
    return;
  }

  /* --------- ĐIỀU KHIỂN ĐÈN --------- */
  if (doc.containsKey("light")) {
    lightState = doc["light"];
    digitalWrite(RELAY_LIGHT, lightState ? LOW : HIGH); 
    // relay active LOW
  }

  /* --------- ĐIỀU KHIỂN BƠM --------- */
  if (doc.containsKey("pump")) {
    pumpState = doc["pump"];
    digitalWrite(RELAY_PUMP, pumpState ? LOW : HIGH);
  }

  /* --------- ĐIỀU KHIỂN CỬA (SERVO) --------- */
  if (doc.containsKey("window")) {
    windowState = doc["window"];

    if (windowState == 1) {
      windowServo.write(90);   // mở cửa
    } else {
      windowServo.write(0);    // đóng cửa
    }
  }

  Serial.println("✅ Đã cập nhật thiết bị");
}

/* ==================================================
                MQTT RECONNECT
   -> Nếu mất kết nối MQTT sẽ tự reconnect
   -> Sau khi kết nối lại sẽ subscribe topic
================================================== */
void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting MQTT...");

    if (client.connect("ESP32_Sensor")) {
      Serial.println("connected");

      // subscribe để nhận lệnh điều khiển
      client.subscribe(SUB_TOPIC);
      Serial.println("Subscribed control topic");

    } else {
      Serial.print("failed, rc=");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

/* ==================================================
                        SETUP
================================================== */
void setup() {
  Serial.begin(115200);

  // input sensor
  pinMode(LDR_DO, INPUT);

  // output relay
  pinMode(RELAY_LIGHT, OUTPUT);
  pinMode(RELAY_PUMP, OUTPUT);

  // tắt relay ban đầu
  digitalWrite(RELAY_LIGHT, HIGH);
  digitalWrite(RELAY_PUMP, HIGH);

  // khởi tạo servo
  windowServo.attach(SERVO_PIN);
  windowServo.write(0);

  // khởi tạo DHT
  dht.begin();

  // kết nối wifi + mqtt
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);

  // gán hàm callback
  client.setCallback(callback);
}

/* ==================================================
                        LOOP
   -> Gửi dữ liệu sensor liên tục
   -> Nhận lệnh điều khiển từ MQTT
================================================== */
void loop() {

  // kiểm tra kết nối MQTT
  if (!client.connected()) {
    reconnect();
  }

  client.loop(); // xử lý nhận dữ liệu MQTT

  /* ---------- ĐỌC SENSOR ---------- */
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  int moisture = analogRead(MOISTURE_PIN);
  int ldrAnalog = analogRead(LDR_AO);
  int ldrDigital = digitalRead(LDR_DO);

  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT error");
    delay(2000);
    return;
  }

  unsigned long timestamp = millis() / 1000;

  /* ---------- TẠO JSON ---------- */
  char payload[256];
  snprintf(payload, sizeof(payload),
    "{"
      "\"deviceId\":\"esp32-01\","
      "\"temperature\":%.2f,"
      "\"humidity\":%.2f,"
      "\"soilMoisture\":%d,"
      "\"light\":%d,"
      "\"timestamp\":%lu"
    "}",
    temp,
    hum,
    moisture,
    ldrAnalog,
    timestamp
  );

  /* ---------- GỬI MQTT ---------- */
  client.publish(PUB_TOPIC, payload);

  Serial.println("\nPublished JSON:");
  Serial.println(payload);

  delay(2000);
}