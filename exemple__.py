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
    cls()
    import requests

    try:
        req = requests.get('https://api.hitbtc.com/api/2/public/candles/'+\
                       'LTCBTC?period=M1&from=2015-01-01T00:00:00.000Z&till=2015-02-01T00:00:00.000Z&limit=1000')
        
    except Exception as e:
        print(e)
        sys.exit()
    if req.status_code!=200 :
        print(req.status_code)
        sys.exit()
    '''    
    print(req.encoding)  # returns 'utf-8'
    print(req.status_code) # returns 200
    print(req.elapsed)       # returns datetime.timedelta(0, 1, 666890)
    print(req.headers['Content-Type'])'''

    res_json = req.json()

    #print(res_json)

    #обработка формат даты
    for i in range(len(res_json)):
        res_json[i]['time']=str(res_json[i]['timestamp'])[11:-5]
        res_json[i]['date']=str(res_json[i]['timestamp'])[0:-14]
        

    from pandas.io.json import json_normalize

    res_json=json_normalize(res_json)
    print('LTCBTC')
    print(res_json[['date','time','open','close','min','max',
                    'volume','volumeQuote']])

def find_k():
    cls()
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
        cls()
        res_res=res_json.id.str.find(x)   
        if len(res_res)==0 : print('Ничего не найдено')
        else:
            print('Количество записей: '+str(len(res_res)))
            for i in range(len(res_res)):
                if res_res[i] != -1 : print(res_json.id[i])  
                
        print('<===========================================>')
        x=input('Закончить поиск? y/n: ')
        if x=='y' : break

#очиска экрана
def cls(): print("\n"*50)

        

def main(): #Mеню консоли
    
    menu = [' ',
         'Список команд ',
         '1 - Поиск пары',
         '2 - Создать БД',
         '3 - ','(========================) ',
         '4 - Выход' ]
    while True :
         
        for element in menu:
              print (element)
          
        a = input ('Введите команду ' )
     
        if a == '1' : find_k()
     
        elif a == '2': loadsql()
                  
        elif a == '3': pass
          
        elif a == '4' :
              cls()  
              print ('Работа программы завершена ')
              sys.exit()
        else :
            cls()
            print ("Водите только цифры от 1-4")
    

#{--------------------------------------------------------------}



if __name__ == "__main__":
    main()
    




