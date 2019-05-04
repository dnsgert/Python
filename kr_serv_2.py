import requests,os, time
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta, datetime
from sqlalchemy.orm import sessionmaker
t_name='ltc_rub'
Base = declarative_base()
class LTC_RUB(Base):
               __tablename__= t_name
               id = Column(Integer, primary_key=True)
               date= Column(String(10))
               time = Column(String(6))
               price = Column(Integer)
               price_max = Column(Integer)
               price_min = Column(Integer)
               price_v= Column(Integer)
                                               
               def __init__(self, date, time, price, price_max,price_min,price_v):
                   self.date = date
                   self.time = time
                   self.price = price
                   self.price_max = price_max
                   self.price_min = price_min
                   self.price_v = price_v

#class ETH_LTC(LTC_RUB,Base):
#        __tablename__= 'eth_ltc'
        
def html_err(url):
    try:
        response = requests.get(url, timeout=(5))#0.0001 для проверке
    
    except requests.exceptions.RequestException as e:# This is the correct syntax
        print()
        print(e)
        print()
        result=False
    else:
        result=True

    return (result)

def html_api(url_get):
    
    if html_err(url_get)==False:
        res='Сайт не доступен'
    else :
        # получить данные с биржи
        response = requests.get(url_get)
        # переводим данные во понятный программе формат
        response_json = response.json()
        
        #print(response_json)
        engine = create_engine('sqlite:///base.db')
        
        
        #Проверка файла
        if os.path.isfile('base.db') == False: 
            Base.metadata.create_all(engine)
            print('База успешно создана.',str(datetime.now().strftime("%H:%M")))
            
               
            #print('Таблица загружена',str(datetime.now().strftime("%H:%M")))
            
        print('                                   ')   
        Session = sessionmaker(bind=engine)
        session = Session()
        #Add new sting
        '''ltc_rub=LTC_RUB(datetime.now().strftime("%d.%m.%Y"),datetime.now().strftime("%H:%M"),
                       int(float(response_json['LTC_RUB']['buy_price'])),int(float(response_json['LTC_RUB']['high'])),
                       int(float(response_json['LTC_RUB']['low'])),float(response_json['LTC_RUB']['vol']))'''
        session.add_all([LTC_RUB(datetime.now().strftime("%d.%m.%Y"),datetime.now().strftime("%H:%M"),
                       int(float(response_json['LTC_RUB']['buy_price'])),int(float(response_json['LTC_RUB']['high'])),
                       int(float(response_json['LTC_RUB']['low'])),int(float(response_json['LTC_RUB']['vol'])))])
                 
        session.commit()
        session.close()
        '''
        {'Time':datetime.now().strftime("%H:%M"),
                        'Date':datetime.now().strftime("%d.%m.%Y"),
                        'LTC_R':float(response_json['LTC_RUB']['buy_price']),
                        'LTC_R_MAX':float(response_json['LTC_RUB']['high']),
                        'LTC_R_LOW':float(response_json['LTC_RUB']['low']),
                        'LTC_R_V':float(response_json['LTC_RUB']['vol']),
                        
                        'ETH_L':round(float(response_json['ETH_LTC']['buy_price']),2),
                        'ETH_L_MAX':round(float(response_json['ETH_LTC']['high']),2),
                        'ETH_L_LOW':round(float(response_json['ETH_LTC']['low']),2),
                        'ETH_L_V':round(float(response_json['ETH_LTC']['vol'])),
                        'LTC_B':round(float(response_json['LTC_BTC']['buy_price']),4),
                        'LTC_B_MAX':round(float(response_json['LTC_BTC']['high']),4),
                        'LTC_B_LOW':round(float(response_json['LTC_BTC']['low']),4),
                        'LTC_B_V':round(float(response_json['LTC_BTC']['vol']),4),
                        'ETH_B':round(float(response_json['ETH_BTC']['buy_price']),4),
                        'ETH_B_MAX':round(float(response_json['ETH_BTC']['high']),4),
                        'ETH_B_LOW':round(float(response_json['ETH_BTC']['low']),4),
                        'ETH_B_V':round(float(response_json['ETH_BTC']['vol']),4),
                        'BTC_R':round(float(response_json['BTC_RUB']['buy_price'])),
                        'BTC_R_MAX':round(float(response_json['BTC_RUB']['high'])),
                        'BTC_R_LOW':round(float(response_json['BTC_RUB']['low'])),
                        'BTC_R_V':round(float(response_json['BTC_RUB']['vol'])),
                        'ETH_R':float(response_json['ETH_RUB']['buy_price']),
                        'ETH_R_MAX':float(response_json['ETH_RUB']['high']),
                        'ETH_R_LOW':float(response_json['ETH_RUB']['low']),
                        'ETH_R_V':float(response_json['ETH_RUB']['vol']),
                        },ignore_index=True)

        df[['LTC_R','LTC_R_MAX','LTC_R_LOW','LTC_R_V','ETH_R','ETH_R_MAX','ETH_R_LOW',
            'ETH_R_V','ETH_L_V','LTC_B_V','BTC_R','BTC_R_MAX','BTC_R_LOW','BTC_R_V']]=df[['LTC_R','LTC_R_MAX','LTC_R_LOW','LTC_R_V','ETH_R','ETH_R_MAX','ETH_R_LOW',
            'ETH_R_V','ETH_L_V','LTC_B_V','BTC_R','BTC_R_MAX','BTC_R_LOW','BTC_R_V']].round().astype(int)
        #Запись данных в файл
        df.to_csv('file.csv',encoding='utf-8',index=False)
        print ('')
        
        df1=df[['LTC_R','LTC_B','ETH_L','ETH_B','BTC_R','ETH_R','Date','Time',]]
        df_ltc_r=df[['LTC_R','LTC_R_MAX','LTC_R_LOW','LTC_R_V']]
        df_eth_l=df[['ETH_L','ETH_L_MAX','ETH_L_LOW','ETH_L_V']]
        df_ltc_b=df[['LTC_B','LTC_B_MAX','LTC_B_LOW','LTC_B_V']]
        df_eth_b=df[['ETH_B','ETH_B_MAX','ETH_B_LOW','ETH_B_V']]
        df_btc_r=df[['BTC_R','BTC_R_MAX','BTC_R_LOW','BTC_R_V']]
        df_eth_r=df[['ETH_R','ETH_R_MAX','ETH_R_LOW','ETH_R_V']]
        print(df1.tail(25))
        print(df_eth_l)
        print(df_ltc_b)
        print (df_eth_b)
        print (df_btc_r)
        print(df_eth_r)
        print (' ')
        print('Таблица сохранена'''

    

def unix_time(unix_vvod):
    time_u=datetime.datetime.fromtimestamp(int(unix_vvod)).strftime("%Y-%m-%d %H:%M")
    return (time_u)
        
def time_unix (time_vvod):
    d = int(time.mktime(time.strptime(time_vvod, '%Y-%m-%d %H:%M:%S')))
    return (d)

tp=datetime.now() + timedelta(minutes=3)
html_api('https://api.exmo.com/v1/ticker/')
print('Следующие обновление информации: ',tp.strftime("%H:%M"))

try:
    while True:
        #
        now = datetime.now().strftime("%H:%M")
        if tp.strftime("%H:%M")==now :
            print("\n"*50)
            html_api('https://api.exmo.com/v1/ticker/')
            tp=datetime.now() + timedelta(minutes=5)
            print('Следующие обновление информации: ',tp.strftime("%H:%M"))
        time.sleep(2)
except KeyboardInterrupt:
    print('Работа завершена')
