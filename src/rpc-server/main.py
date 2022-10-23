import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.string_length import string_length
from functions.string_reverse import string_reverse
import pandas as pd

class RequestHandler(SimpleXMLRPCRequestHandler):
   rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 9000), requestHandler=RequestHandler) as server:
   server.register_introspection_functions()
   dataset = None
   def signal_handler(signum, frame):
      print("received signal")
      server.server_close()

      # perform clean up, etc. here...

      print("exiting, gracefully")
      sys.exit(0)
   def readDataset():
      dataset = pd.read_csv("master.csv")

   def printDataset():
      print(dataset)

   def saveDatasetInCSV():
      return None

   # signals
   '''
   signal.signal(signal.SIGTERM, signal_handler)
   signal.signal(signal.SIGHUP, signal_handler)
   signal.signal(signal.SIGINT, signal_handler)
   '''

   # register both functions
   server.register_function(string_reverse)
   server.register_function(string_length)
   #server.register_function(printDataset)

   # start the server
   print("Starting the RPC Server...")
   server.serve_forever()