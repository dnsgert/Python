import requests, time, datetime, lxml.html,os
from io import StringIO
import pandas as pd
from lxml import html,etree
import json
from datetime import timedelta, datetime
import numpy as np

def html_css(url):
    r = requests.get(url)

    print(r.encoding)     # Кодировка по умолчанию ISO-8859-1
    r.encoding = 'cp1251' # Указываем настоящюю кодировку документа

    # Формируем дерево элементов
    root = html.parse(StringIO(r.text)).getroot()

    # Выбираем нужную таблицу через смежные селекторы и записи этой таблицы начиная
    # с 4 строки
    result = root.cssselect('div.weather__content a[aria-label]')
    #print(result.text_content().strip())
    #print(result)
    #item = rows[0]

    # Печатаем первый элемент результата поиска
    #print(html.tostring(item,encoding='unicode'))
    
    
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

def html_json(url_get):
    r = requests.get(url)
    data = []
    mementos = r.json()['mementos']['list']
    for memento in mementos:
        data.append(D.get(memento['uri']))
    # print xpath.get(data[10], '//table')
    print (type(data[0]))
    # print data[10]
    print (len(data))
    json_data = json.loads(data)
    print (type(json_data[0]))

    

def html_lxml(url_get):

    if html_err(url_get)==False:
        res='Сайт не доступен'
    else :
        response = requests.get(url_get)

        # Преобразование тела документа в дерево элементов (DOM)

        parsed_body = lxml.html.document_fromstring(response.content)

        # Выполнение xpath в дереве элементов
        print(parsed_body.xpath('//title/text()')) # Получить title страницы 
    
        print()
        #res=parsed_body.xpath('//*[@id="investbox_boxes_list"]/tbody') # Получить аттрибут href для всех ссылок
        #parsed_body.xpath('//*[@class="home-link home-link_black_yes weather__grade"]/@style')
        res=parsed_body.xpath('//*[@id="investbox_boxes_list"]/tbody')#//tr//text()')
       
    return (res)

def html_table(url_get):
    if html_err(url_get)==False:
        res='Сайт не доступен'
    else :
        # получить данные с биржи
        response = requests.get(url_get)
        # переводим данные во понятный программе формат
        response_json = response.json()
        print('                                   ')
        for pair in response_json:
            if pair=='LTC_RUB' :
                print('Валюта                ',pair)
                print('Покупка               ',response_json[pair]['buy_price'],'p.')
                print('Продажа               ',response_json[pair]['sell_price'],'p.')
                print('Max цена              ',response_json[pair]['high'],'p.')
                print('Min цена              ',response_json[pair]['low'],'p.')
                print('Cумма сделок 24 часа  ',response_json[pair]['vol_curr'],'p.')
                print('Объем сделок 24 часа  ',response_json[pair]['vol'])
                print('Дата                  ',unix_time(response_json[pair]['updated']))
            if pair=='ETH_LTC' :
                print('Валюта                ',pair)
                print('Покупка               ',response_json[pair]['buy_price'])
                print('Продажа               ',response_json[pair]['sell_price'])
                print('Max цена              ',response_json[pair]['high'],'')
                print('Min цена              ',response_json[pair]['low'],'')
                print('Cумма сделок 24 часа  ',response_json[pair]['vol_curr'],'')
                print('Объем сделок 24 часа  ',response_json[pair]['vol'])
                print('Дата                  ',unix_time(response_json[pair]['updated']))
                print (' ')

def html_api(url_get):

    if html_err(url_get)==False:
        res='Сайт не доступен'
    else :
        # получить данные с биржи
        response = requests.get(url_get)
        # переводим данные во понятный программе формат
        response_json = response.json()
        
        #print(response_json)

        df= pd.DataFrame()
        '''{'LTC_RUB':[],'LTC_RUB_MAX':[],'LTC_RUB_LOW':[],
                          'LTC_RUB_V':[],'ETH_LTC':[],
                          'ETH_LTC_MAX':[],'ETH_LTC_LOW':[],
                          'ETH_LTC_V':[],'LTC_BTC':[],'LTC_BTC_MAX':[],
                          'LTC_BTC_LOW':[],'LTC-BTC_V':[],
                          'ETH-BTC':[],'ETH-BTC_MAX':[],'ETH-BTC_LOW':[],
                          'ETH-BTC_V':[],
                           'Date':[],'Time':[]})'''
        #Проверка файла
        if os.path.isfile('file.csv') == True: 
            df=pd.read_csv('file.csv')
            print('Таблица загружена',str(datetime.now().strftime("%H:%M")))
            
        print('                                   ')   
                
        #Add new sting    
        df = df.append({'Time':datetime.now().strftime("%H:%M"),
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
        '''print(df_eth_l)
        print(df_ltc_b)
        print (df_eth_b)
        print (df_btc_r)
        print(df_eth_r)'''
        print (' ')
        print('Таблица сохранена')
        


        
def unix_time(unix_vvod):
    time_u=datetime.datetime.fromtimestamp(int(unix_vvod)).strftime("%Y-%m-%d %H:%M")
    return (time_u)
        
def time_unix (time_vvod):
    d = int(time.mktime(time.strptime(time_vvod, '%Y-%m-%d %H:%M:%S')))
    return (d)


    
#html_api('https://api.exmo.com/v1/ticker/')
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

