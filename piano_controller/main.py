#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiringpi2

OUTPUT_MODE = 1

TILE_ONE = 7

wiringpi2.wiringPiSetup()

# Configuration
wiringpi2.pinMode(TILE_ONE, OUTPUT_MODE)
wiringpi2.softPwmCreate(TILE_ONE, 0, 255)

# Writing on the raspberry
wiringpi2.softPwmWrite(TILE_ONE, 125)