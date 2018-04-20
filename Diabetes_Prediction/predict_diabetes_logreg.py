import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

diabetes_dataset = pd.read_csv("diabetes2.csv")
diabetes_dataset.shape

diabetes_dataset.groupby("Outcome").size()

train,test = train_test_split(diabetes_dataset, test_size=0.25, random_state=0, stratify=diabetes_dataset['Outcome']) 
train_X = train[train.columns[:8]]
test_X = test[test.columns[:8]]
train_Y = train['Outcome']
test_Y = test['Outcome']

model = LogisticRegression()
model.fit(train_X,train_Y)
prediction = model.predict(test_X)
print(metrics.accuracy_score(test_Y, prediction))