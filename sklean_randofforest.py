from sklearn import tree
import pandas as pd
import time
import matplotlib.pyplot as plt

from sqlalchemy import create_engine, exc

#import matplotlib.pyplot as plt
con=create_engine('sqlite:///arhiv.db') #Путь к базе

#загружаем data
start=time.time()
print('3агружаю данные SQL')
sql_pr='select * from BTCUSD'
df_pr=pd.read_sql(sql_pr,con)
end=time.time()-start
print('Даныые успешно загружены: ',round(end),' sec')

X = df_pr.values[::, 4:8]
y = df_pr.values[::, 2:3]


#Проверка качество модели
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)


from sklearn.linear_model import LinearRegression

model = LinearRegression().fit(X_train,y_train)
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error,       r2_score

print('MSE train: {:.3f}, test: {:.3f}'.format(
        mean_squared_error(y_train, y_train_pred),
        mean_squared_error(y_test, y_test_pred)))
print('R^2 train: {:.3f}, test: {:.3f}'.format(
        r2_score(y_train, y_train_pred),
        r2_score(y_test, y_test_pred)))





print('coefficient of determination:', model.score(X_train, y_train))
print('Slope: ',model.coef_)
print('Intercept: ',model.intercept_)

plt.scatter(X_test, y_test,  color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()




