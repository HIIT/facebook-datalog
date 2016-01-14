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
        try:
            with open(path,'r') as f:
                lines = f.read().split('\n')
            for i in range(len(lines)-1, -1, -1):
                if lines[i] == "":
                    del lines[i]
            return lines
        except:
            return []

    accessToken = askUser("paste access token here, then press enter: ")
    pagesToFetch = listFromFile('page_ids.txt')
    groupsToFetch = listFromFile('group_ids.txt')
    fb = FBDataFetcher()
    
    # fetch events
    for eventId in listFromFile('event_ids.txt'):
        filepath = "event_"+eventId+".json"
        fb.fetchEventToFile(eventId, accessToken, filepath, options={"default": True})
    # fetch pages
    for pageId in listFromFile('page_ids.txt'):
        filepath = "page_"+pageId+".json"
        fb.fetchPageToFile(pageId, accessToken, filepath, options={"default": True})
    # fetch groups
    for groupId in listFromFile('group_ids.txt'):
        filepath = "group_"+groupId+".json"
        fb.fetchEventToFile(groupId, accessToken, filepath, options={"default": True, "likes": False})
