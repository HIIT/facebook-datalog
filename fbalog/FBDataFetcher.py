#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import time
import urllib.error
import urllib.request
from FakeResponse import *

# JAHugawa's TODO Corner
# DOJO: requestCount != 1 UNTESTED
# DOJO: when API returns X users attending, FB page says X+1 O.o
# DOJO: page fetch does not work as expected, test with several pages
# DOJO: optimize to use fields to get likes, comments with same requests -> less rate limit usage
# DOJO: remove unused permission for facebook review

class FBDataFetcher:
    def __init__(self):
        self._API_URL = "https://graph.facebook.com/v2.4/"
        self._PAGINATION_LIMIT = 1000
        self._HTTP_ERROR_RETRIES = 3
        self._RATE_LIMIT_COUNT = 600
        self._RATE_LIMIT_SECONDS = 600
        self._SHOULD_FETCH_DEFAULT = True # default value to use if a key is not found in self._options when calling self._shouldFetch()

        self._rateLimitCounters = {} # key, val as fb user id, rate limit counter as str, int
        self._rateLimitTimes = {} # key, val as fb user id, rate limit counter start time (unix epoch) as str, int
        self._accessToken = None # when set, should use fb access tokens (str)
        
#-########################
# PRIVATE UTIL FUNCTIONS #
#-########################

    # returns urllib request response object
    def _makeAPIRequest(self, url, data=None, requestCount=1):
        # check rate limits
        if self._accessToken not in self._rateLimitCounters.keys():
            self._rateLimitCounters[self._accessToken] = 0
            self._rateLimitTimes[self._accessToken] = int(time.time())
        self._rateLimitCounters[self._accessToken] += requestCount
        if self._rateLimitCounters[self._accessToken] >= self._RATE_LIMIT_COUNT:
            previous = self._rateLimitTimes[self._accessToken]
            current = int(time.time())
            nextAvailableTime = previous + self._RATE_LIMIT_SECONDS + 1 # + 1 to make sure that, when handling integers, we end up on the safe side of rate limiting
            wait = nextAvailableTime - current
            if wait > 0:
                print("Info: rate limit reached! Waiting for "+str(wait)+" seconds, then continuing")
                time.sleep(wait)
            self._rateLimitCounters[self._accessToken] -= self._RATE_LIMIT_COUNT
            self._rateLimitTimes[self._accessToken] = int(time.time())

        # send http request and return it's answer
        for i in range(0, self._HTTP_ERROR_RETRIES):
            try:
                return urllib.request.urlopen(url, data=data)
            except urllib.error.URLError as e:
                print("Url error: "+e.reason)
            except urllib.error.HTTPError as e:
                print("Http error "+e.code+": "+e.reason)
            except urllib.error.ContentTooShortError as e:
                print(e)
        print("Warning: request to "+url+" failed. Returning an empty response")
        return FakeResponse()

    def _setTemporaryData(self, accessToken, currentId=None, options={}):
        self._accessToken = accessToken
        self._currentId = currentId
        self._options = options
    
    def _resetTemporaryData(self):
        self._accessToken = None
        self._currentId = None
        self._options = None

    def _shouldFetch(self, key):
        if key not in self._options:
            if "default" in self._options:
                return self._options["default"]
            else:
                return self._SHOULD_FETCH_DEFAULT
        else:
            return self._options[key]
        
