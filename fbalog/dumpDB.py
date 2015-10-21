import json
import sys
import time

from AppConfiguration import *
from DbConnection import *
from FBDataFetcher import *

# JAHugawa's ToDo corner:
# DOJO: flag to get users to separate user-named-files
# DOJO: flag to use id instead of name
# DOJO: complete dump versus posts-only
# DOJO: use argparse!

if __name__ == "__main__":
    db = DbConnection()
    fb = FBDataFetcher()
    
    userId = []
    if len(sys.argv) >= 2:
        userId += sys.argv[1:]
    else:
        # if no user ids are supplied, fetch all users
        userId += db.getAllUserIds()
    
    # dump posts to json
    posts = []
    for uid in userId:
        posts += db.getUserActivity(uid)
    postsJson = json.dumps(posts)
    currentTime = time.strftime("%Y_%m_%d_%H%M%S", time.gmtime())
    with open("posts_%s.json" % (currentTime,),"w") as f:
        f.write(postsJson)

