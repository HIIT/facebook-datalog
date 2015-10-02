import sys

from AppConfiguration import *
from DbConnection import *
from FBDataFetcher import *












if __name__ == "__main__":
    # except one additional argument: user id
    if len(sys.argv) < 2:
        f.open(LOG_PATH, "w")
        f.write("ERROR: no logging can be done! Process must receive one additional argument (user id to log)")
        f.close()
    else:
        db = DbConnection()
        fb = FBDataFetcher()
    
        userId = sys.argv[1]
        accessToken = db.getAccessToken(userId)
        
        # DOJO: write mining operations
        