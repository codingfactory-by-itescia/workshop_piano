#!/usr/bin/env python
# -*- coding: utf-8 -*-

import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)

STATE_LOW = False
STATE_HIGH = True

class BoardManager():
    '''A class used to manage the pins of all the MCP23017 components
    Attributes
    ----------
    boards : MCP23017[]
        This array contain all the MCP23017 instances to interact with all the leds
    '''
    boards = []

    def add(self, address):
        '''
        Add a new MCP23017 to the global board
        Parameters
        ----------
        address: str
            The address on the i2c interface (can be found by using the "i2cdetect -y 1" command)
        '''
        mcp = MCP23017(i2c, address=address)
        
        # Initialize all the LEDs with a HIGH signal (because the leds we use are common cathode ones)
        self.__initializePins(mcp, STATE_HIGH)

        self.boards.append(mcp)

    def __initializePins(self, mcp, defaultState):
        '''Init the 15 pins of the MCP23017 to the specified state
        Parameters
        ----------
        mcp : MCP23017
        defaultState : bool
            The state of the pin (can be STATUS_HIGH = True or STATUS_LOW = False)
        '''
        # Set all pins to HIGH by default
        for pinNumber in range(15):
            pin = mcp.get_pin(pinNumber)
            pin.switch_to_output(value=True)
            pin.value = defaultState

    def write(self, pinNumber, state):
        '''Write a new state on a led
        Parameters
        ----------
        pinNumber : int
            The number of the pin who will be written. This number is a value between 0 and the total number of pins - 1 (eg. 3 = Board 1 Pin GPA3, 18 = Board 2, GPA2... )            
        state : bool
            The new state of the pin (can be STATUS_HIGH = True or STATUS_LOW = False)
        '''
        if pinNumber < 0 or pinNumber > (len(self.boards) * 16) - 1:
            raise Exception("The pin number is out of range !")
        
        boardNumber = self.__getInRange(pinNumber)
        board = self.boards[boardNumber]
        pin = board.get_pin(pinNumber)
        pin.value = state

    def __getInRange(self, pinNumber):
        '''
        Parameters
        ----------
        pinNumber : int
            The number of the pin on the global board
        '''
        for boardIndex, _ in enumerate(self.boards):
            start_bound = boardIndex * 16
            end_bound = ((boardIndex + 1) * 16) - 1
            if pinNumber > start_bound and pinNumber < end_bound:
                return boardIndex
        return 0
        