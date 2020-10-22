#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from enums.TileTypes import TileTypes

BASE_FILEPATH = "./maps"

class MusicMap():
    lines = []

    def __init__(self, filePath):
        print("Retreiving the map content...")
        self.transformed_map = self.__readFile(filePath)
        print("Map loaded !")

    def start(self, tiles):
        for tile in tiles:
            tile.resetState()
            
        for index, line in enumerate(self.transformed_map):
            for tile, tileState in enumerate(line):
                if (tile >= len(tiles)):
                    continue

                if tileState == TileTypes.EMPTY:
                    tiles[tile].resetState()
                elif tileState == TileTypes.SHORT:
                    tiles[tile].run(self.tempo, False)
                elif tileState == TileTypes.LONG:
                    tiles[tile].run(self.tempo, True)
                else:
                    print("Invalid tile type in the map line " + str(index + 1))
            time.sleep(float(self.tempo / 1000))

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
        
    