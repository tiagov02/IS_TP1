import pandas as pd

class readdataset():
    def read(self):
        dataset = pd.read_csv("master.csv")
        return dataset

    def view(self):
        #consultar dados dataset
        #apenas dá para ver duas tabelas de cada vez
        dataset = pd.read_csv("master.csv")

if __name__ == '__main__':
    dataset = readdataset().read()
    readdataset().view()




