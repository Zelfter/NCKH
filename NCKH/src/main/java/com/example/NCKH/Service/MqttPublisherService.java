package com.example.NCKH.Service;

import com.example.NCKH.DTO.MultiSensorControl;
import com.example.NCKH.DTO.SensorControl;
import org.eclipse.paho.client.mqttv3.*;
import org.springframework.stereotype.Service;
import tools.jackson.databind.ObjectMapper;

import java.util.HashMap;
import java.util.Map;


@Service
public class MqttPublisherService {

    private static final String BROKER = "tcp://192.168.1.209:1883";
    private static final String TOPIC = "esp32/hanangthai/sensor/control";

    private MqttClient client;

    public MqttPublisherService() throws Exception {
        client = new MqttClient(BROKER, MqttClient.generateClientId());
        client.connect();
    }

    public void publishControls(Map<String, Integer> payloadMap) {

        try {
            ObjectMapper mapper = new ObjectMapper();
            String payload = mapper.writeValueAsString(payloadMap);

            MqttMessage message = new MqttMessage(payload.getBytes());
            client.publish(TOPIC, message);

            System.out.println("Sent MQTT: " + payload);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
