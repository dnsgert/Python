import matplotlib.pyplot as plt 

import pandas as pd

import numpy as np

#from sklearn import metrics

dataset = pd.read_csv('Salary_Data.csv')

#print ('Shape \n',dataset.shape)

#print('head \n',dataset.head())

print('describe \n',dataset.describe())

X= dataset.iloc[:,:-1].values
#print(X)

y= dataset.iloc[:,1].values
#print(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2, random_state=0)

from sklearn.linear_model import LinearRegression  
regressor = LinearRegression()  
regressor.fit(X_train, y_train)


y_pred = regressor.predict(X_test)

print('Точность модели: ',regressor.score(X_test,y_test))# Точность модели

#метрика модели
from sklearn import metrics
print (metrics.accuracy_score(y_test, y_pred))

#Кросс-валидация проверим точность модели с использованием 10-кратной перекрестной проверки
from sklearn.cross_validation import cross_val_score
#cross_val = cross_val_score(regressor, X, y, scoring='accuracy', cv=10)
#print(cross_val.mean())


plt.scatter(X_train,y_train,color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.title('Заработная плата vs Опыт(Тренировочные данные)')
plt.xlabel('Опыт в годах')
plt.ylabel("Заработная плата")
#plt.show()






'''
train = np.array([[1, 1], [1,2], [2,2], [2,3]])
result =np.dot(train, np.array([1, 2])) + 3

#pylab.scatter(map(lambda traain:train[0],))


#print (train)
#print (result)

model = linear_model.LinearRegression().fit(train,result)

#print ('R² Value: \n',model.score(train,result))

#print('Intercept: \n', model.intercept_)

#print('Coefficient: \n', model.coef_)
print('######################')

predict = model.predict([[1,3],[1,4],[1,5]])
print('predicted response:', predict )
metrics.mean_absolute_error(result,predict)'''
