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
         connection = psycopg2.connect(user="is",
                                       password="is",
                                       host="localhost",
                                       port="5432",
                                       database="is")

         cursor = connection.cursor()
         cursor.execute("INSERT INTO imported_documents (file_name, xml) VALUES(%s, %s)", ("suicides2.xml", s))
         connection.commit()
      except (Exception, psycopg2.Error) as error:
         print("Failed to fetch data", error)
      finally:
         if connection:
            cursor.close()
            connection.close()

   # XPATH AND XQUERY
   def orderByYear(year:str):
       res = None
       try:
           connection = psycopg2.connect(user="is",
                                         password="is",
                                         host="localhost",
                                         port="5432",
                                         database="is")

           cursor = connection.cursor()
           print(year)
           res = cursor.execute(
               f"with suicides as ( select unnest ( xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY/SUICIDE', xml)) as suicide from imported_documents where file_name='suicides2.xml') SELECT (xpath('@sex', suicide))[1]::text as sex, COUNT(*) as count FROM suicides GROUP BY (xpath('@sex', suicide))[1]::text")
           for data in cursor:
               print(f"SEX: {data[0]}, NS: {data[1]}")
       except (Exception, psycopg2.Error) as error:
           print("Failed to fetch data", error)
       finally:
           if connection:
               cursor.close()
               connection.close()
           return res

   def orderByCountryAndYear(year:str,country:str):
      try:
         connection = psycopg2.connect(user="is",
                                       password="is",
                                       host="localhost",
                                       port="5432",
                                       database="is")

         cursor = connection.cursor()
         cursor.execute("SELECT xpath(/suicides/year/country[name='"+country+"']/suicides/text(),xml) from imported_documents")
         for sdata in cursor:
            print(sdata)
      except (Exception, psycopg2.Error) as error:
         print("Failed to fetch data", error)
      finally:
         if connection:
            cursor.close()
            connection.close()
   def orderByGdpPerCapita():
      return
   def childrensWhoCommitedSuicide():
      return
   def oldersWhoCommitedSuicide():
      return
   #####

   def menu(option:str, year,country):
      if option == '1':
         return orderByYear(year)
      elif option == '2':
         orderByCountryAndYear(year,country)
      elif option == '3':
         orderByGdpPerCapita()
      elif option == '4':
         childrensWhoCommitedSuicide()
      elif option == '5':
         oldersWhoCommitedSuicide()


   # signals

   signal.signal(signal.SIGTERM, signal_handler)
   signal.signal(signal.SIGHUP, signal_handler)
   signal.signal(signal.SIGINT, signal_handler)


   # register both functions
   server.register_function(string_reverse)
   server.register_function(string_length)
   server.register_function(receive_file)
   server.register_function(menu)

   # start the server
   print("Starting the RPC Server...")
   server.serve_forever()
