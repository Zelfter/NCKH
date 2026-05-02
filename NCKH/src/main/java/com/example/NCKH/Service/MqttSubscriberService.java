package com.example.NCKH.Service;

import com.example.NCKH.DTO.SensorData;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.springframework.stereotype.Service;
import jakarta.annotation.PostConstruct;
import tools.jackson.databind.ObjectMapper;

@Service
public class MqttSubscriberService {

    private static final String BROKER = "tcp://192.168.1.209:1883";
    private static final String TOPIC = "esp32/hanangthai/sensor/data";

    private SensorData latestData; // lưu JSON mới nhất

    public SensorData getLatestData() {
        return latestData;
    }

    @PostConstruct
    public void init() {
        try {
            String clientId = "SpringBootClient_" + System.currentTimeMillis();
            MqttClient client = new MqttClient(BROKER, clientId);

            MqttConnectOptions options = new MqttConnectOptions();
            options.setCleanSession(true);

            client.connect(options);
            System.out.println("Connected to MQTT broker");

            ObjectMapper mapper = new ObjectMapper();
            client.subscribe(TOPIC, (topic, message) -> {
                try {
                    String payload = new String(message.getPayload());
                    System.out.println("Parsed: " + payload);
                    latestData = mapper.readValue(payload, SensorData.class);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}