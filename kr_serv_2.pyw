import requests,os,sys, time
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta, datetime
from sqlalchemy.orm import sessionmaker
import pandas as pd


Base = declarative_base()
class Trade(Base):
               __abstract__ = True
               id = Column(Integer, primary_key=True)
               date= Column(String(10))
               time = Column(String(6))
               price = Column(Float)
               price_max = Column(Float)
               price_min = Column(Float)
               price_v= Column(Integer)
                                               
               def __init__(self, date, time, price, price_max,price_min,price_v):
                   self.date = date
                   self.time = time
                   self.price = price
                   self.price_max = price_max
                   self.price_min = price_min
                   self.price_v = price_v

class LTC_RUB(Trade):
       __tablename__='ltc_rub'
              
class ETH_LTC(Trade):
       __tablename__= 'eth_ltc'

class LTC_BTC(Trade):
       __tablename__= 'ltc_btc'

class ETH_BTC(Trade):
       __tablename__= 'eth_btc'

class BTC_RUB(Trade):
       __tablename__= 'btc_rub'
       
class ETH_RUB(Trade):
       __tablename__= 'eth_rub'
       
class BCH_BTC(Trade):
       __tablename__= 'bch_btc'

class BCH_RUB(Trade):
       __tablename__= 'bch_rub'
       
class BCH_ETH(Trade):
       __tablename__= 'bch_eth'

class XRP_ETH(Trade):
       __tablename__= 'xrp_eth'

class XRP_RUB(Trade):
       __tablename__= 'xrp_rub'
       
class XRP_BTC(Trade):
       __tablename__= 'xrp_btc'

class WAVES_BTC(Trade):
       __tablename__= 'waves_btc'

class WAVES_RUB(Trade):
       __tablename__= 'waves_rub'
       
class WAVES_ETH(Trade):
       __tablename__= 'waves_eth'       


def convert():

    #Проверка файла
    if os.path.isfile('file.csv') == False: 
        print('БД не найдена')

    else :
        df=pd.read_csv('file.csv')
        df_title=df[['LTC_R','LTC_B','ETH_L','ETH_B','BTC_R','ETH_R','Date','Time',]]
        print(df_title.tail(5))
        print('Таблица загружена',str(datetime.today().strftime("%H:%M")),
          'Число строк',df.Date.count())
        print(' ')

        #Создаем список классов
        class_sp=[LTC_RUB,LTC_BTC,ETH_BTC,ETH_LTC,ETH_RUB,BTC_RUB]
        class_sp2=['LTC_R','LTC_B','ETH_B','ETH_L','ETH_R','BTC_R']
        now=datetime.now()
        engine = create_engine('sqlite:///base.db')
        
        #Запись в базу
        Session = sessionmaker(bind=engine)
        session = Session()
        
        for i in range(df.Date.count()):
            proc_result=datetime.now()-now
            print('Выполено: ',int(round((i/df.Date.count())*100)),'% ',
                  ' Время: [',proc_result.seconds,']')
            for j in range(len(class_sp)):
                #print(class_sp[j],df.Date[i],df.Time[i])
                session.add(class_sp[j](df.Date[i],df.Time[i],
                       float(df.loc[i,class_sp2[j]]),
                       float(df.loc[i,(class_sp2[j]+'_MAX')]),
                       float(df.loc[i,(class_sp2[j]+'_LOW')]),
                       float(df.loc[i,(class_sp2[j]+'_V')])       ))
        session.commit()
        session.close()
        print('Конвертация завершена')
        time.sleep(5)


        
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
            convert()
               
        #Создаем список классов
        class_sp=[LTC_RUB,LTC_BTC,ETH_BTC,ETH_LTC,ETH_RUB,BTC_RUB,
                  BCH_BTC,BCH_RUB,BCH_ETH,XRP_ETH,XRP_RUB,XRP_BTC,
                  WAVES_BTC,WAVES_RUB,WAVES_ETH]    

        #текущая дата и врем
        d_date=datetime.now().strftime("%d.%m.%Y")
        t_time=datetime.now().strftime("%H:%M")

        #convert()
        print('                                   ')   

        #Запись в базу
        Session = sessionmaker(bind=engine)
        session = Session()
                       
        for i in range(len(class_sp)):
            print(class_sp[i].__name__,response_json[class_sp[i].__name__]['buy_price'])
            session.add(class_sp[i](d_date,t_time,
                       float(response_json[class_sp[i].__name__]['buy_price']),
                       float(response_json[class_sp[i].__name__]['high']),
                       float(response_json[class_sp[i].__name__]['low']),
                       int(float(response_json[class_sp[i].__name__]['vol'])) ))
        
        session.commit()
        session.close()
        print('Данные добавлены в БД')

    

def unix_time(unix_vvod):
    return (datetime.datetime.fromtimestamp(int(unix_vvod)).strftime("%Y-%m-%d %H:%M"))
        
def time_unix (time_vvod):
    return (int(time.mktime(time.strptime(time_vvod, '%Y-%m-%d %H:%M:%S'))))

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
            tp=datetime.now() + timedelta(minutes=3)
            print('Следующие обновление информации: ',tp.strftime("%H:%M"))
        time.sleep(2)
except KeyboardInterrupt:
    print('Работа завершена')
