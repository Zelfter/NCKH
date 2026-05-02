package com.example.NCKH.Controller;

import com.example.NCKH.DTO.SensorData;
import org.springframework.web.bind.annotation.GetMapping;
//import org.springframework.web.bind.annotation.RestController;
import com.example.NCKH.Service.MqttSubscriberService;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.ResponseBody;


@Controller
public class SensorController {

//    @GetMapping("/home")
//    public String home(){
//        return "index";
//    }
    private final MqttSubscriberService mqttService;

    public SensorController(MqttSubscriberService mqttService) {
        this.mqttService = mqttService;
    }

    @GetMapping("/sensor-data")
    @ResponseBody
    public SensorData getSensorData() {
        return mqttService.getLatestData();
    }

}
