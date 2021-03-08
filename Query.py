import sqlite3
from datetime import datetime

#default parameter error in this function
'''
def query(f , t = datetime.now().strftime("%Y-%m-%d"), stockID):
    #formatedDates = []
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        dates = cur.execute("select invoice_date from table4 where invoice_date between :fr and :to;", {"fr" : f, "to" : t}).fetchall()
        sales = []
        for i in range(0, len(dates)):
            s = str(dates[i])
            #print(s[2:12])
            requiredDate = s[2:12]
            requiredDate = requiredDate.replace('-', '_')
            requiredDate = '"' + requiredDate + '"'
            #q = "select "+ requiredDate +" from table3 where stockID = :id;"
            #print(q)
            sale = cur.execute("select "+ requiredDate +" from table3 where stockID = :id;",{ "id" : stockID}).fetchone()
            sales.append(sale);
            #print(sales)  
            #formatedDates.append(requiredDate)
        print(sales)
        final_sales = []
        for i in range(0, len(sales)):
            j = str(sales[i])
            final_sales.append(float(j[1:-2]))    
    return final_sales
#print(query("2010-12-01", "2010-12-02", "10002"))
'''
#function to get both highest and lowest sold items in last 7 days
def highOnDemand(dates_list, conn, cur):
    total_sales_of_stockID = ""
    for i in range(0, len(dates_list)):
        if(i != (len(dates_list) - 1)):
            total_sales_of_stockID += (" " + dates_list[i] + " + ")
        else:
            total_sales_of_stockID += (" " + dates_list[i])
    #print(total_sales_of_stockID) -> it give the string which represents the sum of all days in the date_list
    q = "select stockID from( select stockID,(" + total_sales_of_stockID + ") as total from table3) order by total desc limit 7;"
    #print(q) -> query string
    sales = cur.execute(q).fetchall()
    sales_list = []
    for i in sales:
        t = str(i).replace("('","").replace("',)","").replace("(","").replace(")","")
        sales_list.append(t)
    #print(sales) -> will give the list of tuples which contains the (stockID, total) 
    #print(sales_list)
    return sales_list

#print(highOnDemand(['"2011_11_22"', '"2011_11_23"']))
#print(highOnDemand(['"2011_11_23"', '"2011_11_22"']))