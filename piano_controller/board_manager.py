#!/usr/bin/env python
# -*- coding: utf-8 -*-

import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)

STATE_LOW = False
STATE_HIGH = True

class BoardManager():
    boards = []

    def add(self, address):
        mcp = MCP23017(i2c, address=address)
        
        # Set all pins to HIGH by default
        for pinNumber in range(15):
            pin = mcp.get_pin(pinNumber)
            pin.switch_to_output(value=True)
            pin.value = STATE_HIGH

        self.boards.append(mcp)

    def write(self, pinNumber, state):
        if pinNumber < 0 or pinNumber > (len(self.boards) * 16) - 1:
            raise Exception("The pin number is out of range !")
        
        boardNumber = self.__getInRange(pinNumber)
        board = self.boards[boardNumber]
        pin = board.get_pin(pinNumber)
        pin.value = state

    def __getInRange(self, pinNumber):
        for boardIndex, _ in enumerate(self.boards):
            start_bound = boardIndex * 16
            end_bound = ((boardIndex + 1) * 16) - 1
            if pinNumber > start_bound and pinNumber < end_bound:
                return boardIndex
        return 0
        