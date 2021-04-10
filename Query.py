import sqlite3
from datetime import datetime
import json
from difflib import get_close_matches
from model import *
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
        dates_desc = cur.execute("select daily_date from daily_sales order by daily_date DESC LIMIT 7;").fetchall()
        dates_list_desc = []
        for i in dates_desc:
            dates_list_desc.append(i[0])
    return dates_list_desc

def getAllTheDates():
    overall_dates = []
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        q = "select daily_date from daily_sales;"
        dates = cur.execute(q).fetchall()
        for i in dates:
            overall_dates.append(i[0])
    return overall_dates

dates = getLast7dates()
print(dates)

def formated_date(d):
    return d.replace("-", "_")

# fucntion to get the live sales
def live_sales():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select * from table6;"
        target = cur.execute(q).fetchall()
        return target


# function to get both highest and lowest sold items in last 7 days
def highOnDemand(flag, limit):
    total_sales_of_stockID = ""
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select * from daily_sales order by rowid desc limit " + str(limit);
        val = cur.execute(q).fetchall()
        sumOfSales = []
        dic = {}
        for i in range(1, 51):
            sum = 0
            for j in range(0, limit):
                sum += val[j][i]
            dic[i] = sum
            sumOfSales.append(sum)
        dict = {}
        items = []
        quantity = []
        if flag:
            sorted_keys = sorted(dic, key = dic.get, reverse = True)
            cnt = 0
            for w in sorted_keys:
                if cnt == limit:
                    break
                cnt += 1    
                items.append(w)
                quantity.append(dic[w])
        else:
            sorted_keys = sorted(dic, key = dic.get, reverse = False)
            cnt = 0
            for w in sorted_keys:
                if cnt == limit:
                    break
                cnt += 1    
                items.append(w)
                quantity.append(dic[w])
    return {"items": items, "quantity": quantity, "limit" : limit}

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


def getSalesCount():
    salesList = []
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
    return {"xaxis": dates, "yaxis": salesList}

# Fixme: Prasad
def highestEarning(flag):
    highDemands = {}
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select * from daily_sales order by rowid desc limit 7";
        val = cur.execute(q).fetchall()
        for i in range(1, 51):
            sum = 0
            item_name = "ITEM_"
            if i < 10:
                item_name += ("0" + str(i))
            else:
                item_name += (str(i))
            for j in range(0, 7):
                sum += (val[j][i] * productDataJson[item_name]['price'])
            highDemands[i] = round(sum, 2)
        items = []
        total = []
        if flag:
            sorted_keys = sorted(highDemands, key = highDemands.get, reverse = True)
            cnt = 0
            for w in sorted_keys:
                if cnt == 7:
                    break
                cnt += 1    
                items.append(w)
                total.append(highDemands[w])
        else:
            sorted_keys = sorted(highDemands, key = highDemands.get, reverse = False)
            cnt = 0
            for w in sorted_keys:
                if cnt == 7:
                    break
                cnt += 1    
                items.append(w)
                total.append(highDemands[w])
    return [items, total]

#Moved
def prepareHomePayload():
    payload = {}
    payload["highOnDemand"] = highOnDemand(dates, True, 7)
    payload["lowOnDemand"] = highOnDemand(dates, False, 7)
    payload["salesData"] = getSalesCount()
    payload["highestEarning"] = highestEarning(True)
    payload["lowestEarning"] = highestEarning(False)
    return payload

def get_all_items():
    stocks_list = []
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select stockID from table3;"
        stocks = cur.execute(q).fetchall()
        for i in stocks:
            stocks_list.append(i[0])
    return stocks_list

def each_item_sold_count():
    sold_count = []
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        stocks = get_all_items()
        for i in stocks:
            q = "select * from table3 where stockID = '"+ i +"';"
            dates = cur.execute(q).fetchall()
            sold_count.append(dates)
    return sold_count


def updateSalesDb(item, quantity):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("insert into table5(:item, :quan);", {"item": item, "quan": quantity})
        con.commit()

def getDistributorInfo(itemID):
    # TODO: Prasad
    pass

def getItemPrediction():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        var = cur.execute("select * from daily_sales order by rowid DESC limit 1;").fetchall()
        #print(var[0])
        #model.main()
        load_main()
        res = weekdata(list(var[0]))
        print(res)
#getItemPrediction()
