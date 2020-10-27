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

    def run(self):
        if self.isLong:
            self.__handleLongTile()
        else:
            self.__handleShortTile()

    def __handleShortTile(self):
        self.__writeSecondaryShort()
        wiringpi.delay(self.map.tempo)
        self.__writePrimaryShort()
        
        self.__resetLedsAfterDelay(self.map.tempo)

    def __handleLongTile(self):
        if self.isFirst:
            # Allume la led tampon
            wiringpi.softPwmWrite(self.pins[2], 255) # Secondary green
        elif self.isLast:
            # Allume uniquement la led finale
            wiringpi.softPwmWrite(self.pins[1], 255) # Primary green

            self.__resetLedsAfterDelay(self.map.tempo)
        else:
            # Allume les deux leds
            wiringpi.softPwmWrite(self.pins[1], 255) # Primary green
            wiringpi.softPwmWrite(self.pins[2], 255) # Secondary green

    def __resetLedsAfterDelay(self, delay):
        # Reset leds after a delay
        wiringpi.delay(self.map.tempo)
        wiringpi.softPwmWrite(self.pins[0], 0) # Reset the red pin
        wiringpi.softPwmWrite(self.pins[1], 0) # Reset the green pin
        wiringpi.softPwmWrite(self.pins[2], 0) # Reset the blue pin

    def __writePrimaryShort(self):
        wiringpi.softPwmWrite(self.pins[0], 255) # Primary blue
        wiringpi.softPwmWrite(self.pins[1], 0) # Primary green
        wiringpi.softPwmWrite(self.pins[2], 0) # Secondary green

    def __writeSecondaryShort(self):
        wiringpi.softPwmWrite(self.pins[0], 0) # Primary blue
        wiringpi.softPwmWrite(self.pins[1], 0) # Primary green
        wiringpi.softPwmWrite(self.pins[2], 255) # Secondary green