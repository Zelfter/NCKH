package com.example.NCKH.DTO;

import java.util.List;

public class MultiSensorControl {

    private List<SensorControl> devices;

    public List<SensorControl> getDevices() {
        return devices;
    }

    public void setDevices(List<SensorControl> devices) {
        this.devices = devices;
    }
}
