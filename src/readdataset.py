import pandas as pd
import matplotlib.pyplot as plt


class readdataset():
    def read(self):
        dataset = pd.read_csv("master.csv")
        print(dataset.shape)
        print(dataset.head(12))

    def view(self):
        #consultar dados dataset
        #apenas dá para ver duas tabelas de cada vez
        dataset = pd.read_csv("master.csv")

        country = dataset["country"]
        year = dataset["year"]

        plt.xlabel("country")
        plt.xlabel("year")

        plt.scatter(country, year)
        plt.show()


if __name__ == '__main__':
    readdataset().read()
    readdataset().view()




