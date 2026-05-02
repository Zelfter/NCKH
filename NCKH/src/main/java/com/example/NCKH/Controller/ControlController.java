package com.example.NCKH.Controller;


import com.example.NCKH.DTO.MultiSensorControl;
import com.example.NCKH.DTO.SensorControl;
import com.example.NCKH.DTO.SensorData;
import com.example.NCKH.Service.MqttPublisherService;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
public class ControlController {

    private final MqttPublisherService mqttService;

    public ControlController(MqttPublisherService mqttService) {
        this.mqttService = mqttService;
    }

    @CrossOrigin(origins = "*")
    @PostMapping("/sensor-control")
    public String control(@RequestBody Map<String, Integer> request) {

        mqttService.publishControls(request);

        return "OK";
    }
    @PostMapping("/control-data")
    @ResponseBody
    public SensorControl getControlData() {
        return new SensorControl("all",1);
    }
}