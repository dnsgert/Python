import os,time
import pandas as pd
from datetime import date, timedelta ,datetime
from sqlalchemy import create_engine

#case по столбцам
def s_r(x):
     return {'up_hight':'+',
             'down_hight':'-',
             'up_low':'+',
             'down_low':'-'}.get(x)

#обработка результатов
def analiz_result():

     
     #df_true.reset_index(inplace=True)# сброс индекса
     #del df_true['index'] #удалить столбец
     
     #df_analiz.drop([0,1,2,3,4],inplace=True)#удаление строк  

     #переименовка столбцов
     #df_analiz.rename(columns={'Trade': 'Date', 'up_hight': 'Trade','down_hight':'Result','up_low':'%','down_low':'Status'}, inplace=True)
     
     
#определение изменение
def bol_fun(x):      
     if x>0 : res= '-'#+str(x) 
     if x<0 : res= '+'#+str(x)
     if x==0 : res='0'#+str(x)
     #print('return  ',res)
     return (res)

#очиска экрана
def cls(): print("\n"*50)

#============================================================#

#Проверка файла
if os.path.isfile('base.db') == False: 
    print('БД не найдена')
    sys.exit()

table_list=['ltc_rub','ltc_btc','eth_btc','eth_ltc','eth_rub','btc_rub',
                  'bch_btc','bch_rub','bch_eth','xrp_eth','xrp_rub','xrp_btc',
                  'waves_btc','waves_rub','waves_eth']

start_date=date(2019,2,21)#(2019,2,21)#Начальная дата

end_date=date.today()# Конечная дата

con=create_engine('sqlite:///base.db') #Путь к базе



df_res=pd.DataFrame(columns=['trade','','price_go'])

while  start_date<=end_date: #диапазон дат для оработки

     #print(start_date)
     #отбираем по дате по паре
     sql='select * from '+table_list[3]+\
     ' where date='+start_date.strftime('"%d.%m.%Y"')+' and price_go="+"'
     #print(sql)


     df=pd.read_sql(sql, con,index_col='id') #Получаем данные в панду

     #print(df)
    
     #print('Таблица загружена',str(datetime.today().strftime("%H:%M")),
          #'Число строк',len(df))
     #print(' ')
        
     #print(tuple(list(df.kurs)))
     #df=df[df.key.notnull()] # убираем пустые значения
     #print(df)

         
     for i in range(len(table_list)):#ищем изменения в других таблицах
           
           if   len(df)==1:  
                tt=("('"+list(df['time'])[0]+"')")
           else: tt=tuple(list(df.time))
           
           sql='select price_go from '+table_list[i]+\
                  ' where date='+start_date.strftime('"%d.%m.%Y"')+\
                  ' and price_go!=0'+\
                  ' and time in '+str(tt) 

           #print(sql) 
           if table_list[i]!=table_list[3]: #пропускаем свою таблицу    
                df_true=pd.read_sql(sql, con)
                df_true['trade']=table_list[i]
                df_res=df_res.append(df_true,ignore_index=True,sort=False)[['trade','price_go']]

     #print (df_res) 
     start_date=start_date+timedelta(1)
df_res=df_res.groupby(['trade','price_go'])['price_go'].agg(['size']).astype(int).sort_values(by='size',ascending=False).reset_index()
#df_res['procent']=(round((df_res['size']/df_res['size'].sum())*100)).astype(int)

print ('Пара: '+table_list[3]+' условия при росте' )
print('')
print (df_res)      

 
#print(start_date,'  ',end_date) 

      
         
   

    
'''
    
    
    for i in range((pbar.total)+1):
    
         
         df_date=df[df.Date==d.strftime('%d.%m.%Y')]
         if len(df_date.index)>0:
                  df_date.reset_index(inplace=True)
                  itog_result=itog_result.append(save_result(df_date,d.strftime('%d.%m.%Y')),ignore_index=True)
                    
         print()               
         pbar.update(1)                   
         
         #print()
         #cls()
         d = d+timedelta(1)
         
                
         
    pbar.close()     
    #убираем пустые значения
    itog_result=itog_result[itog_result['Trade'].notnull()]
    
    #print(itog_result)
    #cls()
    
    
    #Выбираем по столбцу, групируем по количеству, сортируем и сбрасываем индекс   
    grouped=itog_result[itog_result.Status=='up'].groupby(['Trade','Result','Status'])['%'].agg(['size']).astype(int).sort_values(by='size',ascending=False).reset_index()
    grouped['procent']=(round((grouped['size']/grouped['size'].sum())*100)).astype(int)
    print('Условия при повышении')
    print(grouped)
    
    
    grouped1=itog_result[itog_result.Status=='down'].groupby(['Trade','Result','Status'])['%'].agg(['size']).sort_values(by='size',ascending=False).reset_index()
    grouped1['procent']=(round((grouped1['size']/grouped1['size'].sum())*100)).astype(int)   
    print('Условия при понижении')
    print(grouped1)
    print()'''
       
    
    
         
    
    
    
    
