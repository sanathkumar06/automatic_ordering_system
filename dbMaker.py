import xlrd
import sqlite3
from datetime import datetime, date 


def dateConvert(d):
    sec = (d-25569)*86400
    return str(datetime.utcfromtimestamp(sec).date())

        

loc = 'table_data/Table2.xlsx'
db = sqlite3.connect('data.db')

cur = db.cursor()

xl = xlrd.open_workbook(loc)
s = xl.sheet_by_index(0)
num = s.nrows

'''
Table 1
create = "CREATE TABLE IF NOT EXISTS table1(stockID text PRIMARY KEY, quantity int);"
insert = "INSERT INTO table1(stockID, quantity) values "

cur.execute(create)
db.commit()

cnt = 0
for i in range(0, num):
    data = s.row_values(i)
    stock_id = data[1]
    quant = 0
    val = "('"+ stock_id + "' ,"+ str(quant) +");"
    print(val)
    q = insert + val
    try:
        cur.execute(q)
    except:
        print(val)
db.commit()

Table - 2
create = "CREATE TABLE IF NOT EXISTS table2(Price_Date Date, Price float, stockID text, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
insert = "INSERT INTO table2(Price_Date, Price, stockID) values "

cur.execute(create)
db.commit()
#data = s.row_values(1)

#print(type(data[1]))
#print(data[2] , data[3])
cnt = 0
for i in range(20, num):
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
loc2 = 'table_data/stockID.xlsx'
xl = xlrd.open_workbook(loc2)
adr = xl.sheet_by_index(0)
rows = adr.nrows

create = "CREATE TABLE IF NOT EXISTS table3(Sale_Date Date, "
# Price float, stockID text, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
col = ""
ins = "table3(Sale_Date, "
for i in range(1, rows):
    row_num = adr.row_values(i)
    val = str(row_num[1])
    if i != rows - 1:
        #ins += (val + ", ")
        create += (val + " text, ") 
    else:
        #ins += (val + ")")
        create += (val + " text);")

print(create)
cur.execute(create)
db.commit()
#sprint(create + "\n")
#print(ins + "\n")

loc1 = 'table_data/Table3.xlsx'
xls = xlrd.open_workbook(loc1)
addr = xls.sheet_by_index(0)
rowws = addr.nrows

state = ""

for i in range(1, rowws):
    state += "INSERT INTO " + ins + " values " + "("
    for j in range(0, rows):
        if(j==0):
            state+=str(dateConvert(addr.row_values(i)[j])) +", "
        else:
            state += (str(addr.row_values(i)[j]))
            if(j<rows - 1):
                state+= ", "
    state+=");\n"
    try:
        cur.execute(state)
    except:
        print(state)
   # print(state)

db.commit()

cur.execute(create)
db.commit()
#data = s.row_values(1)


