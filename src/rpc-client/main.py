import xmlrpc.client
import pandas as pd

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://localhost:9000')

string = "hello world"


def readDataset():
    dataset = pd.read_csv("../master.csv")
    print(dataset)
    return dataset

print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")
readDataset()