#-###########################
# PRIVATE PARSING FUNCTIONS #
#-###########################

    # returns next pagination url as str, or None if such url does not exist
    def _parsePaginationNextUrl(self, fbResponseData):
        parsed = json.loads(fbResponseData)
        url = None
        if "paging" in parsed.keys():
            paging = parsed["paging"]
            if "next" in paging.keys():
                url = paging["next"]
        return url

    # return an array of feed post ids
    def _parseItemIds(self, fbResponseData):
        ids = []
        parsed = json.loads(fbResponseData)
        if "data" in parsed.keys():
            for postData in parsed["data"]:
                if "id" in postData.keys():
                    ids.append(postData["id"])
        return ids

    # parse user ids, rsvp_status and names from the json, and return as array of maps
    def _parseParticipationData(self, fbResponseData):
        participants = []
        parsed = json.loads(fbResponseData)
        if "data" in parsed.keys():
            for userData in parsed["data"]:
                if set(["name","rsvp_status","id"]).issubset(set(userData.keys())):
                    participants.append(userData)
        return participants

    def _parseComment(self, fbResponseData):
        comment = None
        parsed = json.loads(fbResponseData)
        comment = parsed.copy()
        #if set(["created_time","from","message","id"]).issubset(set(parsed.keys())):
        #    if not set(["name","id"]).issubset(set(parsed["from"].keys())):
        #        print("Warning: a comment is missing data!")
        #else:
        #    print("Warning: a comment is missing data!")
        return comment

    # parse likes, return an array of fb user ids
    def _parseLikes(self, fbResponseData):
        likes = []
        parsed = json.loads(fbResponseData)
        if "data" in parsed.keys():
            for userData in parsed["data"]:
                if set(["id"]).issubset(set(userData.keys())):
                    likes.append({"id": userData["id"]})
        return likes
    
    # parse friends, return an array of maps such as {"id": "fb_user_id","name": "name"}
    def _parseFriends(self, fbResponseData):
        friends = []
        parsed = json.loads(fbResponseData)
        if "data" in parsed.keys():
            for userData in parsed["data"]:
                if set(["id","name"]).issubset(set(userData.keys())):
                    friends.append({"id": userData["id"], "name": userData["name"]})
        return friends

#-#########################
# PRIVATE FETCH FUNCTIONS #
#-#########################

    # participationType may be one of the following: "attending" "maybe" "declined" "noreply"
    def _fetchParticipationOfType(self, participationType):
        if participationType not in ["attending", "maybe", "declined", "noreply"]:
            print("ERROR: alert the programmers! Trying to use "+participationType+" as participation type! No participation data for this type will be returned!")
            return []
        participation = []
        nextUrl = self._API_URL+self._currentId+"/"+participationType+"?format=json&limit="+str(self._PAGINATION_LIMIT)+"&access_token="+self._accessToken
        while nextUrl != None:
            response = self._makeAPIRequest(nextUrl)
            responseData = response.read().decode("utf-8")
            participation += self._parseParticipationData(responseData)
            nextUrl = self._parsePaginationNextUrl(responseData)
        return participation
        
    def _fetchParticipation(self):
        participation = self._fetchParticipationOfType("attending") + self._fetchParticipationOfType("maybe") + self._fetchParticipationOfType("declined") + self._fetchParticipationOfType("noreply")
        return participation

    def _fetchFriends(self, itemId):
        friends = []
        nextUrl = self._API_URL+itemId+"/likes?format=json&access_token="+self._accessToken+"&limit="+str(self._PAGINATION_LIMIT)
        while nextUrl != None:
            response = self._makeAPIRequest(nextUrl)
            responseData = response.read().decode("utf-8")
            friends += self._parseFriends(responseData)
            nextUrl = self._parsePaginationNextUrl(responseData)
        return friends
    
    def _fetchLikes(self, itemId):
        likes = []
        nextUrl = self._API_URL+itemId+"/likes?format=json&access_token="+self._accessToken+"&limit="+str(self._PAGINATION_LIMIT)
        while nextUrl != None:
            response = self._makeAPIRequest(nextUrl)
            responseData = response.read().decode("utf-8")
            likes += self._parseLikes(responseData)
            nextUrl = self._parsePaginationNextUrl(responseData)
        return likes

    def _fetchComment(self, commentId):
        # get comment data (create_time, message, id, from(name, id))
        nextUrl = self._API_URL+commentId+"?format=json&access_token="+self._accessToken
        response = self._makeAPIRequest(nextUrl)
        responseData = response.read().decode("utf-8")
        comment = self._parseComment(responseData)
        if comment == None:
            return None
        # get comment likes
        if self._shouldFetch("likes"):
            comment["likes"] = self._fetchLikes(commentId)
        return comment

    def _fetchComments(self, itemId):
        comments = []
        nextUrl = self._API_URL+itemId+"/comments?format=json&access_token="+self._accessToken
        while nextUrl != None:
            response = self._makeAPIRequest(nextUrl)
            responseData = response.read().decode("utf-8")
            parsed = json.loads(responseData)
            if "data" in parsed.keys():
                for commentData in parsed["data"]:
                    if "id" in commentData:
                        comments.append(self._fetchComment(commentData["id"]))
            nextUrl = self._parsePaginationNextUrl(responseData)
        return comments

    def _fetchItem(self, itemId, fields=[]):
        # if fields are not specified, use whatever facebook gives us
        if len(fields) != 0:
            fields = "fields="+",".join(fields)
        else:
            fields = ""
        nextUrl = self._API_URL+itemId+"?format=json&access_token="+self._accessToken+"&"+fields
        response = self._makeAPIRequest(nextUrl)
        parsed = json.loads(response.read().decode("utf-8"))
        item = parsed.copy()
        # get likes
        if self._shouldFetch("likes"):
            item["likes"] = self._fetchLikes(itemId)
        # get comments
        if self._shouldFetch("comments"):
            item["comments"] = self._fetchComments(itemId)
        # return fetched item
        return item

    def _fetchMany(self, fromWhere, fields=[]):
        fetched = []
        nextUrl = self._API_URL+fromWhere+"?format=json&limit="+str(self._PAGINATION_LIMIT)+"&access_token="+self._accessToken
        while nextUrl != None:
            response = self._makeAPIRequest(nextUrl)
            responseData = response.read().decode("utf-8")
            ids = self._parseItemIds(responseData)
            for itemId in ids:
                fetched.append(self._fetchItem(itemId, fields))
            nextUrl = self._parsePaginationNextUrl(responseData)
        return fetched

    def _fetchFeed(self):
        return self._fetchMany(self._currentId+"/feed")

    def _fetchPosts(self):
        return self._fetchMany(self._currentId+"/posts", ["created_time","from","likes","link","message","shares","type","updated_time"])

