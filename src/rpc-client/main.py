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
    for year , df_group in dataset.groupby('year'):
        i:int =0
        print(year)
        years = ET.Element('Year',{'code':year})
        for country,df_group_country  in df_group.groupby('country'):
            #print(country)
            #print(df_group_country['country-year'])
            countys = ET.Element('country',{'name':country})
            #ver gravar varios countrys(append)
            for item in df_group_country.iterrows():
                i = i+1
                #split
                suicides = ET.Element('suicide',{'sex': item[i].T['sex'], 'suicides_no' : item[i].T['suicides_no'] ,
                                                 'population': item[i].T['suicides_no']})
                #item[1].T['year']
                #print(item)
    tree = ET.ElementTree(years, countys, suicides)
    tree.write("suicides.xml")





print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")
dataset = readDataset()
writeXML(dataset)
#writeToXML(dataset)

#print(len(dataset))



