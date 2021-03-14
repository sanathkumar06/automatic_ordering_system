import sqlite3
from datetime import datetime
import json
from difflib import get_close_matches

productDataPath = "C:\\Users\\vamshi\\Desktop\\automatic_ordering_system\\productData.json"
with open(productDataPath) as f:
    productDataJson = json.load(f)

nameIDMapJsonPath = "C:\\Users\\vamshi\\Desktop\\automatic_ordering_system\\nameIDMap.json"
with open(nameIDMapJsonPath) as f:
    nameIDMapJson = json.load(f)

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
def highOnDemand(dates_list, flag, limit):
    total_sales_of_stockID = ""
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        for i in range(0, len(dates_list)):
            if(i != (len(dates_list) - 1)):
                d = dates_list[i].replace("-", "_")
                total_sales_of_stockID += (' "' + d + '"+')
            else:
                total_sales_of_stockID += (' "' + d + '"')

        if(flag): 
            q = "select stockID from( select stockID,(" + total_sales_of_stockID + ") as total from table3) order by total desc limit " +  str(limit) +";"
        else:
            q = "select stockID from( select stockID,(" + total_sales_of_stockID + ") as total from table3) order by total asc limit " +  str(limit) +";"
        
        sales = cur.execute(q).fetchall()
        sales_list = []
        for i in sales:
            t = str(i).replace("('","").replace("',)","").replace("(","").replace(")","")
            sales_list.append(t)
        #print(sales) -> will give the list of tuples which contains the (stockID, total) 
        return sales_list


def getLast7dates():
    with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            #getting last 7 dates from table for which only contain dates
            dates_desc = cur.execute("select invoice_date from table4 order by invoice_date DESC LIMIT 7;").fetchall()
            dates_list_desc = []
            
            for i in dates_desc:
                t = str(i).replace("('","").replace("',)","")
                dates_list_desc.append(t)
    
    return dates_list_desc


def lookForItem(item):
    try:
        productDataJson[item]
        return item
    except:
        try:
            id = nameIDMapJson[item]
            return id
        except:
            return "null"

def getSimilar(item):
    items = get_close_matches(item, nameIDMapJson.keys(), n=10, cutoff=0.3)
    IDs = []
    for item in items:
        IDs.append(nameIDMapJson[item])
    
    IDandName = {"ID": IDs, "names":items}
    
    #changes
    itemId = IDandName.get("ID")
    itemName = IDandName.get("names")


    print(IDandName)
    return IDandName