#-##################
# PUBLIC FUNCTIONS #
#-##################

    def fetchEvent(self, eventId, accessToken, options={}):
        # set temporary data
        self._setTemporaryData(accessToken, eventId, options)
        
        # fetch participant data:
        participation = []
        if self._shouldFetch("participation"):
            participation = self._fetchParticipation()
        # fetch event feed:
        feed = []
        if self._shouldFetch("feed"):
            feed = self._fetchFeed()
        # create final json:
        finalJson = json.dumps({"participation": participation, "feed": feed})
        
        # reset temporary data
        self._resetTemporaryData()
        # return final json
        return finalJson

    def fetchPage(self, pageId, accessToken, options={}):
        # set temporary data
        self._setTemporaryData(accessToken, pageId, options)

        # fetch page feed:
        feed = []
        if self._shouldFetch("feed"):
            feed = self._fetchFeed()
        # fetch page likes:
        likes = []
        if self._shouldFetch("likes"):
            likes = self._fetchLikes(self._currentId)
        # create final json:
        finalJson = json.dumps({"feed": feed, "likes": likes})

        # reset temporary data
        self._resetTemporaryData()
        # return final json
        return finalJson
    
    def fetchUserId(self, accessToken, options={"default":False}):
        # set temporary data
        self._setTemporaryData(accessToken, "me", options)
        
        # fetch
        user = self._fetchItem("me")
        userId = None
        if "id" not in user.keys():
            print("Error: fb data does not contain id for user! Returning None")
        else:
            userId = user["id"]
        
        # reset temporary data
        self._resetTemporaryData()
        # return data
        return userId

    def fetchUserName(self, userId, accessToken, options={"default":False}):
        # set temporary data
        self._setTemporaryData(accessToken, "me", options)
        
        # fetch
        user = self._fetchItem("me", fields=["name"])
        userName = "failed_to_fetch_name"
        if "name" not in user.keys():
            print("Error: fb data does not contain name for user! Returning dummy value...")
        else:
            userName = user["name"]
        
        # reset temporary data
        self._resetTemporaryData()
        # return data
        return userName

    def fetchUserActivity(self, userId, accessToken, options={}):
        # set temporary data
        self._setTemporaryData(accessToken, userId, options)
        
        # fetch own posts
        activity = []
        feed = self._fetchPosts()
        
        # reset temporary data
        self._resetTemporaryData()
        # return data
        return feed

#-##################
# end of class def #
#-##################



#-###################
# unit tests (ToDo) #
#-###################

if __name__ == "__main__":
    print("--- UNIT TESTS START ---")
    accessToken = input("paste access token here, then enter: ")
    fb = FBDataFetcher()
    userId = fb.fetchUserId(accessToken)
    print("Your user id is "+userId)
    print("--- UNIT TESTS END ---")
