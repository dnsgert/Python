import pandas as pd

import datetime,time, sys

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
    #print(unix_vvod)
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
        
def loadsql():
    v_list=['BTCUSD','DOGEBTC','DOGEUSD','ETHBTC','LTCBTC','LTCUSD','LTCETH',
            'XRPBTC','WAVESBTC','DOGEETH','ETHUSD','XRPETH']
    x=input('Ведите пару: ')
    import requests

    try:
        #req = requests.get('https://api.hitbtc.com/api/2/public/candles/'+\
         #              'ETHBTC?period=D1&from=2016-07-01T00:00:00.000Z&till=2016-07-30T00:00:00.000Z')
        req=requests.get('https://api.hitbtc.com/api/2/public/symbol/'+str(x))
    except Exception as e:
        print(e)
        sys.exit()
    '''    
    print(req.encoding)  # returns 'utf-8'
    print(req.status_code) # returns 200
    print(req.elapsed)       # returns datetime.timedelta(0, 1, 666890)
    print(req.headers['Content-Type'])'''

    res_json = req.json()

    print(res_json)

    #обработка формат даты
    for i in range(len(res_json)):
        res_json[i]['timestamp']=str(res_json[i]['timestamp'])[0:-14]

    from pandas.io.json import json_normalize

    res_json=json_normalize(res_json)
    print('ETHBTC')
    print(res_json[['timestamp','close']])

def find_k():
    
    import requests

    try:
        req=requests.get('https://api.hitbtc.com/api/2/public/symbol/')
    except Exception as e:
        print(e)
        sys.exit()

    res_json = req.json()

    from pandas.io.json import json_normalize

    res_json=json_normalize(res_json)
    
    while True:
        print('')
        x=input('Ведите валюту: ')
        print('')
        res_res=res_json.id.str.find(x)   
        if len(res_res)==0 : print('Ничего не найдено')
        else: print(res_res)    
        print('<===========================================>')
        x=input('Закончить поиск? y/n: ')
        if x=='y' : break
        

def main(): #Mеню консоли

    menu = [' ',
         'Список команд ',
         '1 - Поиск пары',
         '2 - Поиск пустых данных',
         '3 - ','(========================) ',
         '4 - Выход' ]
    while True :
     
        for element in menu:
              print (element)
          
        a = input ('Введите команду ' )
     
        if a == '1' : find_k()
     
        elif a == '2': pass
      
        elif a == '3': pass
          
        elif a == '4' :
              print ('Работа программы завершена ')
              sys.exit()
        else : print ("Водите только цифры от 1-6")
    

#{--------------------------------------------------------------}



if __name__ == "__main__":
    main()
    




