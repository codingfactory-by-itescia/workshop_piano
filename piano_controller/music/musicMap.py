#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from enums.TileTypes import TileTypes
from music.Tile import Tile
from board_manager import STATE_HIGH, STATE_LOW

BASE_FILEPATH = "./maps"

class MusicMap():
    '''The representation of a music map in the program

    This class is used to parse the map file contained in the "maps" directory
    and to light up the needed leds by instanciating some Tile objects
    '''

    def __init__(self, boardManager, filePath):
        '''
        Parameters
        ----------
        boardManager : BoardManager
            The manager who will be used to light up the leds
        filePath : str
            The path of the parsed file
        '''
        self.transformed_map = self.__readFile(filePath)
        self.boardManager = boardManager

    def startSignal(self, tiles):
        '''Trigger the LED animation to notify the user of the beginning of the game 
        Parameters
        ----------
        tiles : int[][]
            The pins of all the leds connected to the Raspberry
        '''
        pins = list(map(lambda tilePins: tilePins[0], tiles)) # Get the blue pin in each tile
        for i in range(3):
            for pin in pins:
                self.boardManager.write(pin, STATE_LOW)
            time.sleep(0.5)
            for pin in pins:
                self.boardManager.write(pin, STATE_HIGH)
            time.sleep(0.5)
        
    def start(self, tiles):
        '''Start the game

        This method will instanciate a Tile when the note should be played on the LEDs

        Parameters
        ----------
        tiles : int[][]
            The pins of all the leds connected to the Raspberry
        '''
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
        '''Instanciate a new Tile who will be handle by a separated Thread

        Parameters
        ----------
        pins : int[]
            The pins of the tile
        isLong : bool
            If the tile is a long one (a 2 ion the file)
        isFirst : bool, optional
            If the tile is the first of the serie (Used only for long tiles)
        isLast : bool, optional
            If the tile is the last of the serie (Used only for long tiles)
        '''
        tile = Tile(pins, isLong, isFirst, isLast, self)
        tile.start()

    def __readFile(self, filePath):
        '''Read the map file and transform the numbers into TileTypes

        Parameters
        ----------
        filePath : str
            The path of the file to parse

        Returns
        -------
        lines
            The file lines transformed to TileTypes
        '''
        file = open(BASE_FILEPATH + filePath, "r")
        self.tempo = self.__bpmToMs(int(file.readline()))
        lines = []
        for line in file:
            line = self.__transformToTileTypes(line.rstrip().split(","))
            lines.append(line)
        return lines

    def __transformToTileTypes(self, values):
        '''Transform a line of numbers to a TileTypes array 
        Parameters
        ----------
        values : str[]
            The line values splitted

        Returns
        -------
        values :  TileTypes[]
            The line transformed to TileTypes
        '''
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
        '''Convert a bpm value to milliseconds
        tempo : int
            The tempo of the music
        '''
        return 60000 / tempo
    