import xlrd
import sqlite3

loc = 'DataSet.xlsx'
db = sqlite3.connect('data.db')

cur = db.cursor()

xl = xlrd.open_workbook(loc)
s = xl.sheet_by_index(0)
print(s)

num = s.nrows
#print(num)
create = "CREATE TABLE IF NOT EXISTS stocks(stockID text PRIMARY KEY, price FLOAT);"
insert = "INSERT INTO stocks(stockID, price) values "

cur.execute(create)
print("\n")
db.commit()
#data =  s.row_values(1)
#print(data[2] + "--- " + data[5])
##stock_id = data[2]
##amt = data[5]

#val = "('"+ stock_id + "' ,"+ str(amt) +");"
#print(val)
for i in range(0, num):
    data = s.row_values(i)
    stock_id = data[2]
    amt = data[5]
    val = "('"+ stock_id + "' ,"+ str(amt) +");"
    print(val)
    q = insert + val
    # print(q)
    try:
        cur.execute(q)
    except:
        print(val)
    # print(data)
db.commit()
