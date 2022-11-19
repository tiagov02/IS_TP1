import psycopg2


connection = None
cursor = None
#test commit

def connect():
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

    finally:
        if connection:
            cursor.close()
            connection.close()


def dbSave(xml:str):
    xml_file = etree.fromstring(xml)
    s = etree.tostring(xml_file, encoding="utf8", method="xml").decode()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO imported_documents (file_name, xml) VALUES(%s, %s)", ("suicides", s))
    connection.commit()