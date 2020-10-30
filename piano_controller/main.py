#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing as mp
import rtmidi

from music.musicMap import MusicMap
from board_manager import BoardManager
from enums.MappedMidiInput import MappedMidiInput

DEBUG_MODE = True

midiin = rtmidi.RtMidiIn()

def initializeBoard():
    '''
    Create a new board manager and add the MS23017 to it
    '''
    manager = BoardManager()

    # Add the component located at the 0x27 address (You can find the address with the "i2cdetect -y 1" command)
    manager.add(0x27)

    return manager

def startGame():
    '''
    Initialize the music map and start the game
    '''
    manager = initializeBoard()

    myMap = MusicMap(manager, "/LettreEliseStart.txt") # Initialize the map

    keyboard = [
        [
            0, # Bleu
            1, # Vert principal
            2 # Vert secondaire
        ]
        # [3, 4, 5]
    ]

    myMap.startSignal(keyboard) # Notify the user that the game will start 
 
    myMap.start(keyboard) # Begin the music map

if __name__ == "__main__":
    '''
    Check for MIDI inputs and launch the game if the P1 key is pressed on the keyboard
    '''
    ports = range(midiin.getPortCount())
    if ports:
        midiin.openPort(1)
        while True:
            m = midiin.getMessage(250) # some timeout in ms
            if m and m.isNoteOn() and m.getMidiNoteName(m.getNoteNumber()) == MappedMidiInput.get("P1"):
                startGame()
                if DEBUG_MODE == True:
                    break
    else:
        print('NO MIDI INPUT PORTS!')

