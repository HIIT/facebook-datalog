#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from FBDataFetcher import *

if __name__ == "__main__":
    accessToken = input("paster access token here, then press enter: ")
    eventsToFetch = ["724641294332217","847916881985099","468794753302290","1660348977536049","500590370113391","1068122033207712","526212614201771","121902428163319"]
    # NOTE: page fetching does not work quite as expected (it crashes),  consult JAHugawa before trying this at home!
    pagesToFetch = []#"1125819457447058"]
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

