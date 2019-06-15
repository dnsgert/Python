import os
import time
import sys
import pandas as pd
from datetime import date, timedelta ,datetime
from sqlalchemy import create_engine


table_list=['ltc_rub','ltc_btc','eth_btc','eth_ltc','eth_rub','btc_rub',
                  'bch_btc','bch_rub','bch_eth','xrp_eth','xrp_rub','xrp_btc',
                  'waves_btc','waves_rub','waves_eth']


def shema():

    con=create_engine('sqlite:///base.db') #Путь к базе
    sql='select * from prog_up'
    df=pd.read_sql(sql,con)
    print(df)
    
#поиск пустых значений
def sql_null():
    import sqlite3

    #Проверка файла
    if os.path.isfile('base.db') == False: 
         print('БД не найдена')
         sys.exit()
         
    con = sqlite3.connect('base.db')
    z=0
    with con: 
         cur = con.cursor()

         cur.execute('select name from sqlite_master')
    
         class_sp=list(sum(cur.fetchall(),()))

         for i in range(len(class_sp)):

              cur.execute('SELECT * FROM '+class_sp[i])

              col_names = [cn[0] for cn in cur.description]
              
              for j in range(len(col_names)):
               
                  b=list(sum(cur.execute('SELECT * FROM '+class_sp[i]+\
                                 ' WHERE '+str(col_names[j])+' IS NULL').fetchall(),()))
                  if b:
                      print('Таблица '+str(class_sp[i])+\
                            ' Столбец '+str(col_names[j])+' id ',b[0])
                      print('')
                      z=z+1

    cur.close()#Закрываем объект-курсора
    con.close()
    print('Найдено результатов: ',z)


def analiz():
     
     #Проверка файла
     if os.path.isfile('base.db') == False: 
         print('БД не найдена')
         sys.exit()
    
     con=create_engine('sqlite:///base.db') #Путь к базе

     con.execute('DROP TABLE IF EXISTS prog_up')
     con.execute('DROP TABLE IF EXISTS prog_low') #если существует удаляем
       
        
     df_prog_up=pd.DataFrame()
     df_prog_low=pd.DataFrame()

     now=datetime.now()

     oz=['+','-']

     for j in range(len(table_list)):
     
     
          print(p_bar(j,len(table_list),now,'Анализ : '))

          for i in range(len(oz)):
               if oz[i]=='+':
                    #print ('Пара: '+table_list[j]+' условия +')
                    df_up=ozk(oz[i],table_list[j])
                    #print(df_up)
                    #print(' ')
               else:
                    #print ('Пара: '+table_list[j]+' условия -')
                    df_low=ozk(oz[i],table_list[j])
                    #print(df_low)

          df_up['pr']=None
          df_low['pr']=None
          df_up['cripta']=None
          df_low['cripta']=None
          #print(table_list[j],df_up)
          #print(table_list[j],df_low)
          for i in range(len(df_up)):
            
               col=df_up.loc[i,'size']+df_up[(
                   df_up.trade==df_up.loc[i,'trade'])&(
                   df_up.price_go!=df_up.loc[i,'price_go'])]['size'].values[0]     
               
               df_up.loc[i,'pr']=round(df_up.loc[i,'size']/col*100 )
               df_up.loc[i,'cripta']=table_list[j]

               col=df_low.loc[i,'size']+df_low[(
                   df_low.trade==df_low.loc[i,'trade'])&(
                   df_low.price_go!=df_low.loc[i,'price_go'])]['size'].values[0]     
               
               df_low.loc[i,'pr']=round(df_low.loc[i,'size']/col*100 )
               df_low.loc[i,'cripta']=table_list[j]


               #print(col)
          #print ('Пара: '+table_list[j]+' условия +')
          #print(df_up)       
          #print(' ')
          #print (df_low)
          #sys.exit()
          df_prog_up=df_prog_up.append(df_up,ignore_index=True,
                    sort=False)[['cripta','trade','price_go','pr']]
          df_prog_low=df_prog_low.append(df_low,ignore_index=True,
                    sort=False)[['cripta','trade','price_go','pr']]
     #print(df_prognoz)
          
     df_prog_up.to_sql('prog_up',con,index=False)
     df_prog_low.to_sql('prog_low',con,index=False)
     print(p_bar(1,1,now,'Анализ завершен: '))        


