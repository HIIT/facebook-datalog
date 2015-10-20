#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# JAHugawa's ToDo corner:
# DOJO: chmod dbfile rights!
# DOJO: injection-proofness (fb data!)
# DOJO: encrypt access tokens?

import sqlite3
from DbConnection import *

if __name__ == "__main__":
    db = DbConnection()
    db.initTables()
