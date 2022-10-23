import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://localhost:9000')

string = "hello world"

print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")
#print(f" > {server.printDataset()}")