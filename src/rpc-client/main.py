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
        years = ET.Element('Year',{'code':year})


print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")
dataset = readDataset()
#writeToXML(dataset)

#print(len(dataset))



