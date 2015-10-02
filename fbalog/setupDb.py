#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# JAHugawa's ToDo corner:
# DOJO: chmod dbfile rights!
# DOJO: injection-proofness (fb data!)
# DOJO: encrypt access tokens?

import sqlite3

DB_FILEPATH = "fb_imports.db"

# establish db connection
dbConnection = sqlite3.connect(DB_FILEPATH)
dbCursor = dbConnection.cursor()

# create required tables
dbCursor.execute("""CREATE TABLE IF NOT EXISTS user_activity (user_id TEXT, content_type TEXT, content TEXT, target_type TEXT, target_id TEXT, created_time TEXT);""")
dbCursor.execute("""CREATE TABLE IF NOT EXISTS access_tokens (user_id TEXT, access_token TEXT);""")


# save and exit
dbConnection.commit()
dbConnection.close()
