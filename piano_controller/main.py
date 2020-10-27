#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing as mp
import wiringpi
import rtmidi

from musicMap import MusicMap

DEBUG_MODE = True

wiringpi.wiringPiSetupPhys()

midiin = rtmidi.RtMidiIn()

def startGame(midi):
    myMap = MusicMap("/LettreEliseStart.txt")
    keyboard = [
        [7, 8, 10],
        [11, 12, 13]
    ]
    myMap.start(keyboard)

if __name__ == "__main__":
    ports = range(midiin.getPortCount())
    if ports:
        midiin.openPort(1)
        while True:
            m = midiin.getMessage(250) # some timeout in ms
            if m and m.isNoteOn() and m.getMidiNoteName(m.getNoteNumber()) == "C1":
                startGame(m)
                if DEBUG_MODE == True:
                    break
    else:
        print('NO MIDI INPUT PORTS!')

