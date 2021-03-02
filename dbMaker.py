import xlrd
import sqlite3
from datetime import datetime, date 


def dateConvert(d):
    sec = (d-25569)*86400
    day = str(datetime.utcfromtimestamp(sec).date())
    #print(day)
    lis = []
    for i in day:
        if(i=='-'):
            lis.append('_')
        else:
            lis.append(i)
    return ''.join(lis)


        

loc = 'table_data/Table2.xlsx'
db = sqlite3.connect('data.db')

cur = db.cursor()

xl = xlrd.open_workbook(loc)
s = xl.sheet_by_index(0)
num = s.nrows

'''
#Table 1
create = "CREATE TABLE IF NOT EXISTS table1(stockID text PRIMARY KEY, quantity int);"
insert = "INSERT INTO table1(stockID, quantity) values "
try:
    cur.execute(create)
except:
    print("dtabase error")
db.commit()

cnt = 0
for i in range(1, num):
    data = s.row_values(i)
    stock_id = data[1]
    quant = 0
    val = "('"+ stock_id + "' ,"+ str(quant) +");"
    #print(val)
    q = insert + val
    try:
        cur.execute(q)
    except:
        print(val)
db.commit()
'''
#Table - 2
create = "CREATE TABLE IF NOT EXISTS table2(Price_Date Date, Price float, stockID text, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
insert = "INSERT INTO table2(Price_Date, Price, stockID) values "

cur.execute(create)
db.commit()
#data = s.row_values(1)

#print(type(data[1]))
#print(data[2] , data[3])


cnt = 0
for i in range(1, num):
    data = s.row_values(i)
    sec = (data[1]-25569)*86400
    priceDate = str(datetime.utcfromtimestamp(sec).date())
    price = data[3]
    stockid = data[2]
#    print(priceDate, price, stockid)
    val = "('"+ priceDate + "',"+ str(price) +",'"+ stockid + "');"
    #print(val)
    cnt += 1
    q = insert + val
    try:
        cur.execute(q)
    except:
        print(val)
db.commit()
print(cnt)

'''
#Table 3
loc2 = 'table_data/table3.xlsx'
xl = xlrd.open_workbook(loc2)
adr = xl.sheet_by_index(0)
rows = adr.nrows
header_row = adr.row_values(0)
col = len(header_row)


create = 'CREATE TABLE IF NOT EXISTS table3(stockID text, '
# Price float, stockID text, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
#ins = 'table3(stockID, '
for i in range(1, col):
    val = dateConvert(header_row[i])
    if i!= col-1:
        #ins += '"'+val + '"'  + ', '
        create += '"'+str(val) + '"'  + ' float, '
    else:
        #ins += '"'+val + '"' + ')'
        create += '"'+str(val) + '"'  + 'float);'
cur.execute(create)
db.commit()


for i in range(1,rows):
    data = adr.row_values(i)
    state = 'INSERT INTO table3 values (' 
    for j in range(0, col):
        if(j!=col-1):
            state+=  '"'+str(data[j])+'"' +', '
        else:
            state += '"'+str(data[j])+'"' + ');'
    try:
        cur.execute(state)
    except:
        print(state)
        break


db.commit()
'''
'''
Table : 