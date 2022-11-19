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
      if True:
         with open("suicides.xml", "wb") as handle:
            saveToDb(arg.data)
            handle.write(arg.data)
            return True
      else:
         return False

#Funções da base de dados
   def connectToDb():

      # test commit

      try:
         connection = psycopg2.connect(user="is",
                                       password="is",
                                       host="localhost",
                                       port="5432",
                                       database="is")

         cursor = connection.cursor()
         cursor.execute("SELECT * FROM teachers")

         print("Teachers list:")
         for teacher in cursor:
            print(f" > {teacher[0]}, from {teacher[1]}")

      except (Exception, psycopg2.Error) as error:
         print("Failed to fetch data", error)



   def saveToDb(xml:str):
      try:
         xml_file = etree.fromstring(xml)
         s = etree.tostring(xml_file, encoding="utf8", method="xml").decode()
         connection = psycopg2.connect(user="is",
                                       password="is",
                                       host="localhost",
                                       port="5432",
                                       database="is")

         cursor = connection.cursor()
         cursor.execute("INSERT INTO imported_documents (file_name, xml) VALUES(%s, %s)", ("nameXML", s))
         connection.commit()
      except (Exception, psycopg2.Error) as error:
         print("Failed to fetch data", error)
      finally:
         if connection:
            cursor.close()
            connection.close()



       #test save


   # signals

   signal.signal(signal.SIGTERM, signal_handler)
   signal.signal(signal.SIGHUP, signal_handler)
   signal.signal(signal.SIGINT, signal_handler)


   # register both functions
   server.register_function(string_reverse)
   server.register_function(string_length)
   server.register_function(receive_file)

   connectToDb()
   # start the server
   print("Starting the RPC Server...")
   server.serve_forever()
