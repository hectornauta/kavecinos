import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

fruits = pd.read_table('dataset04.txt',sep=';')
print(fruits)

x = fruits[['x1', 'x2']]
y = fruits['Clase']
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

for i in range(1,11):
    knn = KNeighborsClassifier(n_neighbors = i)
    print(knn.fit(x_train,y_train))
    print(knn.score(x_test,y_test))