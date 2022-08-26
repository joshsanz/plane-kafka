#!/usr/bin/env python3

# ./dump1090 --net | python ../share/pollandpicture.py

# Imports
import sys
import subprocess
import re
import time
import getopt
import os.path
from pprint import pprint
from datetime import datetime
from subprocess import call

# constants and globals
cDump1080 = "/home/pi/dump1090/dump1090"
cDump1080 = "/usr/local/bin/dump1090"
playback1090 = "python3 ./playback-dump1090.py -r 0.1 -f {}"
playbackFile = ""


def formNumber(pInputText):
    try:
        return float(pInputText.replace('\r', ''))
    except ValueError:
        return float(0)


def formText(pInputText):
    return pInputText.replace('\r', '')


def printStuff(pText):
    print("{:%Y%m%d %H:%M:%S} {}".format(datetime.now(), pText))


################################################################################
# Setup
textblock = ''
vDebugMode = 0
vSnapMode = 0

try:
    opts, args = getopt.getopt(sys.argv[1:], "vd:f:", ["verbose", "debug=", "file="])
except getopt.GetoptError:
    print('plane-kafka.py [-v|--verbose] [-d XX|--debug=] [-f PLAYBACK_FILE|--file=]')
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-d', '--debug'):
        vDebugMode = 1
        vDebugFile = arg
        if not os.path.isfile(vDebugFile):
            print("File {} does not exist".format(vDebugFile))
            sys.exit(2)
    elif opt in ('-v', '--verbose'):
        vVerboseMode = 1
    elif opt in ('-f', '--file'):
        playbackFile = arg

if vDebugMode == 0:
    if playbackFile:
        printStuff("Playing file {}...".format(playbackFile))
        print(playback1090.format(playbackFile))
        sproc = subprocess.Popen(playback1090.format(playbackFile), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        printStuff("Listening to live ADS-B...")
        sproc = subprocess.Popen(cDump1080, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
else:
    print('*** DEBUG MODE ***')
    sproc = subprocess.Popen('cat {}'.format(vDebugFile), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


# Create/clear log file for REST calls
call(["cp", "kafka_REST.log", "kafka_REST.log.old"])
call(["touch", "kafka_REST.log"])


################################################################################
# Begin main read loop

printStuff('Started')

while True:
    if vDebugMode == 1:
        time.sleep(.01)

    line = sproc.stdout.readline()
    textblock = textblock + line.decode("utf-8")
    if len(line) == 1:
        # Start of block of info
        searchICAO = re.search(r'(ICAO Address   : )(.*$)', textblock, re.M | re.I)
        searchFeet = re.search(r'(Altitude : )(.*)(feet)(.*$)', textblock, re.M | re.I)
        searchLatitude = re.search(r'(Latitude : )(.*$)', textblock, re.M | re.I)
        searchLongitude = re.search(r'(Longitude: )(.*$)', textblock, re.M | re.I)
        searchIdent = re.search(r'(Identification : )(.*$)', textblock, re.M | re.I)

        if searchICAO and searchIdent:
            valICAO = formText(searchICAO.group(2))
            valIdent = formText(searchIdent.group(2)).strip()
            printStuff('valICAO:{} valIdent:{}'.format(valICAO, valIdent))
            call(["./send_kafka", "ident-topic", valICAO, valIdent])
            # storeAndRefineICAOandCode(valICAO, valIdent)

        if searchFeet and searchICAO and searchLatitude and searchLongitude \
           and not ('not decoded' in searchLatitude.group(2)) \
           and not ('not decoded' in searchLongitude.group(2)):

            # Found a valid combination
            valICAO = formText(searchICAO.group(2))
            valFeet = formNumber(searchFeet.group(2))
            valLatitude = formNumber(searchLatitude.group(2))
            valLongitude = formNumber(searchLongitude.group(2))
            printStuff('valICAO:{} valFeet:{} valLatitude:{} valLongitude:{}'.format(valICAO, valFeet, (valLatitude), (valLongitude)))
            # ./send_kafka location-topic ico height location
            call(["./send_kafka", "location-topic", valICAO, "{}".format(valFeet), "{},{}".format(valLatitude, valLongitude)])
#            processSquark (valICAO, valFeet, (valLatitude), (valLongitude))

        # End of block of info
        textblock = ''
    # End of read of line

retval = sproc.wait()
