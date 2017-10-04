import sys
from os.path import basename
import csv

import urlparse

from collect import *

def strip_non_ascii(string):
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

collect_counter = 0

ii = len( sys.argv[1:] )

for i, f in enumerate( sys.argv[1:] ):

     fname = f.split('/')[-1]

     data = json.load( open( f ) )
     _id = data[ 'id' ]
     newdata = collect( _id , previous_data = data )
     json.dump( newdata , open( './data/' + fname, 'w' ) )    
