#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiringpi

wiringpi.wiringPiSetupPhys()

class Tile:
    def __init__(self, pins): 
        self.pins = pins
        for _, pin in enumerate(pins):
            wiringpi.pinMode(pin, 1)
            wiringpi.softPwmCreate(pin, 0, 255)

    def run(self): 
        for brightness in range(0,100): # Going from 0 to 100 will give us full off to full on
            wiringpi.softPwmWrite(self.pins[0], brightness) # Change PWM duty cycle
            wiringpi.delay(10) # Delay for 0.2 seconds
        for brightness in reversed(range(0,100)):
            wiringpi.softPwmWrite(self.pins[0], brightness)
            wiringpi.delay(10)
