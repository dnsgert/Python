import requests,os,sys, time
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import timedelta, datetime
from sqlalchemy.orm import sessionmaker




Base = declarative_base()
class Trade(Base):
               __abstract__ = True
               id = Column(Integer, primary_key=True)
               date= Column(String(10))
               time = Column(String(6))
               price = Column(Float)
               #price_max = Column(Float)
               #price_min = Column(Float)
               price_v= Column(Integer)
               price_go=Column(String(1))
               price_v_go=Column(String(1))
                                               
               def __init__(self, date, time, price, price_v, price_go, price_v_go):
                   self.date = date
                   self.time = time
                   self.price = price
                   self.price_v = price_v
                   self.price_go = price_go
                   self.price_v_go = price_v_go

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


def bol_fun(x):      
     if x>0 : res= '-'#+str(x) 
     if x<0 : res= '+'#+str(x)
     if x==0 : res='0'#+str(x)
     #print('return  ',res)
     return (res)

def sql_q():
    import sqlite3
    class_sp=['ltc_rub','ltc_btc','eth_btc','eth_ltc','eth_rub','btc_rub',
                  'bch_btc','bch_rub','bch_eth','xrp_eth','xrp_rub','xrp_btc',
                  'waves_btc','waves_rub','waves_eth']    
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    #sql=

    #print(sql)
    
    for i in range(len(class_sp)): 
        cursor.executescript('ALTER TABLE '+class_sp[i]+' RENAME TO '+class_sp[i]+'_old;'+\
            'CREATE TABLE '+class_sp[i]+\
            '( id INTEGER PRIMARY KEY NOT NULL, date VARCHAR(10), '+\
            'time VARCHAR(6), price float, price_v integer, '+\
            'price_go varchar(1), price_v_go varchar(1));'+\
            'INSERT INTO '+class_sp[i]+' (id, date, time, price, price_v) '+\
            'SELECT id, date, time, price, price_v '+\
            'FROM '+class_sp[i]+'_old;'+\
            'DROP TABLE '+class_sp[i]+'_old;')# Выполняем SQL-запрос
    
    conn.commit()
    cursor.close()    # Закрываем объект-курсора
    conn.close()

                           
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
            
               
        #Создаем список классов
        class_sp=[LTC_RUB,LTC_BTC,ETH_BTC,ETH_LTC,ETH_RUB,BTC_RUB,
                  BCH_BTC,BCH_RUB,BCH_ETH,XRP_ETH,XRP_RUB,XRP_BTC,
                  WAVES_BTC,WAVES_RUB,WAVES_ETH]    

        #текущая дата и врем
        d_date=datetime.now().strftime("%d.%m.%Y")
        t_time=datetime.now().strftime("%H:%M")

        #sql_q()
        print('                                   ')
        
        
        
        
        #Запись в базу
        Session = sessionmaker(bind=engine)
        session = Session()
        
        #s=session.query(class_sp[0]).filter(class_sp[0].id == (session.query(class_sp[0].price).count())).one()
        #print(s.price)
        #print(s.price_v)
                      
        for i in range(len(class_sp)):
            s=session.query(class_sp[i]).filter(class_sp[i].id == (session.query(class_sp[i].price).count())).one()
            #print(class_sp[i].__name__,response_json[class_sp[i].__name__]['buy_price'])
            session.add(class_sp[i](d_date,t_time,
                       float(response_json[class_sp[i].__name__]['buy_price']),
                       int(float(response_json[class_sp[i].__name__]['vol'])),
                       bol_fun(s.price-float(response_json[class_sp[i].__name__]['buy_price'])),
                       bol_fun(s.price_v-float(response_json[class_sp[i].__name__]['vol']))                                    ))
        
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
