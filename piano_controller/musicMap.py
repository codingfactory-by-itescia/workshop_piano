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
            for tileIndex, tileState in enumerate(line):
                if (tileIndex >= len(tiles)):
                    break

                if tileState == TileTypes.EMPTY:
                    pass
                elif tileState == TileTypes.SHORT:
                    tile = Tile(tiles[tileIndex], False, self)
                    tile.start()
                elif tileState == TileTypes.LONG:
                    tile = Tile(tiles[tileIndex], True, self)
                    tile.start()
            time.sleep((float(self.tempo) / 1000))
        

    def __readFile(self, filePath):
        file = open(BASE_FILEPATH + filePath, "r")
        self.tempo = int(file.readline())
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

    def __transformToColumns(self, lines):
        transformedLines = []
        
        for column in range(len(lines[0])):
            transformedLines.append([])
            for row, l in enumerate(lines):
                transformedLines[column].append(l[column])

        return transformedLines
        
    