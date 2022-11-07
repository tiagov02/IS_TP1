import xmlrpc.client
import pandas as pd
import xml.etree.cElementTree as ET

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://localhost:9000')

string = "hello world"

def readDataset():
    dataset = pd.read_csv("../master.csv")
    print(dataset)
    return dataset
def writeXML(dataset:pd):
    root = ET.Element('SUICIDES')
    aux = None
    suicides = None
    for year , df_group in dataset.groupby('year'):
        i=0
        print(year)
        years = ET.SubElement(root,'Year',{'code':str(year)})
        for country,df_group_country  in df_group.groupby('country'):
            countys = ET.SubElement(years,'country',{'name':str(country)})
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
                suicides = ET.SubElement(countys,'suicide',{'sex':str(aux['sex']),'minAge':str(minAge),'maxAge':str(maxAge),
                                                            'tax':str(aux['suicides/100k pop']),'population_no':str(aux['population']),
                                                            'suicides_no':str(aux['suicides_no']), 'generation':str(aux['generation']),
                                                            'gdp_for_year':str(aux[' gdp_for_year ($) ']),'hdi_for_year':str(aux['HDI for year']),
                                                            'gdp_per_capita':str(aux['gdp_per_capita ($)'])})
    tree = ET.ElementTree(root)
    with open('out.xml', 'w') as f:
        tree.write(f, encoding='unicode')





print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")
dataset = readDataset()
writeXML(dataset)
with open("out.xml", "rb") as handle:
    binary_data = xmlrpc.client.Binary(handle.read())
    server.receive_file(binary_data)




