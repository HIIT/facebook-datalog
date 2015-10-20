#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# JAHugawa's ToDo corner:
# DOJO: nothing to do, hooray \o/

import sqlite3

DB_FILEPATH = "fb_imports.db"

class DbConnection:
    def __init__(self):
        self._path = DB_FILEPATH
        self._connection = None
        self._cursor = None
    
    def _startOperation(self):
        if self._connection != None or self._cursor != None:
            print("Warning: existing db connection not closed! Closing it now and starting a new one.")
            self._finishOperation()
        self._connection = sqlite3.connect(self._path)
        self._cursor = self._connection.cursor()
    
    def _finishOperation(self):
        if self._connection == None or self._cursor == None:
            print("Warning: trying to finish db operation which doesn't exist! Nothing will be done.")
        else:
            self._connection.commit()
            self._connection.close()
            self._connection = None
            self._cursor = None
    
#-##################
# public interface #
#-##################

    def setAccessToken(self, userId, accessToken):
        self._startOperation()
        
        # save user id and access token
        self._cursor.execute("""INSERT INTO access_tokens VALUES (?, ?);""", (userId, accessToken))
        
        self._finishOperation()
    
    def getAccessToken(self, userId):
        self._startOperation()
        
        # save user id and access token
        print(userId)
        self._cursor.execute("""SELECT access_token FROM access_tokens WHERE user_id IS ?;""", (userId,))
        row = self._cursor.fetchone()
        accessToken = row[0]
        
        self._finishOperation()
        return accessToken        

    def initTables(self):
        self._startOperation()
        
        # create required tables if they do not exist
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS user_activity (user_id TEXT, content_type TEXT, content TEXT, target_type TEXT, target_id TEXT, created_time TEXT);""")
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS access_tokens (user_id TEXT UNIQUE ON CONFLICT REPLACE, access_token TEXT);""")
        
        self._finishOperation()
    
    def insertIntoUserActivity(self, rows):
        self._startOperation()
        
        # push each row separately
        for r in rows:
            self._cursor.execute("""INSERT INTO user_activity VALUES (?, ?, ?, ?, ?, ?);""", tuple(r))
        
        self._finishOperation()
