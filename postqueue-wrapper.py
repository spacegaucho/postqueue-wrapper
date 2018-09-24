#!/usr/bin/python2.7 -B
# FOR NOW THIS IS HOW TO DELETE EMAILS:
# for i in $(./postqueue-wrapper.py -c <postfixConfDir> -s "<stringToDelete>"); do postsuper -d $i -c <postfixConfDir>; done
# FIXME: make functions, test if rawInput out of range

import sys
import os
from optparse import OptionParser

# Global vars
global options
global args
global segreagatedList
global searchStrin

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

segreagatedList = []
searchString = options.searchString

def parse_postqueue():
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

def print_output():
  if options.verbose == True:
    print(element)
  else:
    print(element.split(' ',1)[0])

def search():
  for element in segreagatedList:
    if element.find(searchString) >= 0:
      print_output(element)

def no_search():
  for element in segreagatedList:
    print_output(element)

if options.postfixConfig and options.searchString:
  try:
    parse_postqueue
  except:
    print("E: Could not parse postqueue")
  search

elif options.postfixConfig and not options.searchString:
  try:
    parse_postqueue
  except:
    print("E: Could not parse postqueue")
  no_search

else:
  parser.error("wrong parameters. -c is required")
