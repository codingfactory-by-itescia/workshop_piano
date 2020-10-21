#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tile import Tile
from colour import Color

tile = Tile([7])

for time in range(0, 4):
    tile.run()