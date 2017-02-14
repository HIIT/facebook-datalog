import sys
from os.path import basename
import csv

from collect import *

collect_counter = 0

ii = len( sys.argv[1:] )

for i, filename in enumerate( sys.argv[1:] ):

    jj = len( open( filename ).readlines() )

    basefile = basename( filename )

    for j, entry in enumerate( csv.DictReader( open( filename ) ) ):

        try:

            print "File", (i+1), "of", ii, "entry", (j+1), "of", jj

            if 'id' in entry:
                fbid = entry['id']

            else:

                url = entry['url']
                fbid = url.strip()
                fbid = url.split('?')[0]

                if 'groups' in fbid:
                    fbid = fbid.split('.com/')[1]
                    fbid = fbid.split('/')[1]
                    fbid = fbid.replace('/', '')

            data = collect( fbid )

            if data:

                json.dump( data, open( 'data/data_' + entry['type'] + '_' + basefile + '_' + data['name'].replace(' ', '_').replace('/', '_').lower() + '.json', 'w' ), sort_keys=True, indent=4 )

                collect_counter += 1

                if collect_counter % 50 == 0:
                    print "Sleeping: Time to relax"
                    time.sleep( 60 * 60 ) ## relax loading speed

        except:

            if 'url' in entry:
                open('error.log', 'a').write('Failed ' + entry['url'] + '\n' )
            else:
                open('error.log', 'a').write('Failed ' + entry['id'] + '\n' )

