#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import wiringpi

class Tile(Thread):
    def __init__(self, pins, isLong, fileMap): 
        Thread.__init__(self)
        self.pins = pins
        self.isLong = isLong
        self.map = fileMap
        self.__initPins()


    def __initPins(self):
        '''Initialize the pins specified in the constructor in output mode with the softpwm mode enabled'''
        for _, pin in enumerate(self.pins):
            wiringpi.pinMode(pin, 1) # Defining the pin as an output
            wiringpi.softPwmCreate(pin, 0, 255) # The pin is now a PWM pin

    def resetState(self):
        wiringpi.delay(150)
        for pin in self.pins:
            wiringpi.softPwmWrite(pin, 0) # Resetting the state of the pin

    def __fade(self, pin, range):
        '''Fade the light of the specified led pin within the specified range'''
        for brightness in range:
            wiringpi.softPwmWrite(pin, brightness) # Red pin
            wiringpi.delay(10)

    def run(self): 
        '''Start the gradient on each leds'''
        # delay = (float((255 * 2)) / self.map.tempo)
        # self.__fade(self.pins[0], reversed(range(0, 255)))
        # self.__fade(self.pins[1], range(0, 255))

        if self.isLong == False:
            wiringpi.softPwmWrite(self.pins[0], 0) # Reset the red pin
            wiringpi.softPwmWrite(self.pins[1], 0) # Reset the green pin
            wiringpi.softPwmWrite(self.pins[2], 255) # Turn on the blue pin
        else:
            wiringpi.softPwmWrite(self.pins[0], 0) # Reset the red pin
            wiringpi.softPwmWrite(self.pins[1], 120) # Reset the green pin
            wiringpi.softPwmWrite(self.pins[2], 125) # Turn on the blue pin

        # Reset leds after a delay
        wiringpi.delay(self.map.tempo)
        wiringpi.softPwmWrite(self.pins[0], 0) # Reset the red pin
        wiringpi.softPwmWrite(self.pins[1], 0) # Reset the green pin
        wiringpi.softPwmWrite(self.pins[2], 0) # Reset the blue pin
