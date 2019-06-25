import sys
import pandas as pd
#import sqlite3
from sqlalchemy import create_engine, exc


def sql_error(sql,conn):#
    print(sql)
    
    try:
        conn.execute(sql)
        
    except exc.SQLAlchemyError as ex:
        print(ex,'Работа программы завершина аварийно /n')
        
        sys.exit()    

    return(sql)
    
def sql_obr(query):#
    
    query.fetchone()
    print(query)
    if query.fetchone()==None :
        print('1')
        return(query.fetchone()) 
    else : return(query.fetchone()[0])

val='btc_rub'

con=create_engine('sqlite:///base.db') #Путь к базе

#загружаем прогноз
sql_pr=sql_error('select * from prog_up where cripta="'+val+'"',con)

df_pr=pd.read_sql(sql_pr,con)
    
df_pr=df_pr[df_pr['pr']>59].sort_values(
            by='pr',ascending=False).reset_index(drop=True)
df_pr['res']=None
df_pr['itog']=None
#print('Прогноз \n',df_pr)

#выбираем первую запись
sql=sql_error('select date from '+val+' where id=(select min(id) from '+val+')',con)
#print(sql)

#сохраняем дату для отбора
date=con.execute(sql).fetchone()[0]
#print('дату для отбора:',date.fetchone()[0])

#загружаем по дате
sql=sql_error('select * from '+val+' where date="'+str(date)+'"',con)
#print(sql)
df_sort=pd.read_sql(sql,con,index_col='id')

#print(df_sort)

for i in range(len(df_pr)):
    
    sql='select price_go from '+str(df_pr.loc[i,'trade'])+\
         ' where date="'+str(df_sort.loc[1,'date'])+'" and time="'+\
         df_sort.loc[1,'time']+'"'
    #print(sql)
    #print(sql_obr(con.execute(sql)))
    if df_pr.loc[i,'price_go']==con.execute(sql).fetchone():
        df_pr.loc[i,'res']=True
    else: df_pr.loc[i,'res']=False

#df_pr.fillna(0,inplace=True)# убираем пустые значения

#'select time from '+val+' where date="08.05.2019" and time="16:58"'



#sql_2='select * from prog_up where cripta="'+val+'"'

#print(sql_2)
#SELECT max(id),time FROM ltc_rub 



print(df_pr)
print(len(df_pr[df_pr.res==False].count))
