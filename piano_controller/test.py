#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wiringpi

wiringpi.wiringPiSetupPhys()

wiringpi.pinMode(7, 1) # Defining the pin as an output

wiringpi.digitalWrite(7, 1)

wiringpi.delay(1000)

wiringpi.digitalWrite(7, 0)
