import pandas as pd
#import sqlite3
from sqlalchemy import create_engine

val='btc_rub'

con=create_engine('sqlite:///base.db') #Путь к базе

#загружаем прогноз
sql_pr='select * from prog_up where cripta="'+val+'"'
df_pr=pd.read_sql(sql_pr,con)
df_pr=df_pr[df_pr['pr']>59].sort_values(
            by='pr',ascending=False).reset_index(drop=True)
df_pr['res']=None

#выбираем первую запись
sql='select date from '+val+' where id=(select min(id) from '+val+')'

#сохраняем дату для отбора
date=con.execute(sql).fetchone()[0]

#загружаем по дате
df_sort=pd.read_sql('select * from '+val+' where date="'+date+'"',con,index_col='id')



for i in range(len(df_pr)):
    
    sql='select price_go from '+str(df_pr.loc[i,'trade'])+\
         ' where date="'+str(df_sort.loc[1,'date'])+'" and time="'+\
         df_sort.loc[1,'time']+'"'
    print(sql)
    print(con.execute(sql).fetchone()[0])
    df_pr.loc[i,'res']=con.execute(sql).fetchone()[0]

#'select time from '+val+' where date="08.05.2019" and time="16:58"'

df=pd.read_sql(sql,con)

sql_2='select * from prog_up where cripta="'+val+'"'

#print(sql_2)
#SELECT max(id),time FROM ltc_rub 



print(df_pr)
print(df_sort)
