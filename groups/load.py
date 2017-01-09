import sys
import datetime

from collect import *

collect_counter = 0

ii = len( sys.argv[1:] )

for i, filename in enumerate( sys.argv[1:] ):

    jj = len( open(filename).readlines() )

    for j, url in enumerate( open(filename) ):

        print "File", (i+1), "of", ii, "entry", (j+1), "of", jj

        url = url.strip()
        fbid = url.split('?')[0]
        fbid = fbid.split('.com/')[1]
        ## remove list of bad terms
        for s in ['groups/']:
            fbid = fbid.replace(s, '')
        fbid = fbid.replace('/', '')

        ## data collection starts here

        data = collect( fbid )

        ## TODO: add group and page metadata collection

        json.dump( data, open( 'data/data_' + data['name'].replace(' ', '_').replace('/', '_').lower() + '.json', 'w' ), sort_keys=True, indent=4 )

        collect_counter += 1

        if collect_counter % 50 == 0:
            print "Sleeping: Time to relax"
            time.sleep( 60 * 60 ) ## relax loading speed
