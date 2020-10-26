#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import wiringpi

class Tile(Thread):
    def __init__(self, pins, isLong, isFirst, isLast, fileMap): 
        Thread.__init__(self)
        self.pins = pins
        self.isLong = isLong
        self.isFirst = isFirst
        self.isLast = isLast
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

    def __writePrimaryShort(self):
        wiringpi.softPwmWrite(self.pins[0], 255) # Primary blue
        wiringpi.softPwmWrite(self.pins[1], 0) # Primary green
        wiringpi.softPwmWrite(self.pins[2], 0) # Secondary green

    def __writeSecondaryShort(self):
        wiringpi.softPwmWrite(self.pins[0], 0) # Primary blue
        wiringpi.softPwmWrite(self.pins[1], 0) # Primary green
        wiringpi.softPwmWrite(self.pins[2], 255) # Secondary green

    def run(self):
        '''Start the gradient on each leds'''
        if self.isLong == False:
            self.__writeSecondaryShort()
            wiringpi.delay(self.map.tempo)
            self.__writePrimaryShort()
            
            # Reset leds after a delay
            wiringpi.delay(self.map.tempo)
            wiringpi.softPwmWrite(self.pins[0], 0) # Reset the red pin
            wiringpi.softPwmWrite(self.pins[1], 0) # Reset the green pin
            wiringpi.softPwmWrite(self.pins[2], 0) # Reset the blue pin
        else:
            if self.isFirst:
                # Allume la led tampon
                wiringpi.softPwmWrite(self.pins[2], 255) # Secondary green
            elif self.isLast:
                # Allume uniquement la led finale
                wiringpi.softPwmWrite(self.pins[1], 255) # Primary green

                # Reset leds after a delay
                wiringpi.delay(self.map.tempo)
                wiringpi.softPwmWrite(self.pins[0], 0) # Reset the red pin
                wiringpi.softPwmWrite(self.pins[1], 0) # Reset the green pin
                wiringpi.softPwmWrite(self.pins[2], 0) # Reset the blue pin
            else:
                # Allume les deux leds
                wiringpi.softPwmWrite(self.pins[1], 255) # Primary green
                wiringpi.softPwmWrite(self.pins[2], 255) # Secondary green
                