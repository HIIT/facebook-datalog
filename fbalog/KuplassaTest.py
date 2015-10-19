#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# DOJO: python 2 (because of server configs >.<) so does not work with python3

from cgi import escape
from urlparse import parse_qs
#from flup.server.fcgi import WSGIServer
import os
import sys
from wsgiref.simple_server import make_server

def app(environ, start_response):
    # change these to test different things
    printInput = True
    printEnviron = False
    
    start_response('200 OK', [('Content-Type', 'text/html')])
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]

    yield '<html><body><p>Kuplaa rakennetaan...</p>'#</body></html>'
    # <img src="https://utmemes.com/images/under_construction_cat_soap.jpg></img>'
    if printInput:
        yield '<pre>PATH: %s</pre></br>' % escape(  path  )
        if method == "POST":
            if environ['CONTENT_LENGTH'] == "":
                yield '<pre>CONTENT: %s</pre></br>' % escape(  "NONE"  )
            else:
                yield '<pre>CONTENT: %s</pre></br>' % escape(  environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))  )
        elif method == "GET":
            yield '<pre>QUERY_STRING:\n%s</pre>' % escape(  "\n".join(parse_qs(environ["QUERY_STRING"]))  )
        
    if printEnviron:
        yield '<table>'
        for k, v in sorted(environ.items()):
            if type(k) == str:
                kShow = escape(k)
            else:
                kShow = escape("NON-STRING KEY")
            if type(v) == str:
                vShow = escape(v)
            else:
                vShow = escape("NON-STRING VALUE")
                print type(v)
            yield '<tr><th>{0}</th><td>{1}</td></tr>'.format(kShow,vShow)
        yield '</table>'
    yield '</body></html>'

port = 9090
kuplassaServer = make_server('localhost', port, app)
print("Kuplassa Server running on port %d" % port)
kuplassaServer.serve_forever()
