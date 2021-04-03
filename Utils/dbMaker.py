import xlrd
import sqlite3
import pandas
import json
from datetime import datetime, date 

productDataPath = "../productData.json"
with open(productDataPath) as f:
    productDataJson = json.load(f)

db = sqlite3.connect('../data.db')
cur = db.cursor()

#stock_price table creation
print(productDataJson)
i = 1
while(i <= 50):
    item_name = "ITEM_"
    if i < 10:
        item_name += ("0" + str(i))
    else:
        item_name += (str(i))
    price = productDataJson[item_name]['price']
    i += 1 
    print(str(item_name) + "===>" + str(price))
    q = "insert into stock_price values('"+ str(item_name) +"', "+ str(price) +");"
    cur.execute(q)
    db.commit()

# table-1
# all_stocks = []
# query_line = ""
# for i in range(1, 51):
#     stock_id = ""
#     if i < 10:
#         stock_id = "ITEM_0" + str(i)
#     else:
#         stock_id = "ITEM_" + str(i)
#     if i != 50:    
#         query_line += stock_id + " int,"
#     else:
#         query_line += stock_id + " int" 
# print(query_line)

# query_string = "daily_date date," + query_line

# print(query_string)
    # all_stocks.append(stock_id)
    # q = "insert into table1 values('"+ stock_id +"', 0);"
    # cur.execute(q)
    # db.commit()

# table - 2
# q = "create table daily_sales(" + query_string + ");"
# cur.execute(q)

# db.commit()
# data = pandas.read_csv('../daily_sales.csv')
# print(data)

# # print(data['date'][0], data['1'][0])
# query = "insert into daily_sales values("
# for i in range(10, 1642):
#     q = query + ""   
#     qq = str(data['date'][i])
#     q += ("'"+ qq +"',")
#     sales = "" 
#     for j in range(1, 51):
#         if j != 50:
#             sales +=  (str(data[str(j)][i]) + ",")
#         else:
#             sales +=  (str(data[str(j)][i]) + ");")
#     out = (q + sales)
#     cur.execute(out)
#     db.commit()
#     print(out)

#table-2 column rename

# q = insert into daily_sales()
# ans = cur.execute("select * from table1 limit 5;").fetchall()
# this is for dates sorting
# val = cur.execute("select invoice_date from table4 order by invoice_date DESC;").fetchall()
# print()
# prediction table
# create = "CREATE TABLE IF NOT EXISTS table7(stockID text, quantity int, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
# cur.execute(create)
# db.commit()

# create = "CREATE TABLE IF NOT EXISTS table7(stockID text, sold int, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
# cur.execute(create)
# db.commit()

# This is for sales portal table creation
# create = "CREATE TABLE IF NOT EXISTS table5(stockID text, sold int, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
# cur.execute(create)
# db.commit()


# sel = "select * from table4 where stockID =" + '" + 90179B + "'+ ";"
# all_items = [cur.execute(sel)]

# def dateConvert(d):
#     sec = (d-25569)*86400
#     day = str(datetime.utcfromtimestamp(sec).date())
#     #print(day)
#     lis = []
#     for i in day:
#         if(i=='-'):
#             lis.append('_')
#         else:
#             lis.append(i)
#     return ''.join(lis)

# loc = 'table_data/datenum.xlsx'
# db = sqlite3.connect('data.db')

# cur = db.cursor()

# xl = xlrd.open_workbook(loc)
# s = xl.sheet_by_index(0)
# num = s.nrows
# create = "CREATE TABLE IF NOT EXISTS table4(invoice_date date);"
# insert = "INSERT INTO table4(invoice_date) values "
# cur.execute(create)
# db.commit()

# for i in range(1, num):
#     data = s.row_values(i)
#     sec = (data[1]-25569)*86400
#     priceDate = str(datetime.utcfromtimestamp(sec).date())
#     val = "('"+ priceDate + "');"
#     q =insert + val
#     print(q)
#     try:
#         cur.execute(q)
#     except:
#         print(val)
# db.commit()





# #Table 1
# create = "CREATE TABLE IF NOT EXISTS table1(stockID text PRIMARY KEY, quantity int);"
# insert = "INSERT INTO table1(stockID, quantity) values "
# try:
#     cur.execute(create)
# except:
#     print("dtabase error")
# db.commit()

# cnt = 0
# for i in range(1, num):
#     data = s.row_values(i)
#     stock_id = data[1]
#     quant = 0
#     val = "('"+ stock_id + "' ,"+ str(quant) +");"
#     #print(val)
#     q = insert + val
#     try:
#         cur.execute(q)
#     except:
#         print(val)
# db.commit()
# #Table - 2
# create = "CREATE TABLE IF NOT EXISTS table2(Price_Date Date, Price float, stockID text, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
# insert = "INSERT INTO table2(Price_Date, Price, stockID) values "

# cur.execute(create)
# db.commit()
# #data = s.row_values(1)

# #print(type(data[1]))
# #print(data[2] , data[3])


# cnt = 0
# for i in range(1, num):
#     data = s.row_values(i)
#     sec = (data[1]-25569)*86400
#     priceDate = str(datetime.utcfromtimestamp(sec).date())
#     price = data[3]
#     stockid = data[2]
# #    print(priceDate, price, stockid)
#     val = "('"+ priceDate + "',"+ str(price) +",'"+ stockid + "');"
#     #print(val)
#     cnt += 1
#     q = insert + val
#     try:
#         cur.execute(q)
#     except:
#         print(val)
# db.commit()
# print(cnt)

# #Table 3
# loc2 = 'table_data/table3.xlsx'
# xl = xlrd.open_workbook(loc2)
# adr = xl.sheet_by_index(0)
# rows = adr.nrows
# header_row = adr.row_values(0)
# col = len(header_row)


# create = 'CREATE TABLE IF NOT EXISTS table3(stockID text, '
# # Price float, stockID text, FOREIGN KEY(stockID) REFERENCES table1(stockID));"
# #ins = 'table3(stockID, '
# for i in range(1, col):
#     val = dateConvert(header_row[i])
#     if i!= col-1:
#         #ins += '"'+val + '"'  + ', '
#         create += '"'+str(val) + '"'  + ' float, '
#     else:
#         #ins += '"'+val + '"' + ')'
#         create += '"'+str(val) + '"'  + 'float);'
# cur.execute(create)
# db.commit()


# for i in range(1,rows):
#     data = adr.row_values(i)
#     state = 'INSERT INTO table3 values (' 
#     for j in range(0, col):
#         if(j!=col-1):
#             state+=  '"'+str(data[j])+'"' +', '
#         else:
#             state += '"'+str(data[j])+'"' + ');'
#     try:
#         cur.execute(state)
#     except:
#         print(state)
#         break


# db.commit()

