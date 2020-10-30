#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from threading import Thread
from board_manager import STATE_HIGH, STATE_LOW

class Tile(Thread):
    '''A class used ot represent a tile on the keyboard
    
    This class use a thread to light up the LEDs
    '''

    def __init__(self, pins, isLong, isFirst, isLast, fileMap):
        '''
        Parameters
        ----------
        pins : int[]
            The pins of the tile
        isLong : bool
            If the tile is a long one (a 2 ion the file)
        isFirst : bool, optional
            If the tile is the first of the serie (Used only for long tiles)
        isLast : bool, optional
            If the tile is the last of the serie (Used only for long tiles)
        fileMap : MusicMap
            The current music map
        '''
        Thread.__init__(self)
        self.pins = pins
        self.isLong = isLong
        self.isFirst = isFirst
        self.isLast = isLast
        self.map = fileMap

    def run(self):
        '''Handle the display of a pair of LEDs'''
        if self.isLong:
            self.__handleLongTile()
        else:
            self.__handleShortTile()

    def __handleShortTile(self):
        '''Handle the animation of a short tile'''
        self.__writeSecondaryShort()
        time.sleep(self.map.tempo / 1000)
        self.__writePrimaryShort()
        
        self.__resetLedsAfterDelay(self.map.tempo / 1000)

    def __handleLongTile(self):
        '''Handle the animation of a short tile
        
        If the tile is the first of the serie, light up the green one (the one connected with 2 pins)
        If the tile is the last of the serie, light up the blue one (the one connected with 3 pins)
        else all the leds of the tile will be on        
        '''
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
        '''Turn off all the leds after one measure'''
        # Reset leds after a delay
        time.sleep(self.map.tempo / 1000)
        self.map.boardManager.write(self.pins[0], STATE_HIGH) # Reset the red pin
        self.map.boardManager.write(self.pins[1], STATE_HIGH) # Reset the green pin
        self.map.boardManager.write(self.pins[2], STATE_HIGH) # Reset the blue pin

    def __writePrimaryShort(self):
        '''Turn on the first led to blue and turn off the second one'''
        self.map.boardManager.write(self.pins[0], STATE_LOW) # Primary blue
        self.map.boardManager.write(self.pins[1], STATE_HIGH) # Primary green
        self.map.boardManager.write(self.pins[2], STATE_HIGH) # Secondary green

    def __writeSecondaryShort(self):
        '''Turn on the second led to green and turn off the first one'''
        self.map.boardManager.write(self.pins[0], STATE_HIGH) # Primary blue
        self.map.boardManager.write(self.pins[1], STATE_HIGH) # Primary green
        self.map.boardManager.write(self.pins[2], STATE_LOW) # Secondary green