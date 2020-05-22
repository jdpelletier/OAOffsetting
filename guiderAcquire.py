import os
import platform

import ktl

from OAOUtil import getGscale

if platform.system() == "Windows":
    os.system('cls')
else:
    os.system('clear')

dcs = ktl.Service('dcs')
instrument = dcs.read('INSTRUME')
gscale = getScales(instrument.lower())

def main():

    print('--------------------------------')
    print('--Guider Acquire tool started.--')
    print('--------------------------------\n\n\n')

    try:
        while(True):
            try:
                startString = input('Enter the guider pixel coordinates of the target (no comma): ')
                start = startString.split()
                while len(start) != 2 or ',' in startString:
                    startString = input('Error: Enter input as x y (no comma): ')
                    start = startString.split()
                endString = input('Enter the destination guider pixel coordinates (no comma): ')
                end = endString.split()
                while len(end) != 2 or ',' in endString:
                    endString = input('Error: Enter input as x y (no comma): ')
                    end = endString.split()
                print("Sending star at %s to %s..." % (startString, endString))
                dx = gscale * (int(start[0])-int(end[0])
                dy = gscale * (int(end[1])-int(start[1]))
                gxy(dx, dy)
            except ValueError:
                print("\nWARNING: only enter numbers.\n")
                continue

    except KeyboardInterrupt:
        print('\n\nGuider Acquire ending...\n\n')

if __name__ == '__main__':
    main()
