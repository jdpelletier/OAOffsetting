import os
import platform

import ktl

if platform.system() == "Windows":
    os.system('cls')
else:
    os.system('clear')

dcs = ktl.Service('dcs')
instrument = dcs.read('INSTRUME')
instService = ktl.Service(instrument)
gscale = instService.read('gscale')

def wftel():
    dcs = ktl.Service('dcs')
    autresum = dcs.read('autresum')
    startTime = time.time()
    axestat = dcs.monitor('AXESTAT')
    ktl.waitfor(axestat == "tracking")
    active = dcs.read("AUTACTIV")
    if (active == 'no'):
        print("WARNING: guider not currently active.\n")
        return
    count = 0
    while(True):
        if autresum != dcs.read('autresum'):
            break
        count += 1
        if count >= 20:
            print("[wftel] WARNING: timeoutwaiting for AUTRESUM to increment\n\a")
            break
        time.sleep(1)
    count = 0
    while(true):
        autgo = dcs.read('autgo')
        if autgo.upper() == "RESUMEACK" or augo.upper() == "GUIDE":
            break
        count += 1
        if count >= 20:
            print("[wftel]WARNING: timeout waiting for AUTGO to be RESUMEACK or GUIDE\n\a")
            break
        time.sleep(1)
    elapsedTime = time.time() - startTime
    return elapsedTime

def gxy(x, y):
    tvxoff = self.dcs['tvxoff']
    tvyoff = self.dcs['tvyoff']
    tvxoff.write(x, rel2curr = 't')
    tvyoff.write(y, rel2curr = 't')
    elapsedTime = wftel()
    print("[gxy] wftel completed in %f sec" % elapsedTime)
    return True


def main():

    print('--------------------------------')
    print('--Guider Acquire tool started.--')
    print('--------------------------------\n\n\n')

    try:
        while(True):
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
            dy = gscale * (int(end[1]-start[1]))
            gxy(dx, dy)

    except KeyboardInterrupt:
        print('\n\nGuider Acquire ending...\n\n')

if __name__ == '__main__':
    main()
