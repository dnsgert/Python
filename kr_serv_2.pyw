import requests,os,sys, time, logging
import configparser
from logging.handlers import RotatingFileHandler
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

def f_config(i):

    if not os.path.exists('setting.ini'):
        config = configparser.ConfigParser()
        config.add_section("Settings")
        config.set("Settings", "Learn", "0")
        config.set("Settings", "Close", "0")
        app_log.info('Create ini file')
        with open('setting.ini', "w") as config_file:
            config.write(config_file)

    config = configparser.ConfigParser()
    config.read('setting.ini')
    if i==1:
        # Меняем значения из конфиг. файла.
        config.set('Settings', 'Close', '0')
        
        # Вносим изменения в конфиг. файл.
        with open('setting.ini', 'w') as config_file:
            config.write(config_file)
    else:
        # Читаем некоторые значения из конфиг. файла.
        result=[config.get("Settings", "Learn"),config.get("Settings", "Close")]
        return (result)

def bol_fun(x):      
     if x>0 : res= '-'#+str(x) 
     if x<0 : res= '+'#+str(x)
     if x==0 : res='0'#+str(x)
     #print('return  ',res)
     return (res)

                           
def html_err(url):
    try:
        response = requests.get(url, timeout=(5))#0.0001 для проверке
    
    except requests.exceptions.RequestException as e:# This is the correct syntax
        app_log.error(e)
        result=False
    else:
        result=True

    return (result)

def html_api(url_get):
    
    if html_err(url_get)==False:
        app_log.error('Сайт не доступен')
    else :
        # получить данные с биржи
        response = requests.get(url_get)
        # переводим данные во понятный программе формат
        response_json = response.json()
        
        #console.debug(response_json)
        engine = create_engine('sqlite:///base.db')
        
        
        #Проверка файла
        if os.path.isfile('base.db') == False: 
            #Base.metadata.create_all(engine)
            #console.debug('База успешно создана.',str(datetime.now().strftime("%H:%M")))
            app_log.crit('Base not found. Close program')
            sys.exit()
               
        #Создаем список классов
        class_sp=[LTC_RUB,LTC_BTC,ETH_BTC,ETH_LTC,ETH_RUB,BTC_RUB,
                  BCH_BTC,BCH_RUB,BCH_ETH,XRP_ETH,XRP_RUB,XRP_BTC,
                  WAVES_BTC,WAVES_RUB,WAVES_ETH]    

        #текущая дата и врем
        d_date=datetime.now().strftime("%d.%m.%Y")
        t_time=datetime.now().strftime("%H:%M")
            
        #Запись в базу
        Session = sessionmaker(bind=engine)
        session = Session()
                             
        for i in range(len(class_sp)):
            s=session.query(class_sp[i]).filter(class_sp[i].id == (session.query(class_sp[i].price).count())).one()
            #console.debug(class_sp[i].__name__,response_json[class_sp[i].__name__]['buy_price'])
            session.add(class_sp[i](d_date,t_time,
                       float(response_json[class_sp[i].__name__]['buy_price']),
                       int(float(response_json[class_sp[i].__name__]['vol'])),
                       bol_fun(s.price-float(response_json[class_sp[i].__name__]['buy_price'])),
                       bol_fun(s.price_v-float(response_json[class_sp[i].__name__]['vol']))                                    ))
        
        session.commit()
        session.close()
        console.debug('Данные добавлены в БД')

#настройка логирования
log_format=logging.Formatter('%(asctime)s [%(levelname)s] :  %(message)s', 
    datefmt='%d.%m.%Y %H:%M:%S')

# полный лог файл
f_hand = RotatingFileHandler('log.log', mode = 'a', maxBytes = 10485760,
                                 backupCount = 10, encoding = None, delay = 0)
f_hand.setFormatter(log_format)
f_hand.setLevel(logging.INFO)

# лог файл только ошибок
f_er_hand = RotatingFileHandler('error.log', mode = 'a', maxBytes = 10485760,
                                 backupCount = 10, encoding = None, delay = 0)
f_er_hand.setFormatter(log_format)
f_er_hand.setLevel(logging.ERROR)

#
d_hand=logging.StreamHandler()
d_hand.setLevel(logging.DEBUG)


# инициализация логирования
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

console = logging.getLogger('console')
console.setLevel(logging.DEBUG)
 
app_log.addHandler(f_hand)
app_log.addHandler(f_er_hand)
console.addHandler(d_hand)


app_log.info('Start program') # записываем сообщение

f_config(1) #обнуляем закрытие скрипта

tp=datetime.now() + timedelta(minutes=3)
html_api('https://api.exmo.com/v1/ticker/')
console.debug('Следующие обновление информации: '+str(tp.strftime("%H:%M")))

try:
    while True:
        #
        now = datetime.now().strftime("%H:%M")
        if tp.strftime("%H:%M")==now :
            print("\n"*50)
            html_api('https://api.exmo.com/v1/ticker/')
            tp=datetime.now() + timedelta(minutes=3)
            if f_config(0)[1]=='1':
                console.debug('Работа завершена')
                app_log.info('Close program')
                sys.exit()
                
            console.debug('Следующие обновление информации: '+str(tp.strftime("%H:%M")))
        time.sleep(10)
except KeyboardInterrupt:
    console.debug('Работа завершена')
    app_log.info('Close program')
