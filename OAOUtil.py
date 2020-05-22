import time
import datetime
from subprocess import Popen, PIPE
from pathlib import Path
import logging

import ktl

dcs = ktl.Service('dcs')

def gxy(x, y):
    tvxoff = dcs['tvxoff']
    tvyoff = dcs['tvyoff']
    tvxoff.write(x, rel2curr = 't')
    tvyoff.write(y, rel2curr = 't')
    print("Offset executed")
    elapsedTime = wftel()
    log = myLogger()
    log.info("[gxy] offset %f, %f in guider coordinates" % (x, y))
    print("[gxy] wftel completed in %f sec" % elapsedTime)
    return True

def nightpath():
    nightly = Path('/s')
    tel = ktl.read('dcs', 'TELESCOP')
    if tel == 'Keck I':
        nightly = nightly / 'nightly1'
    else:
        nightly = nightly / 'nightly2'
    date = datetime.datetime.utcnow()
    year, month, day = str(date.strftime("%y")), str(date.strftime("%m")), str(date.strftime("%d"))
    nightly = nightly / year / month / day
    return nightly

def checkNightpath():
    nightly = nightpath()
    return nightly.exists()

def getGscale(instrument):
    scale_dict = {'mosfire' : 0.164,
                  'lris' : 0.239,
                  'hires' : 0.086,
                  'osiris' : 0.1338,
                  'kcwi' : 0.184,
                  'nirc2' : 0.134,
                  'nirspec' : 0.207,
                  'esi' : 0.233,
                  'deimos' : 0.207,
                  'nires': 0.244}
    return scale_dict[instrument]

def myLogger():
    log = logging.getLogger('MyLogger')
    log.setLevel(logging.INFO)
    nightly = nightpath()
    nightly = nightly / 'instrumentOffsets'
    LogFileHandler = logging.FileHandler(nightly)
    LogFormat = logging.Formatter('%(asctime)s:%(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    LogFileHandler.setFormatter(LogFormat)
    log.addHandler(LogFileHandler)
    return log

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
