import os, sys
from datetime import datetime

def p_bar(i,col,now):
    result=datetime.now()-now
    s='Выполено: '+str(int(round((i/col)*100)))+'%  Время: ['+\
           str(result.seconds)+']'
    return(s)


def sql_null():
    import sqlite3
    class_sp=['ltc_rub','ltc_btc','eth_btc','eth_ltc','eth_rub','btc_rub',
                  'bch_btc','bch_rub','bch_eth','xrp_eth','xrp_rub','xrp_btc',
                  'waves_btc','waves_rub','waves_eth']

    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    for i in range(len(class_sp)):
        
        cursor.execute('SELECT * FROM '+class_sp[i]+' WHERE price_go IS NULL'+\
                   ' OR price_v_go IS NULL OR date IS NULL OR time IS NULL'+\
                   ' OR price IS NULL OR price_v IS NULL')
        print('Таблица '+str(class_sp[i]),cursor.fetchall())
    cursor.close()    # Закрываем объект-курсора
    conn.close()
   
    
def sql_go():

    import sqlite3
    
    
    class_sp=['ltc_rub','ltc_btc','eth_btc','eth_ltc','eth_rub','btc_rub']
    #class_sp=['bch_btc','bch_rub','bch_eth','xrp_eth','xrp_rub','xrp_btc',
    #             'waves_btc','waves_rub','waves_eth']

    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    now=datetime.now()

    for j in range(len(class_sp)):
        
        print(p_bar(j,len(class_sp),now))
    
        for i in range(1,18864):
        
            cursor.execute('SELECT price_v FROM '+class_sp[j]+' WHERE id IN ('+str(i)+','+str(i+1)+')')
            result_v=list(sum(cursor.fetchall(),()))
            result_v=bol_fun(result_v[0]-result_v[1])
        
            cursor.execute('SELECT price FROM '+class_sp[j]+' WHERE id IN ('+str(i)+','+str(i+1)+')')
            result=list(sum(cursor.fetchall(),()))
            result=bol_fun(result[0]-result[1])
                       

            cursor.execute('UPDATE '+class_sp[j]+' SET price_go="'+result+'" WHERE id='+str(i+1))
        
            cursor.execute('UPDATE '+class_sp[j]+' SET price_v_go="'+result_v+'" WHERE id='+str(i+1))
    conn.commit()
    
    cursor.close()    # Закрываем объект-курсора
    conn.close()
    print(p_bar(1,1,now))

def bol_fun(x):      
     if x>0 : res= '-'#+str(x) 
     if x<0 : res= '+'#+str(x)
     if x==0 : res='0'#+str(x)
     #print('return  ',res)
     return (res)
    
def sql_edit():
    
    import sqlite3
    
    class_sp=['ltc_rub','ltc_btc','eth_btc','eth_ltc','eth_rub','btc_rub',
                  'bch_btc','bch_rub','bch_eth','xrp_eth','xrp_rub','xrp_btc',
                  'waves_btc','waves_rub','waves_eth']    

     
            

    conn = sqlite3.connect('base.db')

    
    cursor = conn.cursor()
    print('working')

    
    '''
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
    
    conn.commit()'''
    cursor.close()    # Закрываем объект-курсора
    conn.close()
   




sql_null()

