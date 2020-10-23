#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing as mp
import wiringpi
from musicMap import MusicMap
from colour import Color

wiringpi.wiringPiSetupPhys()

myMap = MusicMap("/LettreEliseStart.txt")

keyboard = [
    [7, 8, 10],
    [11, 12, 13]
]

myMap.start(keyboard)