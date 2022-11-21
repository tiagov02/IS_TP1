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
    aux = None
    suicides = None
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
    res = None
    print("##############SYSTEMS INTEGRATION##################")
    print("########José Viana, Luís Malheiro@ESTG-IPVC########")
    print("1 -\tPer Year")
    print("2 -\tPer Country and year")
    print("3 -\tWhere GDP per capita is bigger then 18577(Portugal in 2012)")
    print("4 -\t In Children(Age less then 15)")
    print("6 -\t In Olders(Age bigger then 75)")
    option = input("\tEnter your option")
    if option == '1':
        year = input("\tEnter the year that you wanna search")
        presentResult(server.orderByYear(year))
    else:
        if option == '2':
            year = input("\tEnter the year that you wanna search")
            country = input("\tEnter the cuntry that you wanna search")
        else:
            return


def presentResult(res):
    for data in res:
        print(f"SEX: {data[0]} AND NO: {data[1]}")




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







