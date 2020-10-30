#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing as mp
import rtmidi

from music.musicMap import MusicMap
from board_manager import BoardManager
from enums.MappedMidiInput import MappedMidiInput

DEBUG_MODE = True

midiin = rtmidi.RtMidiIn()

def startGame():
    manager = BoardManager()
    manager.add(0x27)

    myMap = MusicMap(manager, "/LettreEliseStart.txt")
    keyboard = [
        [
            0, # Bleu
            1, # Vert principal
            2 # Vert secondaire
        ]
        # [3, 4, 5]
    ]

    myMap.startSignal(keyboard)

    myMap.start(keyboard)

if __name__ == "__main__":
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

