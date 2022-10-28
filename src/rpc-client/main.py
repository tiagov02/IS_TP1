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
def writeToXML(dataset:pd):
    root = ET.Element("Suicides")
    doc = ET.SubElement(root, "doc")
    for ind in dataset.index:
        print(dataset['country'][ind])

print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")
#dataset = readDataset()

#print(len(dataset))
#print(dataset.iterrows())
writeToXML(readDataset())

