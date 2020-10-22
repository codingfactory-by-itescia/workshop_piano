#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiringpi

wiringpi.wiringPiSetupPhys()

class Tile:
    def __init__(self, pins): 
        self.pins = pins
        self.__initPins()

    def __initPins(self):
        '''Initialize the pins specified in the constructor in output mode with the softpwm mode enabled'''
        print("=======================")
        for _, pin in enumerate(self.pins):
            print("Connecting the pin " + str(pin) + "...")
            wiringpi.pinMode(pin, 1) # Defining the pin as an output
            wiringpi.softPwmCreate(pin, 0, 255) # The pin is now a PWM pin
            wiringpi.softPwmWrite(pin, 0) # Resetting the state of the pin
            print("Pin " + str(pin) + " connected")

    def __fade(self, pin, range):
        '''Fade the light of the specified led pin within the specified range'''
        print("Beginning fade on the pin " + str(pin))
        for brightness in range:
            wiringpi.softPwmWrite(pin, brightness) # Red pin
            wiringpi.delay(10) # Delay for 0.2 seconds
        print("Ending fade on the pin " + str(pin))

    def run(self): 
        '''Start the gradient on each leds'''
        print("=======================")
        self.__fade(self.pins[0], reversed(range(0, 255)))
        self.__fade(self.pins[1], range(0, 255))

        wiringpi.softPwmWrite(self.pins[0], 0) # Reset the red pin
        wiringpi.softPwmWrite(self.pins[1], 0) # Reset the green pin
        wiringpi.softPwmWrite(self.pins[2], 255) # Turn on the blue pin
