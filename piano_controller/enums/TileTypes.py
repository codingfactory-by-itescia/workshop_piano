#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class TileTypes(Enum):
    '''An enum who represent a tile state on the map file

    EMPTY
        A 0 in the map file. Represent a tile who will not be instanciated
    SHORT
        A 1 in the map file. Represent a tile that will last one measure
    LONG
        A 2 in the map file. Represent a tile that will last more than one measure
    '''
    EMPTY = 0
    SHORT = 1
    LONG = 2