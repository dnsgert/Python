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
def save_result(df_date,fdate):

     i=0
     eth_df=pd.DataFrame()
     
     #фильтруем изменения по ETH_L
     for i in range(len(df_date.index)-1) :
        if float(df_date.loc[[i],'ETH_L'])!=float(df_date.loc[[i+1],'ETH_L']):
               eth_df=eth_df.append({'Trade':bol_fun(round(float(df_date.loc[[i],'ETH_L'])-float(df_date.loc[[i+1],'ETH_L']),3)),
                         'ETH_B':bol_fun(round(float(df_date.loc[[i],'ETH_B'])-float(df_date.loc[[i+1],'ETH_B']),4)), 
                         'ETH_R':bol_fun(int(df_date.loc[[i],'ETH_R'])-int(df_date.loc[[i+1],'ETH_R'])),
                         'LTC_R':bol_fun(int(df_date.loc[[i],'LTC_R'])-int(df_date.loc[[i+1],'LTC_R'])),
                         'BTC_R':bol_fun(int(df_date.loc[[i],'BTC_R'])-int(df_date.loc[[i+1],'BTC_R'])),
                         'LTC_B':bol_fun(round(float(df_date.loc[[i],'LTC_B'])-float(df_date.loc[[i+1],'LTC_B']),4))},ignore_index=True)
                                    
     #print(eth_df[['BTC_R','Trade']])
     
     # выбираем значение True
     df_true=eth_df[eth_df.Trade=='True']
     df_true.reset_index(inplace=True)
     del df_true['index']

     #Выбираем занчение false
     df_false=eth_df[eth_df.Trade=='False']
     df_false.reset_index(inplace=True)
     del df_false['index']
     '''
     print('выбираем значение True')
     print(df_true)
     print('')
     print('Выбираем занчение false')
     print(df_false)
     print('')
     print('Количество возрастание: ',len(df_true.index))
     print(' Количество понижение: ',len(df_false.index))
     print('')'''
     
     #создаем дата фрейм
     df_analiz=pd.DataFrame(columns=['Trade','up_hight','down_hight','up_low','down_low'])

     #Заполняем его
     i=0
     for i in range(len(df_true.columns)-1):
         df_analiz.loc[i,'Trade'], df_analiz.loc[i,'up_hight'], df_analiz.loc[i,'down_hight']=proc_df(df_true.iloc[:,[i]])

     for i in range(len(df_false.columns)-1):
         #print(i,'Print False : ', len(df_false.index)-1)
         df_analiz.loc[i,'Trade'], df_analiz.loc[i,'up_low'], df_analiz.loc[i,'down_low']=proc_df(df_false.iloc[:,[i]])
          
     #print(df_analiz)
     #print('Количество столбцов ',len(df_analiz.columns))
     #print('Количество строк ',len(df_analiz.index)-1)
     #print(df_result.iloc[0,1])
     for i in range(len(df_analiz.index)-1):

          for j in range(len(df_analiz.columns)-3):
               j=j+3
               if df_analiz.iloc[i,j]>=50:df_analiz.loc[len(df_analiz.index)]=[fdate,
                                 df_analiz.iloc[i,0],s_r(df_analiz.columns[j]),
                                 df_analiz.iloc[i,j],'down']
          for j in range(len(df_analiz.columns)-3):
               j=j+1
               #print(i,j)    
               if df_analiz.iloc[i,j]>=50:df_analiz.loc[len(df_analiz.index)]=[fdate,
                                 df_analiz.iloc[i,0],s_r(df_analiz.columns[j]),
                                 df_analiz.iloc[i,j],'up']
          i=i+1

     #print(df_analiz)
     #удаление строк     
     df_analiz.drop([0,1,2,3,4],inplace=True)

     #удаление столбца
     #del df_analiz['down_low']

     #переименовка столбцов
     df_analiz.rename(columns={'Trade': 'Date', 'up_hight': 'Trade','down_hight':'Result','up_low':'%','down_low':'Status'}, inplace=True)
     if len(df_analiz.index)==0:df_analiz=df_analiz.append({'Date':fdate,'Trade':None,'Result':None,'%':None,'Status':None},ignore_index=True)
     return (df_analiz)
     
# подсчет процентов
def proc_df(df_u):
     
     name=df_u.columns[0]
     yes=round(((len(df_u[df_u.iloc[:,0]=='True'].index))/((len(df_u))))*100)
     no=round(((len(df_u[df_u.iloc[:,0]=='False'].index))/((len(df_u))))*100)
     #print('Количество True: ',len(df_u[df_u.iloc[:,0]=='True'].index),'  ',yes,'%')
     #print('Количество False: ',len(df_u[df_u.iloc[:,0]=='False'].index),'  ',no,'%')
     return (name,yes,no)

#определение изменение
def bol_fun(x):      
     if x>0 : res= '-'#+str(x) 
     if x<0 : res= '+'#+str(x)
     if x==0 : res='0'#+str(x)
     #print('return  ',res)
     return (res)

#очиска экрана
def cls(): print("\n"*50)

#Проверка файла
if os.path.isfile('base.db') == False: 
    print('БД не найдена')

else :
    start_date=date(2019,2,21)#2019,2,21 
    con=create_engine('sqlite:///base.db')
    #отбираем по дате по паре
    sql='select * from eth_ltc where date='+start_date.strftime('"%d.%m.%Y"')
    #print(sql) 
    df=pd.read_sql(sql, con,index_col='id')
    
    #print(df.head(5)) 
    #print(df.tail(5))
    
    print('Таблица загружена',str(datetime.today().strftime("%H:%M")),
          'Число строк',len(df))
    print(' ')
    
    #фильтруем изменения по
    for i in range(1,len(df)):
        #print(i) 
        if df.loc[i,'price']!=df.loc[i+1,'price']:
               df.loc[i+1,'kurs']=bol_fun(df.loc[i,'price']-df.loc[i+1,'price'])
               df.loc[i+1,'key']=df.loc[i+1,'time']     
               df.loc[i+1,'v']=bol_fun(df.loc[i,'price_v']-df.loc[i+1,'price_v'])
               #print(i+1)          

    #df=df[df.key.notnull()] # убираем пустые значения
    #print(df)
    df=df[df.kurs=='+'] #выбираем по "+"
    print(df)

    #print(tuple(list(df.kurs)))
    sql='select time,price,price_v from eth_rub where date='+start_date.strftime('"%d.%m.%Y"')+' and time in '+str(tuple(list(df.key))) 
    #sql='select time,price,price_v from eth_rub where date='+start_date.strftime('"%d.%m.%Y"')+' and time="'+df.key.iloc[0]+'"'
    print(sql) 
    df_true=pd.read_sql(sql, con)
    print (df_true) 
     

    
    #end_date=date.today()#2019,2,25)
    #print(start_date,'  ',end_date) 
    #itog_result=pd.DataFrame(columns=['Date','Trade','Result','%','Status'])
    #d = start_date

    
    '''
    pbar = tqdm(total=(end_date-start_date).days,desc="Завершено: ",
                #ncols=3,leave=False,
                bar_format='{desc}: {percentage:3.0f}% | Количество операций: {n_fmt}/{total_fmt} | Время: [{elapsed}]')
    
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
       
    
    
         
    
    
    
    
