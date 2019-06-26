from sklearn import tree
import pandas as pd
from sqlalchemy import create_engine, exc

#import matplotlib.pyplot as plt
con=create_engine('sqlite:///base.db') #Путь к базе

table_list=('ltc_rub','ltc_btc','eth_btc','eth_ltc','eth_rub','btc_rub',
                  'bch_btc','bch_rub','bch_eth','xrp_eth','xrp_rub','xrp_btc',
                  'waves_btc','waves_rub','waves_eth')
val='btc_rub'

#загружаем прогноз
sql_pr='select * from prog_up where cripta="'+val+'" and pr>55'
df_pr=pd.read_sql(sql_pr,con)
print(df_pr.sort_values(
            by='pr',ascending=False).reset_index(drop=True))


df_pr['price_go']=1

#набор характеристик, по которым будем классифицировать
#train=[[18,0.6,'40'],[18,0.6,'41'],[17,0.5,'40'],[94,600,'38'],[96,500,'39']]
train=df_pr[['trade','price_go']].values.tolist()

#print(train2)
print(train)

result=[]
#Определим результат, который будет давать каждый набор значений.
for i in range(len(df_pr)):
    
    result.append('yes')
print(result)    

#определяем классификатор, который будет основываться на схеме принятия решения
classif=tree.DecisionTreeClassifier()

#classif=tree.DecisionTreeRegressor()

#Передаем наши данные классификатору.
classif.fit(train, result)

#пробуем определить
print (classif.predict([[18,0.5,'40']]))