def p_bar(i,col,now,txt):
     #i - часть
     # col - общее количество
     # now - время начала
     # txt - строка
     
    m=str(((datetime.now()-now).seconds//60)%60)
    s=str((datetime.now()-now).seconds%60)
    
    if len(s)==1: s='0'+s
    
    return(txt+str(int(round((i/col)*100)))+'%  Время: ['+m+':'+s+']')
    

def conv_df(df_x,tip):
    #print(df_x)
    if len(df_x)==1 and tip=='int':
        #print('('+str(df_x[0])+')')
        return ('('+str(df_x[0])+')')
    
    if len(df_x)==1 and tip=='txt':
        #print("('"+str(df_x[0])+"')")
        return ("('"+str(df_x[0])+"')")
    
    if len(df_x)>1 and tip=='txt':
        return(str(tuple(list(df_x))))
    else:
        #print(str(tuple(df_x)))
        return (str(tuple(df_x)))


#case по столбцам
def s_r(x):
     return {'up_hight':'+',
             'down_hight':'-',
             'up_low':'+',
             'down_low':'-'}.get(x)

#обработка результатов
def ozk(status,table):
     
     start_date=date(2019,2,21)#(2019,2,21)#Начальная дата

     end_date=date.today()# Конечная дата

     con=create_engine('sqlite:///base.db') #Путь к базе

     df_res=pd.DataFrame(columns=['trade','','price_go'])

     while  start_date<=end_date: #диапазон дат для оработки
            
          #print(start_date)
          #отбираем по дате по паре
          sql='select * from '+table+\
          ' where date='+start_date.strftime('"%d.%m.%Y"')+' and price_go="'+status+'"'
          #print(sql)

          df=pd.read_sql(sql, con,index_col='id') #Получаем данные в панду
          #print(table,df)
          
          #print(tuple(df.index-1))

          #if len(df)==1:  
          if len(df)!=0:
              sql_2='select price_v_go from '+table+\
                   ' where date='+start_date.strftime('"%d.%m.%Y"')+\
                   ' and price_v_go!=0'+\
                   ' and id in'+conv_df(df.index-1,'int')#str(tuple(df.index-1))
               

              #print(sql_2)
              df_v=pd.read_sql(sql_2,con)
          
              sql_3='select time from '+table+\
                    ' where date='+start_date.strftime('"%d.%m.%Y"')+\
                    ' and id in'+conv_df(df.index-1,'int')
          
              df_time=pd.read_sql(sql_3,con)  
           
          
              df_v['trade']='V'
              df_v.rename(columns={'price_v_go': 'price_go'},inplace=True)
              #print(df_v) 
              #sys.exit()                 
                   
              for i in range(len(table_list)):#ищем изменения в других таблицах
                              
                    sql='select price_go from '+table_list[i]+\
                           ' where date='+start_date.strftime('"%d.%m.%Y"')+\
                           ' and price_go!=0'+\
                           ' and time in '+conv_df(df_time.time,'txt') 

                    #print(sql) 
                    if table_list[i]!=table: #пропускаем свою таблицу    
                         df_true=pd.read_sql(sql, con)
                         df_true['trade']=table_list[i]
                         df_res=df_res.append(df_true,ignore_index=True,sort=False)[['trade','price_go']]

              #print (df_res) 
              
           
              df_res=df_res.append(df_v,ignore_index=True,sort=False)[['trade','price_go']]

          start_date=start_date+timedelta(1)
          #print(df_res)    
     df_res=df_res.groupby(['trade','price_go'])['price_go'].agg(['size']).astype(int).sort_values(by='size',ascending=False).reset_index()
     #df_res['procent']=(round((df_res['size']/df_res['size'].sum())*100)).astype(int)
       
     #print (df_res)
     return (df_res)
  
     
#определение изменение
def bol_fun(x):      
     if x>0 : res= '-'#+str(x) 
     if x<0 : res= '+'#+str(x)
     if x==0 : res='0'#+str(x)
     
     return (res)

#очиска экрана
def cls(): print("\n"*50)

#============================================================#
menu = [' ',
     'Список команд ',
     '1 - Анализ',
     '2 - Поиск пустых данных',
     '3 - Просмотр схемы',
     '4 - Выход' ]
while True :
     
     for element in menu:
          print (element)
     print ('')     
          
     a = input ('Введите команду ' )
     
     if a == '1' : analiz()
     
     elif a == '2': sql_null()
      
     elif a == '3': shema()
          
     elif a == '4' :
          print ('Работа программы завершена ')
          sys.exit()
     else : print ("Вводите только цифры от 1-4")
  
 
 

      
         
   

    
'''
          df_prognoz[['cripta','trade','price_go','%_up','%_low']].sort_values(
                         by='%_up',ascending=False).to_sql('prognoz',con)
         
         df_date=df[df.Date==d.strftime('%d.%m.%Y')]
         if len(df_date.index)>0:
                  df_date.reset_index(inplace=True)
                  itog_result=itog_result.append(save_result(df_date,d.strftime('%d.%m.%Y')),ignore_index=True)
                    
         print()               
                        
         
         #print()
         #cls()
         d = d+timedelta(1)
         
    #df=df[df.key.notnull()] # убираем пустые значения    
        
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
    print()

    df_true.reset_index(inplace=True)# сброс индекса
    del df_true['index'] #удалить столбец
     
    df_analiz.drop([0,1,2,3,4],inplace=True)#удаление строк  

    переименовка столбцов
    df_analiz.rename(columns={'Trade': 'Date', 'up_hight': 'Trade','down_hight':'Result','up_low':'%','down_low':'Status'}, inplace=True) '''
    
    
         
    
    
    
    
