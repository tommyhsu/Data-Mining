import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

data = pd.read_excel("car_evaluation.xlsx")
lable=LabelEncoder()
for i in data.columns:
    data[i] = lable.fit_transform(data[i])
print(data.head())
#print(data.info())
#sns.countplot(data['class'])
#plt.show()

