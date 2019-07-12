import pandas as pd

import datetime,time

from sqlalchemy import create_engine, exc 

def line_reg(X,y):


#кодирования строк, сопоставим каждое значение с числом:
#dataset.sex=dataset.sex.map({'man':1,
#                           'fem':0 })

    from sklearn.linear_model import LinearRegression
    X=dataset.iloc[:,[0]].values
    y=dataset.iloc[:,1].values
    #print(dataset)

#Обучение модели
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


    model = LinearRegression().fit(X, y)

    print(model.score(X, y))

    '''from sklearn.model_selection import cross_val_score
    cross_val = cross_val_score(model, X_test, y_test, cv=5)
    print ('Кросс-валидация: \n',cross_val.mean())'''

    print(model.coef_)

    print(model.intercept_ )

    print(model.predict([[]]))

def unix_time(unix_vvod):
    print(unix_vvod)
    return (datetime.datetime.fromtimestamp(int(unix_vvod)).strftime("%d.%m.%Y")) #%H:%M")))

def sql_error(sql,conn):#
    #print(sql)
    
    try:
        res=conn.execute(sql)
        
    except exc.SQLAlchemyError as ex:
        print(ex,'Работа программы завершина аварийно /n')
        sys.exit()    
    res=res.fetchone()    
    if len(res)==1 :
        #print('1',res)
        return(res[0]) 
    else : return(res)      
        

#{--------------------------------------------------------------}
val='btc_rub'   
con=create_engine('sqlite:///base.db') #Путь к базе

sql=sql_error('select date from '+val+' where id=(select min(id) from '+val+')',con)
print(sql)


from binance.client import Client
client = Client('ao6y7zDn1Qx6in6dI39kZcQzMjDp9tnLbUXrxhXgnEdhEVm28Dhpg4sODb9fuKLn',
                'bmzJiZ6Fr8KapbzOgZBkzdZ6w4AehSbc7gRji5gbxF6p3pavwTlWB5W4DEivolPW')
klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_1DAY, "30 Dec, 2017", "1 Jan, 2018")

data=pd.DataFrame(klines,columns=['Date','Open','Hight','Low','Close','Volume','7','Quote V','9','Active','Kotirov','Ignore'])
data.loc[0,'Date']=unix_time(str(data.loc[0,'Date'])[0:-3])
print(data[['Date','Open','Hight','10']])
