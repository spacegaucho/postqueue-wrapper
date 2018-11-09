#!/usr/bin/python2.7 -B
# FOR NOW THIS IS HOW TO DELETE EMAILS:
# for i in $(./postqueue-wrapper.py -c <postfixConfDir> -s "<stringToDelete>"); do postsuper -d $i -c <postfixConfDir>; done
# Need ability to check if os.popen returned 0, halt if it didn't.

import sys
import os
from optparse import OptionParser

def parse_postqueue():
  global searchString
  global segreagatedList
  global postfixConfig
  segreagatedList = []
  searchString = options.searchString
  postfixConfig = "-c " + options.postfixConfig
  postqueue_out = os.popen('postqueue -p ' + postfixConfig + ' 2>/dev/null')
  rawInput = (postqueue_out.read()).split('\n')
  if postqueue_out.close() != None:
    print ("E: Postqueue did not run correctly")
    exit(1)
  tmpString = ""
  # Header is always suppressed
  try:
    for element in rawInput[1:-1]:
      if element != "":
        tmpString += (element)
      elif element == "":
        segreagatedList.append(tmpString)
        tmpString = ""
  except:
    print("E: Failed generating segreagatedList to work with")
    exit(1)

def search(segreagatedList,searchString):
  for element in segreagatedList:
    if element.find(searchString) >= 0:
      print_output(element,segreagatedList)

def no_search(segreagatedList,searchString):
  for element in segreagatedList:
    print_output(element,segreagatedList)

def del_search(segreagatedList,searchString):
  print("for i in $(./postqueue-wrapper.py -c " + postfixConfig + " -s \"" + searchString + "\"); do postsuper -d $i -c " + postfixConfig + "; done")

def print_output(element,segreagatedList):
  if options.verbose == True:
    print(element)
  else:
    print(element.split(' ',1)[0])

def main():
  global options
  parser = OptionParser(usage="usage: %prog -c <config> [-s <search>] [-v] ")
  parser.add_option("-c", "--config", action="store", dest="postfixConfig",
                    help="Postfix config directory")
  parser.add_option("-s", "--search", action="store", dest="searchString",
                    help="Filter postqueue output with search string," +
                    " if not selected will print all")
  parser.add_option("-D", "--delete",
                    action="store_true", dest="delete", default=False,
                    help="Deletes the search, requires -s/--search")
  parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="Be more verbvose about postqueue queued messages")
  (options, args) = parser.parse_args()

  # Parse search and print
  if options.postfixConfig and options.searchString and not options.delete:
    parse_postqueue()
    search(segreagatedList,searchString)
  # Parse print all
  elif options.postfixConfig and not options.searchString and not options.delete:
    parse_postqueue()
    no_search(segreagatedList,searchString)
  # Parse searche and destroy
  elif options.postfixConfig and options.searchString and options.delete:
    parse_postqueue()
    del_search(segreagatedList,searchString)
  else:
    parser.error("wrong parameters. -c is required")

# Call main
if __name__ == "__main__":
  main()
