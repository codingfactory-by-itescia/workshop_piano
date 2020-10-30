#!/usr/bin/env python
# -*- coding: utf-8 -*-

import board
import busio

from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

mcp = MCP23017(i2c, address=0x27)  # MCP23017 w/ A0 set

pin0 = mcp.get_pin(0)

# Setup pin0 as an output that's at a high logic level.
pin0.switch_to_output(value=True)
pin0.value = False