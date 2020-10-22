#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tile import Tile
from musicMap import MusicMap
from colour import Color

myMap = MusicMap("/LettreEliseStart.txt")

keyboard = [
    Tile([7, 8, 10]),
    Tile([11, 12, 13])
]

myMap.start(keyboard)

# Run a tile
# tile = Tile([7, 8, 10])
# tile.run()