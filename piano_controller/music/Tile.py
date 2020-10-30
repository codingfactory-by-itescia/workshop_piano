#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from threading import Thread
from board_manager import STATE_HIGH, STATE_LOW

class Tile(Thread):
    def __init__(self, pins, isLong, isFirst, isLast, fileMap): 
        Thread.__init__(self)
        self.pins = pins
        self.isLong = isLong
        self.isFirst = isFirst
        self.isLast = isLast
        self.map = fileMap

    def run(self):
        if self.isLong:
            self.__handleLongTile()
        else:
            self.__handleShortTile()

    def __handleShortTile(self):
        self.__writeSecondaryShort()
        time.sleep(self.map.tempo / 1000)
        self.__writePrimaryShort()
        
        self.__resetLedsAfterDelay(self.map.tempo / 1000)

    def __handleLongTile(self):
        if self.isFirst:
            # Allume la led tampon
            self.map.boardManager.write(self.pins[2], STATE_LOW) # Secondary green
        elif self.isLast:
            # Allume uniquement la led finale
            self.map.boardManager.write(self.pins[0], STATE_LOW) # Primary blue
            self.map.boardManager.write(self.pins[1], STATE_LOW) # Primary green

            self.__resetLedsAfterDelay(self.map.tempo)
        else:
            # Allume les deux leds
            self.map.boardManager.write(self.pins[0], STATE_LOW) # Primary blue
            self.map.boardManager.write(self.pins[1], STATE_LOW) # Primary green

            self.map.boardManager.write(self.pins[2], STATE_LOW) # Secondary green

    def __resetLedsAfterDelay(self, delay):
        # Reset leds after a delay
        time.sleep(self.map.tempo / 1000)
        self.map.boardManager.write(self.pins[0], STATE_HIGH) # Reset the red pin
        self.map.boardManager.write(self.pins[1], STATE_HIGH) # Reset the green pin
        self.map.boardManager.write(self.pins[2], STATE_HIGH) # Reset the blue pin

    def __writePrimaryShort(self):
        self.map.boardManager.write(self.pins[0], STATE_LOW) # Primary blue
        self.map.boardManager.write(self.pins[1], STATE_HIGH) # Primary green
        self.map.boardManager.write(self.pins[2], STATE_HIGH) # Secondary green

    def __writeSecondaryShort(self):
        self.map.boardManager.write(self.pins[0], STATE_HIGH) # Primary blue
        self.map.boardManager.write(self.pins[1], STATE_HIGH) # Primary green
        self.map.boardManager.write(self.pins[2], STATE_LOW) # Secondary green