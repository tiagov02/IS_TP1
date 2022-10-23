import pandas as pd
import matplotlib.pyplot as plt


class readdataset():
    def read(self):
        dataset = pd.read_csv("master.csv")
        return dataset

    def view(self):
        #consultar dados dataset
        #apenas dá para ver duas tabelas de cada vez
        dataset = pd.read_csv("master.csv")
        print(dataset.shape)
        print(dataset.head(12))
if __name__ == '__main__':
    dataset = readdataset().read()
    readdataset().view()




