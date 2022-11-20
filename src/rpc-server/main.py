import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.string_length import string_length
from functions.string_reverse import string_reverse
from lxml import etree
import psycopg2


class RequestHandler(SimpleXMLRPCRequestHandler):
   rpc_paths = ('/RPC2',)

with SimpleXMLRPCServer(('localhost', 9000), requestHandler=RequestHandler) as server:
   server.register_introspection_functions()


   def connectToDb():
      connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="localhost",
                                    port="5432",
                                    database="is")

      cursor = connection.cursor()
      cursor.execute("SELECT * FROM teachers")
      return [connection,cursor]

   def signal_handler(signum, frame):
      print("received signal")
      server.server_close()

      # perform clean up, etc. here...

      print("exiting, gracefully")
      sys.exit(0)

   def validateXSD(xml: str, xsd_path: str) -> bool:
      xmlschema_doc = etree.parse(xsd_path)
      xmlschema = etree.XMLSchema(xmlschema_doc)

      xml_doc = etree.fromstring(xml)
      result = xmlschema.validate(xml_doc)

      return result

   def receive_file(arg):
      if validateXSD(arg.data,"suicidesXSD.xsd"):
         with open("suicides.xml", "wb") as handle:
            saveToDb(arg.data)
            handle.write(arg.data)
            return True
      else:
         return False

   def saveToDb(xml:str):
      try:
         xml_file = etree.fromstring(xml)
         s = etree.tostring(xml_file, encoding="utf8", method="xml").decode()
         res = connectToDb()
         cursor = res[0]
         connection = res[1]
         cursor.execute("INSERT INTO imported_documents (file_name, xml) VALUES(%s, %s)", ("suicides.xml", s))
         connection.commit()
      except (Exception, psycopg2.Error) as error:
         print("Failed to fetch data", error)
      finally:
         if connection:
            cursor.close()
            connection.close()

   # XPATH AND XQUERY
   def orderByYear(year:str):
      try:
         res = connectToDb()
         connection = res[0]
         cursor = res[1]
         cursor.execute("SELECT xpath(/suicides/year[code='"+year+"']/country/suicides/text()")
         for sdata in cursor:
            print(sdata)
      except (Exception, psycopg2.Error) as error:
         print("Failed to fetch data", error)

   def orderByCountry():
      return
   def orderByGdpPerCapita():
      return
   def childrensWhoCommitedSuicide():
      return
   def oldersWhoCommitedSuicide():
      return
   #####

   def menu(option:str, data):
      if option == 1:
         a = 0


   # signals

   signal.signal(signal.SIGTERM, signal_handler)
   signal.signal(signal.SIGHUP, signal_handler)
   signal.signal(signal.SIGINT, signal_handler)


   # register both functions
   server.register_function(string_reverse)
   server.register_function(string_length)
   server.register_function(receive_file)

   # start the server
   print("Starting the RPC Server...")
   server.serve_forever()
