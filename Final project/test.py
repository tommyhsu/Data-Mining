import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import validation_curve 
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from matplotlib.colors import ListedColormap

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/car/car.data'
column_names = ['buying_price', 'maint_price', 'num_doors', 
                'people_cap', 'luggage_boot_size', 'safety', 'class']
data = pd.read_csv(url, names=column_names)
#print(data.head())
#print(data.info())
#sns.countplot(data['class'])
#plt.show()
lable=LabelEncoder()
for i in data.columns:
    data[i] = lable.fit_transform(data[i])
#print(data.head())
#fig=plt.figure(figsize=(8,4))
#sns.heatmap(data.corr(),annot=True)
#plt.show()
X=data[data.columns[:-1]]
y=data['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
rfc=RandomForestClassifier(n_jobs=-1,random_state=51)
rfc.fit(X_train,y_train)
predictions = rfc.predict(X_test)
#print("Random Forest Accuracy:",rfc.score(X_test,y_test))
#print("Random Forest F1-score:",f1_score(y_test,rfc.predict(X_test),average='macro'))
#print(classification_report(y_test,predictions))

param_range=[10,25,50,100]
curve=validation_curve(rfc,X_train,y_train,cv=5,param_name='n_estimators',param_range=param_range,n_jobs=-1)

train_score=[curve[0][i].mean() for i in range (0,len(param_range))]
test_score=[curve[1][i].mean() for i in range (0,len(param_range))]
fig=plt.figure(figsize=(6,8))
plt.plot(param_range,train_score)
plt.plot(param_range,test_score)
plt.xticks=param_range
#plt.show()

'''param_grid={'criterion':['gini','entropy'],
           'max_depth':[2,5,10,20],
           'max_features':[2,4,6,'auto'],
           'max_leaf_nodes':[2,3,None],}

grid=GridSearchCV(estimator=RandomForestClassifier(n_estimators=50,n_jobs=-1,random_state=51),
                  #param_grid=param_grid,cv=10,n_jobs=-1)
grid.fit(X_train,y_train)
print(grid.best_params_)
print(grid.best_score_)
'''
svm = SVC(kernel = 'poly', probability = True, gamma = 1 , C = 1)
svm.fit(X_train, y_train)
y_predictions = svm.predict(X_test)
print("SVM Accuracy:",svm.score(X_test, y_test))
print("SVM F1-score:",f1_score(y_test,svm.predict(X_test),average='macro'))
#print(classification_report(y_test,y_predictions))
c_matrix = confusion_matrix(y_test,y_predictions)
print ("confusion matrix:")
print (c_matrix)
#plt.matshow(c_matrix)

params_model = {'C':[0.1,1],'gamma':[1,0.1,0.01,0.001,0.0001]}

model = GridSearchCV(SVC(probability=True), 
                 		params_model, 
                        refit=True,
                        return_train_score=True,
                        cv = 5)        
model.fit(X_train, y_train)
print(model.best_params_)
print(model.best_score_)

param_range=[0.1,1,10]
curve=validation_curve( SVC(kernel = 'poly', probability = True, gamma = 'auto'),X_train,y_train,cv=5,param_name='C',param_range=param_range,n_jobs=-1)

train_score=[curve[0][i].mean() for i in range (0,len(param_range))]
test_score=[curve[1][i].mean() for i in range (0,len(param_range))]
fig=plt.figure(figsize=(6,8))
plt.plot(param_range,train_score)
plt.plot(param_range,test_score)
plt.xticks=param_range
plt.show()


