#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info >= (3,0):
    askUser = input
else:
    askUser = raw_input

from FBDataFetcher import *

if __name__ == "__main__":

    def authFromFile(path):
        with open(path,'r') as f:
            return f.read()

    def listFromFile(path):
        with open(path,'r') as f:
            lines = f.read().split('\n')
        for i in range(len(lines)-1, -1, -1):
            if lines[i] == "":
                del lines[i]
        return lines

    # parse args
    accessToken = None
    options = {"default": True}
    timestamp = ""
    if "-a" in sys.argv:
        accessToken = authFromFile(sys.argv[sys.argv.index("-a")+1])
    if "-s" in sys.argv:
        options["since"] = sys.argv[sys.argv.index("-s")+1]
        timestamp += "_"
        timestamp += options["since"]
    if "-u" in sys.argv:
        options["until"] = sys.argv[sys.argv.index("-u")+1]
        timestamp += "_"
        timestamp += options["until"]
    if accessToken is None:
        accessToken = askUser("paste access token here, then press enter: ")
    eventsToFetch = listFromFile('event_ids.txt')
    pagesToFetch = listFromFile('page_ids.txt')
    groupsToFetch = listFromFile('group_ids.txt')
    fb = FBDataFetcher()

    # fetch events
    for eventId in eventsToFetch:
        eventJson = fb.fetchEvent(eventId, accessToken, options=options)
        # dump to file
        f = open("output/event_"+eventId+timestamp+".json", "w")
        f.write(eventJson)
        f.close()
    # fetch pages
    for pageId in pagesToFetch:
        pageJson = fb.fetchPage(pageId, accessToken, options=options)
        # dump to file
        f = open("output/page_"+pageId+timestamp+".json", "w")
        f.write(pageJson)
        f.close()
    # fetch groups
    for groupId in groupsToFetch:
        options["participation"] = False
        options["likes"] = False
        groupJson = fb.fetchEvent(groupId, accessToken, options=options)
        # dump to file
        f = open("output/group_"+groupId+timestamp+".json", "w")
        f.write(groupJson)
        f.close()

