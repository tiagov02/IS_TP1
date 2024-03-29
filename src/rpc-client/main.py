class Coordinates:
    def __init__(self, country: object, lat: object, lon: object) -> object:
        self.country = country
        self.lat = lat
        self.lon = lon

    def getCountry(self):
        return self.country

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon

import xmlrpc.client
import pandas as pd
import xml.etree.cElementTree as ET
import psycopg2

from pip._vendor import requests

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://localhost:9000')

string = "hello world"
def generate_coords(region: str):
    url = "https://nominatim.openstreetmap.org/"

    params = {
        'q': region,
        'limit': '1',
        'format': 'json'
    }

    r = requests.get(url=url, params=params)

    data = r.json()

    return [
        data[0]["lat"],
        data[0]["lon"]
    ]


def readDataset():
    dataset = pd.read_csv("../master.csv")
    print(dataset)
    return dataset


def writeXML(dataset:pd):
    root = ET.Element('SUICIDES')
    i = 1
    coordinates = []
    find_country: bool = False
    for year , df_group in dataset.groupby('year'):
        i=0
        print(year)
        years = ET.SubElement(root,'YEAR',{'code':str(year)})
        for country,df_group_country  in df_group.groupby('country'):
            if len(coordinates) == 0:
                coords = generate_coords(country)
                countys = ET.SubElement(years, 'COUNTRY',
                                        {'name': str(country), 'lat': str(coords[0]), 'lon': str(coords[1])})
                c = Coordinates(country,coords[0],coords[1])
                coordinates.append(c)
            else:
                for c in coordinates:
                    if c.getCountry() == country:
                        countys = ET.SubElement(years, 'COUNTRY',
                                                {'name': str(country), 'lat': str(c.getLat()), 'lon': str(c.getLon())})
                        find_country = True
                if not find_country:
                    coords = generate_coords(country)
                    countys = ET.SubElement(years, 'COUNTRY',
                                            {'name': str(country), 'lat': str(coords[0]), 'lon': str(coords[1])})
                    c = Coordinates(country, coords[0], coords[1])
                    coordinates.append(c)
            for item in df_group_country.iterrows():
                aux = item[1].T
                minAge = None
                maxAge = None
                if(aux['age'] == "75+ years"):
                    minAge = "75"
                    maxAge= "MAX"
                else:
                    auxStr = str(aux['age']).split("-")
                    auxMax = str(auxStr[1]).split()
                    minAge = auxStr[0]
                    maxAge = auxMax[0]
                suicides = ET.SubElement(countys,'SUICIDE',{'sex':str(aux['sex']),'minAge':str(minAge),'maxAge':str(maxAge),
                                                            'tax':str(aux['suicides/100k pop']),'population_no':str(aux['population']),
                                                            'suicides_no':str(aux['suicides_no']), 'generation':str(aux['generation']),
                                                            'gdp_for_year':str(aux[' gdp_for_year ($) ']),'hdi_for_year':str(aux['HDI for year']),
                                                            'gdp_per_capita':str(aux['gdp_per_capita ($)'])})
    tree = ET.ElementTree(root)

    with open('suicides.xml', 'w') as f:
        tree.write(f, encoding='unicode')


def menu():
    valid: bool = False
    while True:
        print("##############SYSTEMS INTEGRATION##################")
        print("########José Viana, Luís Malheiro@ESTG-IPVC########")
        print("0 -\t Close the Program")
        print("1 -\tPer Year")
        print("2 -\tPer Country")
        print("3 -\tPer Country and year")
        print("4 -\t Where GDP per capita is bigger then 18577(Portugal in 2012)- By Sex")
        print("5 -\t The coundries that have less and more suicides...")
        while True:
            try:
                option = int(input("\tEnter your option:\n"))
            except(Exception):
                option = int(input("\tEnter your option:\n"))
            if option in range(6):
                break
        if option == 1:
            year = input("\tEnter the year that you wanna search:\n")
            presentResult(server.orderByYear(year), f"suicides_per_year_{year}")
        elif option == 2:
            country = input("\tEnter the cuntry that you wanna search:\n")
            presentResult(server.orderByCountry(country), f"suicides_per_country_{country}")
        elif option == 3:
            year = input("\tEnter the year that you wanna search:\n")
            country = input("\tEnter the cuntry that you wanna search\n")
            presentResult(server.orderByYarAndCountry(year, country), f"suicides_per_country_{country}_year_{year}")
        elif option == 4:
            presentSimpleResult(server.suicidesInRichCountry())
        elif option == 5:
            res = server.yearWithLessandMoreSuicides()
            presentCountriesLessMoreSuicides(res)
        elif option == 0:
            break




def presentResult(res,type):
    if not len(res) == 0:
        for data in res[0]:
            print(f"SEX: {data[0]} AND NO: {data[1]}")
        print("CHILDRENS")
        for c in res[2]:
            print(f"{c[0]}")
        print("Olders")
        for o in res[3]:
            print(f"{o[0]}")
        with open(f"{type}.xml", "w") as f:
            f.write(f"<{type}>\n")
        for d in res[1]:
            with open(f"{type}.xml", "a") as handle:
                handle.write(f"{d[0]}\n")
        with open(f"{type}.xml", "a") as file:
            file.write(f"</{type}>")
    else:
        print("The database is not working or not have data or you dont have a valid values")
    return
def presentSimpleResult(res):
    if not len(res) == 0:
        for dt in res:
            print(f"SEX: {dt[0]} NUMBER OF SUICIDES: {dt[1]}")
    else:
        print("The database is not working or not have data")
    return

def presentCountriesLessMoreSuicides(res):

    print(f"The country with more suicides is {res[0][0]} With {res[0][1]} suicides")
    print(f"The country with less suicides is {res[1][0]} With {res[1][1]} suicides")
    print("\n\n\n")
    print("\tPRESENTING THE DATA OF THIS COUNTRIES")
    print("\tThe Country with more suicides")
    presentResult(server.orderByCountry(res[0][0]),f"suicides_per_country_{res[0][0]}".replace(" ","_"))
    print("\tThe Country with les suicides")
    presentResult(server.orderByCountry(res[1][0]),f"suicides_per_country_{res[0][0]}".replace(" ","_"))






print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")
dataset = readDataset()
writeXML(dataset)
resp = None
with open("suicides.xml", "rb") as handle:
    binary_data = xmlrpc.client.Binary(handle.read())
    resp = server.receive_file(binary_data)
print(resp)
menu()








