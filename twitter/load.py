import sys
import common
import json

for f in sys.argv[1:]:
   print 'Loading', f

   ids = map( lambda x: x.strip(), open(f) )

   tweets = common.tweets( ids )

   json.dump( tweets, open( f + '.json', 'w') )
