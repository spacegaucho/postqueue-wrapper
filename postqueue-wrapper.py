#!/usr/bin/python2.7 -B
# FOR NOW THIS IS HOW TO DELETE EMAILS:
# for i in $(./postqueue-wrapper.py -c /etc/postfix-legacy-df01/  -s "<stringToDelete>"); do postsuper -d $i -c <postfixConfDir>; done
# FIXME: make functions, test if rawInput out of range

import sys
import os
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog -c <config> [-s <search>] [-v] ")
parser.add_option("-c", "--config", action="store", dest="postfixConfig",
    help="Postfix config directory")
parser.add_option("-s", "--search", action="store", dest="searchString",
    help="Filter postqueue output with search string," +
    " if not selected will print all")
parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose", default=False,
    help="Be more verbvose about postqueue queued messages")
(options, args) = parser.parse_args()

# Declare some extra vars
segreagatedList = []

if options.postfixConfig and options.searchString:
    searchString = options.searchString
    postfixConfig = "-c " + options.postfixConfig
    rawInput = (os.popen('postqueue -p ' + postfixConfig).read()).split('\n')
    tmpString = ""
    # Header is always suppressed
    for element in rawInput[1:-1]:
        if element != "":
            tmpString += (element)
        elif element == "":
            segreagatedList.append(tmpString)
            tmpString = ""
    for element in segreagatedList:
        if element.find(searchString) >= 0:
            if options.verbose == True:
                print(element)
            else:
                print(element.split(' ',1)[0])


elif options.postfixConfig and not options.searchString:
    postfixConfig = "-c " + options.postfixConfig
    rawInput = (os.popen('postqueue -p ' + postfixConfig).read()).split('\n')
    tmpString = ""
    # Header is always suppressed
    for element in rawInput[1:-1]:
        if element != "":
            tmpString += (element)
        elif element == "":
            segreagatedList.append(tmpString)
            tmpString = ""
    for element in segreagatedList:
        if options.verbose == True:
            print(element)
        else:
            print(element.split(' ',1)[0])

else:
    parser.error("wrong parameters. -c is required")
