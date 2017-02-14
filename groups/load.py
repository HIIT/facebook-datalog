import sys
from os.path import basename
import csv

import urlparse

from collect import *

collect_counter = 0

ii = len( sys.argv[1:] )

for i, filename in enumerate( sys.argv[1:] ):

    jj = len( open( filename ).readlines() ) - 1 ## remove the header row

    basefile = basename( filename )

    for j, entry in enumerate( csv.DictReader( open( filename ) ) ):

        try:

            print "File", (i+1), "of", ii, "entry", (j+1), "of", jj

            if 'id' in entry:
                fbid = entry['id']

            else:

                url = entry['url'].strip()
                url = urlparse.urlparse( url ).path
                print url
                fbid = url.split('/')[-1]

            data = collect( fbid )

            if data:

                json.dump( data, open( 'data/data_' + entry['type'] + '_' + basefile + '_' + data['name'].replace(' ', '_').replace('/', '_').lower() + '.json', 'w' ) )

                collect_counter += 1

                if collect_counter % 50 == 0:
                    print "Sleeping: Time to relax"
                    time.sleep( 60 * 60 ) ## relax loading speed

        except Exception, e:

            def do_nothing():
                pass

            if 'url' in entry:
                handle_fb_errors( entry['url'], e, do_nothing )
            else:
                handle_fb_errors( entry['id'], e, do_nothing )
