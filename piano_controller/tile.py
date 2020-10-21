#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wiringpi import wiringPiSetupPhys, pinMode, softPwmCreate

wiringPiSetupPhys()

class Tile:
    def __init__(self, pins): 
        self.pins = pins
        for _, pin in enumerate(pins):
            pinMode(pin, OUTPUT)
            softPwmCreate(pin, 0, 255)

    def run(): 
        for brightness in range(0,100): # Going from 0 to 100 will give us full off to full on
            softPwmWrite(self.pins[0], brightness) # Change PWM duty cycle
            delay(10) # Delay for 0.2 seconds
        for brightness in reversed(range(0,100)):
            softPwmWrite(self.pins[0], brightness)
            delay(10)
