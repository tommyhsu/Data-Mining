#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 20:05:20 2019

@author: sandilya
"""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Reading the data set
data_set=pd.read_csv("cars.csv")
print(data_set.columns.values)

#encoding the output values
lenc=LabelEncoder()
data_set['predict']=lenc.fit_transform(data_set['predict'])

data_set['buying']=lenc.fit_transform(data_set['buying'])
data_set['persons']=lenc.fit_transform(data_set['persons'])
data_set['doors']=lenc.fit_transform(data_set['doors'])
data_set['maint']=lenc.fit_transform(data_set['maint'])
data_set['lug_boot']=lenc.fit_transform(data_set['lug_boot'])
data_set['saftey']=lenc.fit_transform(data_set['saftey'])

x=data_set.iloc[:,0:-1]
y=data_set.iloc[:,-1]
#splitting the data set
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.3)


#classification
clf=DecisionTreeClassifier(criterion='entropy')
clf.fit(x_train,y_train)
predictions = clf.predict(x_test)
print("Classification accuracy is ",clf.score(x_test,y_test)*100)
print(classification_report(y_test,predictions))

# to export the tree as a .dot file
from sklearn import tree
tree.export_graphviz(clf,out_file='cars_tree.dot')