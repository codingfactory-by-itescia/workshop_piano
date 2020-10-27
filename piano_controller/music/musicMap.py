#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import wiringpi
from enums.TileTypes import TileTypes
from Tile import Tile

BASE_FILEPATH = "./maps"

class MusicMap():
    lines = []

    def __init__(self, filePath):
        self.transformed_map = self.__readFile(filePath)

    def startSignal(self, tiles):
        pins = map(lambda tilePins: tilePins[0], tiles) # Get the blue pin in each tile
        for i in range(3):
            for pin in pins:
                wiringpi.pinMode(pin, 1)
                wiringpi.digitalWrite(pin, 1)
            wiringpi.delay(500)
            for pin in pins:
                wiringpi.digitalWrite(pin, 0)
            wiringpi.delay(500)
        
    def start(self, tiles):
        for index, line in enumerate(self.transformed_map):
            for tileIndex, tileState in enumerate(line):
                if (tileIndex >= len(tiles)):
                    break

                if tileState == TileTypes.SHORT:
                    self.__startTile(tiles[tileIndex], False)
                elif tileState == TileTypes.LONG:
                    previousIndex = index - 1
                    isFirst = self.transformed_map[previousIndex][tileIndex] != TileTypes.LONG if index - 1 >= 0 else True
                    
                    nextIndex = index + 1
                    isLast = self.transformed_map[nextIndex][tileIndex] != TileTypes.LONG if nextIndex < len(self.transformed_map) else True
                    self.__startTile(tiles[tileIndex], True, isFirst, isLast)
            time.sleep((float(self.tempo) / 1000)) # Freeze the state for one measure
        
    def __startTile(self, pins, isLong, isFirst = False, isLast = False):
        tile = Tile(pins, isLong, isFirst, isLast, self)
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
    