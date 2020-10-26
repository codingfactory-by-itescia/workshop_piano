#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from enums.TileTypes import TileTypes
from tile import Tile

BASE_FILEPATH = "./maps"

class MusicMap():
    lines = []

    def __init__(self, filePath):
        self.transformed_map = self.__readFile(filePath)

    def start(self, tiles):
        for index, line in enumerate(self.transformed_map):
            for tileIndex, tileState in enumerate(reversed(line)):
                if (tileIndex >= len(tiles)):
                    break

                if tileState == TileTypes.SHORT:
                    self.__startTile(tiles[tileIndex], False)
                elif tileState == TileTypes.LONG:
                    self.__startTile(tiles[tileIndex], true)
            time.sleep((float(self.tempo) / 1000)) # Freeze the state for one measure
        
    def __startTile(self, pins, isLong):
        tile = Tile(pins, isLong, self)
        tile.start()

    def __readFile(self, filePath):
        file = open(BASE_FILEPATH + filePath, "r")
        self.tempo = self.__bpmToMs(int(file.readline()))
        lines = []
        for line in file:
            line = self.__transformToTileTypes(line.rstrip().split(","))
            lines.append(line)
        return lines

    def __transformToTileTypes(self, values):
        for index, value in enumerate(values):
            intValue = int(value)
            if intValue == 0:
                values[index] = TileTypes.EMPTY
            elif intValue == 1:
                values[index] = TileTypes.SHORT
            else:
                values[index] = TileTypes.LONG
        return values
 
    def __bpmToMs(self, tempo):
        return 60000 / tempo
    