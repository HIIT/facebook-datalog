#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
if sys.version_info >= (3,0):
    askUser = input
else:
    askUser = raw_input

from FBDataFetcher import *

if __name__ == "__main__":

    def listFromFile(path):
        with open(path,'r') as f:
            lines = f.read().split('\n')
        for i in range(len(lines)-1, -1, -1):
            if lines[i] == "":
                del lines[i]
        return lines

    accessToken = askUser("paste access token here, then press enter: ")
    eventsToFetch = listFromFile('event_ids.txt')
    pagesToFetch = listFromFile('page_ids.txt')
    fb = FBDataFetcher()

    # fetch events
    for eventId in eventsToFetch:
        eventJson = fb.fetchEvent(eventId, accessToken, options={"default": True})
        # dump to file
        f = open("event_"+eventId+".json", "w")
        f.write(eventJson)
        f.close()
    # fetch pages
    for pageId in pagesToFetch:
        pageJson = fb.fetchPage(pageId, accessToken, options={"default": True})
        # dump to file
        f = open("page_"+pageId+".json", "w")
        f.write(pageJson)
        f.close()

