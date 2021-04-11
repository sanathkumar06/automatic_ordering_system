import sqlite3
from datetime import datetime
import json
from difflib import get_close_matches
from model import *

# Table 1: Current stocks
# Daily sales: All sales data
# Table 6: Prediction
# Table 5: StockID sold
# Stock price: Stock and price
# prediction: stockID, day1, day2, day3, day4, day5, day6, day7

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


# print(getAllTheDates())

dates = getLast7dates()

def formated_date(d):
    return d.replace("-", "_")


# function to get the live sales
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
def highestEarning(flag, limit):
    highDemands = {}
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select * from daily_sales order by rowid desc limit " + str(limit);
        val = cur.execute(q).fetchall()
        for i in range(1, 51):
            sum = 0
            item_name = "ITEM_"
            if i < 10:
                item_name += ("0" + str(i))
            else:
                item_name += (str(i))
            for j in range(0, limit):
                sum += (val[j][i] * productDataJson[item_name]['price'])
            highDemands[i] = round(sum, 2)
        items = []
        total = []
        if flag:
            sorted_keys = sorted(highDemands, key = highDemands.get, reverse = True)
            cnt = 0
            for w in sorted_keys:
                if cnt == limit:
                    break
                cnt += 1
                items.append(w)
                total.append(highDemands[w])
        else:
            sorted_keys = sorted(highDemands, key = highDemands.get, reverse = False)
            cnt = 0
            for w in sorted_keys:
                if cnt == limit:
                    break
                cnt += 1
                items.append(w)
                total.append(highDemands[w])
    return [items, total, limit]

def getCurrentSales(itemID):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur_sales = []
    q = "select sold from table6 where stockID = '" + itemID + "';"
    item_sales = cur.execute(q).fetchall()
    for i in item_sales:
        cur_sales.append(i[0])
    print(cur_sales)


def getCurrentStock(itemID):
    #TODO Prasad
    pass

def get_all_items():
    stocks_list = []
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select stockID from table3;"
        stocks = cur.execute(q).fetchall()
        for i in stocks:
            stocks_list.append(i[0])
    return stocks_list


def get_all_dates():
    dates_list = []
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select invoice_date from table4;"
        dates = cur.execute(q).fetchall()
        for i in dates:
            dates_list.append(i[0])
    return dates_list

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


def getLatestSales():
    # todo prasad
    pass

def addPredictionColumn(count):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        day = "day"+str(count)
        var = cur.execute("alter table prediction add column '"+ str(day) + "' int;")
        con.commit()

def getItemPrediction(limit, count):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        var = cur.execute("select * from daily_sales order by rowid DESC limit 1;").fetchall()
        #print(var[0])
        #model.main()
        load_main()
        res = weekdata(list(var[0]), limit)
        #print(res[0])
        for i in range(50):
            itemNO = 'ITEM_'
            if(i<10):
                itemNO += '0'
            itemNO += str(i+1)
            for j in range(count,count+3):
                day = 'day'+str(j+1)
                val = int(res[i][j])                
                cur.execute("update prediction set '" + str(day) +"' = '" + str(val)+"' where stockID = '" + itemNO +"';")
                con.commit()

#getItemPrediction()

def intermediatePrediction(date, itemID, limit):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        var = cur.execute("select * from table5;").fetchall()
        print(var)
        lis = [date]
        for i in var:
            lis.append(i)
        res = weekdata(lis,limit)
        itmNo = itemID[:-2]
        lis = []
        for i in res[int(itmNo)-1]:
            lis.append(int(i))

        val1 = int(lis[0])  
        val2 = int(lis[1])          
        cur.execute("update prediction set day6 = '" + str(val1)+"' , day7 = '" + str(val2)+"' where stockID = '" + itemNO +"';")
        con.commit()
        return sum(lis)