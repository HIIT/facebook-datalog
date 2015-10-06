import sys
import time

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
        activity = fb.fetchUserActivity(userId,accessToken)
        rowsToInsert = []
        for item in activity:
            if "type" in item:
                # get data, format as db rows...
                if item["type"] == "link" and "link" in item and "message" in item:
                    content = item["link"] + " "+item["message"]
                elif item["type"] == "status" and "message" in item:
                    content = item["message"]
                else:
                    continue
                itemTime = "0000-00-00T00:00:00+0000"
                if "created_time" in item:
                    itemTime = item["created_time"]
                #if "updated_time" in item:
                #    itemTime = item["updated_time"]
                rowsToInsert.append([userId,"post",content,"user",userId,itemTime])
                if "comments" in item:
                    for c in item["comments"]:
                        # DOJO: validate field existence
                        rowsToInsert.append([c["from"]["id"],"comment",c["message"],"user",userId,c["created_time"]])
                    for l in item["likes"]:
                        # DOJO: validate field existence
                        likeTime = time.strftime("%Y-%m-%dT%H:%M:%S+0000",time.gmtime()) #DOJO: time zone!
                        rowsToInsert.append([l["id"],"like","","user",userId,likeTime])
        # ... push rows to db
        
