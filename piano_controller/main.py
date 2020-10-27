#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing as mp
import wiringpi
import rtmidi

from music.musicMap import MusicMap
from enums.MappedMidiInput import MappedMidiInput

DEBUG_MODE = True

wiringpi.wiringPiSetupPhys()

midiin = rtmidi.RtMidiIn()

def startGame(midi):
    myMap = MusicMap("/LettreEliseStart.txt")
    keyboard = [
        [
            7, # Bleu
            8, # Vert principal
            10 # Vert secondaire
        ],
        [11, 12, 13]
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
                startGame(m)
                if DEBUG_MODE == True:
                    break
    else:
        print('NO MIDI INPUT PORTS!')

