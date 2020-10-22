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
            print("Pin " + str(pin) + " connected")
        
        # self.resetState()

    def resetState(self):
        for pin in self.pins:
            wiringpi.softPwmWrite(pin, 0) # Resetting the state of the pin

    def __fade(self, pin, range, delay):
        '''Fade the light of the specified led pin within the specified range'''
        print("Beginning fade on the pin " + str(pin))
        for brightness in range:
            wiringpi.softPwmWrite(pin, brightness) # Red pin
            wiringpi.delay(10)
        print("Ending fade on the pin " + str(pin))

    def run(self, tempo, isLong): 
        '''Start the gradient on each leds'''
        delay = (float((255 * 2)) / tempo) / 2
        print("=======================")
        self.__fade(self.pins[0], reversed(range(0, 255)), delay)
        self.__fade(self.pins[1], range(0, 255), delay)

        # print(isLong == False)
        # if isLong == False:
        print(self.pins)
        wiringpi.softPwmWrite(self.pins[0], 0) # Reset the red pin
        wiringpi.softPwmWrite(self.pins[1], 0) # Reset the green pin
        wiringpi.softPwmWrite(self.pins[2], 255) # Turn on the blue pin
        # else:
        #     wiringpi.softPwmWrite(self.pins[0], 255) # Reset the red pin
        #     wiringpi.softPwmWrite(self.pins[1], 0) # Reset the green pin
        #     wiringpi.softPwmWrite(self.pins[2], 255) # Turn on the blue pin

