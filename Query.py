import sqlite3
from datetime import datetime
import json
from difflib import get_close_matches

productDataPath = "productData.json"
with open(productDataPath) as f:
    productDataJson = json.load(f)

nameIDMapJsonPath = "nameIDMap.json"
with open(nameIDMapJsonPath) as f:
    nameIDMapJson = json.load(f)


def getLast7dates():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        # getting last 7 dates from table for which only contain dates
        dates_desc = cur.execute("select invoice_date from table4 order by invoice_date DESC LIMIT 7;").fetchall()
        dates_list_desc = []

        for i in dates_desc:
            dates_list_desc.append(i[0])

    return dates_list_desc

def getAllTheDates():
    overall_dates = []
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        q = "select * from table4;"
        dates = cur.execute(q).fetchall()
        for i in dates:
            overall_dates.append(i[0])
    return overall_dates

# print(getAllTheDates())

dates = getLast7dates()

# default parameter error in this function
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
def formated_date(d):
    return d.replace("-", "_")

# function to get both highest and lowest sold items in last 7 days
def highOnDemand(dates_list, flag, limit):
    total_sales_of_stockID = ""
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        for i in range(0, len(dates_list)):
            if (i != (len(dates_list) - 1)):
                d = formated_date(dates_list[i])
                total_sales_of_stockID += (' "' + d + '"+')
            else:
                total_sales_of_stockID += (' "' + d + '"')

        if (flag):
            q = "select stockID, total from( select stockID,(" + total_sales_of_stockID + ") as total from table3) order by total desc limit " + str(
                limit) + ";"
        else:
            q = "select stockID, total from( select stockID,(" + total_sales_of_stockID + ") as total from table3) order by total asc limit " + str(
                limit) + ";"

        sales = cur.execute(q).fetchall()
        items = []
        quantity = []
        for i in sales:
            #print(i[0], i[1])
            items.append(productDataJson[i[0]]["name"])
            quantity.append(i[1])

        return {"items": items, "quantity": quantity}

        # sales_list = []
        # for i in sales:
        #     t = str(i).replace("('","").replace("',)","").replace("(","").replace(")","")
        #     sales_list.append(t)
        # return sales_list


def getItemInfo(itemId):
    return productDataJson[itemId]


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


# Return format example:
    # getSimilar("biscuit"):
    # {'ID': ['D', '21218', '22357'], 'names': ['Discount', 'Red spotty biscuit tin', 'Kings choice biscuit tin']}
def getSimilar(item):
    items = get_close_matches(item, nameIDMapJson.keys(), n=10, cutoff=0.4)
    IDs = []
    for item in items:
        IDs.append(nameIDMapJson[item])

    IDandName = {"ID": IDs, "names": items}
    return IDandName


#Expected return format:
    # {'xaxis': ['2011-12-09', '2011-12-08', '2011-12-07', '2011-12-06', '2011-12-05', '2011-12-04', '2011-12-02'], 'yaxis': ['123', '133', '345', '355', '654', '789','5567']}
def getSalesCount():
    salesList = []
    # TODO: Total sales for last 7 days
    # append to salesList
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        for i in range(0, len(dates)):
            d = formated_date(dates[i])
            query_date = '"' + d + '"'  
            q = "select "+ query_date +" from table3 where " +  query_date  + " = " +  query_date  + " ;"
            sales_count = cur.execute(q).fetchall()
            tot = 0
            for j in sales_count:
                tot += (j[0]);
            salesList.append(tot)
    # return salesList
    return {"xaxis": dates, "yaxis": salesList}

def highestEarning(flag):
    highDemands = []
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        for i in range(0, len(dates)):
            d = formated_date(dates[i])
            query_date = '"' + d + '"'
            if flag:
                # innerjoin to get highest earing for last 7 days
                q = "select a.stockID, max(a.Price * b."+ str(query_date) +") as highEarning from table2 a, table3 b where a.stockID == b.stockID order by highEarning;"
                highEarning = cur.execute(q).fetchone()
            else:
                q = "select a.stockID, min(a.Price * b."+ str(query_date) +") as highEarning from table2 a, table3 b where a.stockID == b.stockID order by highEarning;"
                highEarning = cur.execute(q).fetchone()
            for j in highEarning:
                highDemands.append(j)
        # highDemands.sort()
    return highDemands
            

def prepareHomePayload():
    payload = {}
    payload["highOnDemand"] = highOnDemand(dates, True, 10)
    payload["lowOnDemand"] = highOnDemand(dates, False, 10)
    payload["salesData"] = getSalesCount()
    # TODO: data for highest earning and lowest earning
    payload["highestEarning"] = highestEarning(True)
    payload["lowestEarning"] = highestEarning(False)
    # Add as dictioanry item
    return payload


#Expected return format:
    #prepareItemDataPayload("22142")
    #{'ID': '22142', 'name': 'Christmas craft white fairy ', 'price': 1.45, 'dates': ['2011-12-09', '2011-12-08', '2011-12-07',... All dates], 'sales': [['123', '133', '345',....]}
def prepareItemDataPayload(itemId):
    itemInfo = getItemInfo(itemId)
    payload = {}
    payload["ID"] = itemId
    payload["name"] = itemInfo["name"]
    payload["price"] = itemInfo["price"]
    #payload["dates"] = TODO: All dates of sales as array
    # payload["sales"] = TODO: Daily sales data as array
    # payload["prediction"] = TODO:Predicted sales for the item

    return payload

# print(getLast7dates())
# print(getSalesCount())
# print(highestEarning(True))
# print(getSimilar("pizza"))