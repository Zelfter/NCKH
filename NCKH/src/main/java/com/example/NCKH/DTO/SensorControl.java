package com.example.NCKH.DTO;


public class SensorControl {

    private String device;
    private int state;

    public SensorControl(String device, int state){
        this.device = device;
        this.state = state;
    }
    public String getDevice() {
        return device;
    }

    public void setDevice(String device) {
        this.device = device;
    }

    public int getState() {
        return state;
    }

    public void setState(int state) {
        this.state = state;
    }
}