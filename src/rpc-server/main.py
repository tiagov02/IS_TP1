import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.string_length import string_length
from functions.string_reverse import string_reverse
from lxml import etree

class RequestHandler(SimpleXMLRPCRequestHandler):
   rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 9000), requestHandler=RequestHandler) as server:
   server.register_introspection_functions()
   def signal_handler(signum, frame):
      print("received signal")
      server.server_close()

      # perform clean up, etc. here...

      print("exiting, gracefully")
      sys.exit(0)


   def receive_file(arg):
      with open("suicides.xml", "wb") as handle:
         handle.write(arg.data)
         return True
   # signals
   '''
   signal.signal(signal.SIGTERM, signal_handler)
   signal.signal(signal.SIGHUP, signal_handler)
   signal.signal(signal.SIGINT, signal_handler)
   '''

   # register both functions
   server.register_function(string_reverse)
   server.register_function(string_length)
   server.register_function(receive_file)

   # start the server
   print("Starting the RPC Server...")
   server.serve_forever()