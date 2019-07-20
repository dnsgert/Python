import pandas as pd
import datetime,time, sys, os
from sqlalchemy import create_engine, exc 

def unix_time(unix_vvod):
    #print(unix_vvod)
    return (datetime.datetime.fromtimestamp(int(unix_vvod)).strftime("%d.%m.%Y")) #%H:%M")))

def bin_info(symbol):
    from binance.client import Client
    client = Client('ao6y7zDn1Qx6in6dI39kZcQzMjDp9tnLbUXrxhXgnEdhEVm28Dhpg4sODb9fuKLn',
                'bmzJiZ6Fr8KapbzOgZBkzdZ6w4AehSbc7gRji5gbxF6p3pavwTlWB5W4DEivolPW')

    from binance.exceptions import BinanceAPIException
    
    res = client.get_symbol_info(symbol)
    if res==None: res='None'    
    else: res=res['status']#get('status')
    #print(res)
    return(symbol+' : '+res)

#{=================================================================}
table_list={'ltc_btc':'LTCBTC','eth_btc':'ETHBTC','ltc_eth':'LTCETH',
            'xrp_btc':'XRPBTC','btc_usdt':'BTCUSDT','ltc_usdt':'LTCUSDT',
            'waves_btc':'WAVESBTC','doge_btc':'DOGEBTC','waves_eth':'WAVESETH',
            'doge_usdt':'DOGEUSDT','xrp_eth':'XRPETH','xrp_usdt':'XRPUSDT',
            'waves_usdt':'WAVESUSDT','eth_usdt':'ETHUSDT'}

con=create_engine('sqlite:///arhiv.db') #Путь к базе

#Проверка файла
if os.path.isfile('arhiv.db') == False: 
        print('БД не найдена')
        sys.exit()
try:
    for key in table_list: 
        con.execute('DROP TABLE IF EXISTS '+table_list.get(key))#если существует удаляем  
         

except Exception as e:
    print(e)
    sys.exit()



#for key in table_list:
    #print(bin_info(table_list.get(key)))


from binance.client import Client
client = Client('ao6y7zDn1Qx6in6dI39kZcQzMjDp9tnLbUXrxhXgnEdhEVm28Dhpg4sODb9fuKLn',
                'bmzJiZ6Fr8KapbzOgZBkzdZ6w4AehSbc7gRji5gbxF6p3pavwTlWB5W4DEivolPW')

from binance.exceptions import BinanceAPIException
try:
    #res = client.get_symbol_ticker()
    klines = client.get_historical_klines("LTCBTC", Client.KLINE_INTERVAL_1DAY, "01 Jul, 2011", "20 Jul, 2019")
    
except BinanceAPIException as e:
    print(e)
    sys.exit()
data=pd.DataFrame(klines,columns=['Date','Open','Hight','Low','Close','Volume','7','Quote V','9','Active','Kotirov','Ignore'])

#переводим время
for i in range(len(data)):
    data.loc[i,'Date']=unix_time(str(data.loc[i,'Date'])[0:-3])

data=data.drop(columns=['7','9','Ignore'])#удаляем ненужные колонки    
#print(data.columns.values)# имена колонок

data.to_sql('LTCBTC',con,index=False)#запись в SQL
print('Данные успешно добавлены. Количство: '+str(len(data)))
    
'''
for i in range(len(res)):
    print(res[i].get('symbol'))'''
