import sqlite3
from datetime import datetime
import json
from difflib import get_close_matches
from model import *
import json

# Table 1: Current stocks
# Daily sales: All sales data
# Table 6: Prediction
# Table 5: StockID sold
# Stock price: Stock and price
# prediction: stockID, day1, day2, day3, day4, day5, day6, day7

productDataPath = "Resources/productData.json"
pathToPlacedOrder = "Resources/placedOrders.json"
pathToCache = "Resources/tempCache.json"

with open(productDataPath) as f:
    productDataJson = json.load(f)

nameIDMapJsonPath = "Resources/nameIDMap.json"
with open(nameIDMapJsonPath) as f:
    nameIDMapJson = json.load(f)


#function to get last 30 dates
def getLast30Days():
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        q = "select daily_date from daily_sales order by rowid desc limit 30;"
        dates = cur.execute(q).fetchall()
        return dates


# print(getLast30Days())

#fuction to make query line which has aggregate function sum(each individual item) 
def getQueryLine():
    i = 1
    query_line = ""
    while(i <= 50):
        item_name = "ITEM_"
        if i < 10:
            item_name += ("0" + str(i))
            query_line += (" sum("+ item_name +") +")
        else:
            item_name += (str(i))
            if(i < 50):
                query_line += (" sum("+ item_name +") +")
            else:
                query_line += (" sum(" + item_name + ")")
        i += 1
    return query_line

#funtion to calculate the total quantity sold from the daily_sales table
def getItemSoldAllTime():
    query_line = getQueryLine()
    # print(query_line)
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        q = "select " + query_line + "from daily_sales;"
        total = cur.execute(q).fetchone()
        return total[0]

# funtion to calculate the total quantity sold in last 30 days from the daily_sales table
def getItemSoldPerMonth():
    query_line = getQueryLine()
    dates = getLast30Days()
    item_sold = []
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        for i in dates:
            q = "select " + query_line + " from daily_sales where daily_date = '"+ str(i[0]) +"' ;"
            tot = cur.execute(q).fetchone()
            item_sold.append(tot)
    final_total = 0
    for j in item_sold:
        final_total += j[0]
    return final_total

# function to return recent 7 dates from the daily_sales table
def getLast7dates():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        # getting last 7 dates from table for which only contain dates
        dates_desc = cur.execute("select daily_date from daily_sales order by rowid DESC LIMIT 7;").fetchall()
        dates_list_desc = []
        for i in dates_desc:
            dates_list_desc.append(i[0])
    return dates_list_desc

# function to calculate the total quantity sold in last 7 days from the daily_sales table
def getItemSoldPerWeek():
    query_line = getQueryLine()
    dates = getLast7dates()
    item_sold = []
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        for i in dates:
            q = "select " + query_line + " from daily_sales where daily_date = '"+ str(i) +"' ;"
            tot = cur.execute(q).fetchone()
            item_sold.append(tot)
    final_total = 0
    for j in item_sold:
        final_total += j[0]
    return final_total

# function to return all the dates available from the daily_sales table
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

# 
# def formated_date(d):
#     return d.replace("-", "_")

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
            sorted_keys = sorted(dic, key=dic.get, reverse=True)
            cnt = 0
            for w in sorted_keys:
                if cnt == limit:
                    break
                cnt += 1
                items.append(w)
                quantity.append(dic[w])
        else:
            sorted_keys = sorted(dic, key=dic.get, reverse=False)
            cnt = 0
            for w in sorted_keys:
                if cnt == limit:
                    break
                cnt += 1
                items.append(w)
                quantity.append(dic[w])
    return {"items": items, "quantity": quantity, "limit": limit}

# function to get the item information
def getItemInfo(itemId):
    return productDataJson[itemId]

# function to search an item
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

# function to return the similar names for the item searched for
def getSimilar(item):
    items = get_close_matches(item, nameIDMapJson.keys(), n=10, cutoff=0.4)
    IDs = []
    for item in items:
        IDs.append(nameIDMapJson[item])

    IDandName = {"ID": IDs, "names": items}
    return IDandName

# Return the sales of each ITEMID for last 4 days
def getSalesCount():
    query_line = getQueryLine()
    dates = getLast7dates()
    # print(dates)
    dates = dates[:4]
    item_sold = []
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        for i in dates:
            q = "select " + query_line + " from daily_sales where daily_date = '"+ str(i) +"' ;"
            tot = cur.execute(q).fetchone()
            item_sold.append(tot[0])
    item_sold = item_sold[::-1]
    return item_sold

# Return the current quantity for ITEMID
def getCurrentStocksCount(itemID):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cnt = cur.execute("select quantity from table1 where stockID = '"+ itemID +"';").fetchone()
        return cnt[0]
    
#function to calculate total amount gained from that stock in which total amount gained is highest
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
            sorted_keys = sorted(highDemands, key=highDemands.get, reverse=True)
            cnt = 0
            for w in sorted_keys:
                if cnt == limit:
                    break
                cnt += 1
                items.append(w)
                total.append(highDemands[w])
        else:
            sorted_keys = sorted(highDemands, key=highDemands.get, reverse=False)
            cnt = 0
            for w in sorted_keys:
                if cnt == limit:
                    break
                cnt += 1
                items.append(w)
                total.append(highDemands[w])
    return [items, total, limit]

# Return current sales from Table 5 for an itemID
def getCurrentSales(itemID):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur_sales = []
    q = "select sold from table5 where stockID = '" + itemID + "';"
    item_sales = cur.execute(q).fetchall()
    #for i in item_sales:
    #   cur_sales.append(i[0])
    return int(item_sales[0][0])


# Return current stock from Table 1 for an itemID
def getCurrentStock(itemID):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        var1 = cur.execute("select quantity from table1 where stockID = '" + str(itemID) + "';").fetchall()
        curr = var1[0][0]
        return int(curr)


# Return all itemID
def get_all_items():
    stocks_list = []
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select stockID from table3;"
        stocks = cur.execute(q).fetchall()
        for i in stocks:
            stocks_list.append(i[0])
    return stocks_list

# function to retreive all dates
def get_all_dates():
    dates_list = []
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select invoice_date from table4;"
        dates = cur.execute(q).fetchall()
        for i in dates:
            dates_list.append(i[0])
    return dates_list

#function return items sold for limited dates
def eachItemSoldCount(limit, id):
    # sold_count = []
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select daily_date, "+ id + " from daily_sales order by rowid limit "+ str(limit) + ";"
        sold_count = cur.execute(q).fetchall()
    return sold_count

# print(eachItemSoldCount(90, "ITEM_01"))

# function to update the sold table 
def updateSalesDb(item, quantity):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        currentStock = cur.execute("select sold from table5 where stockID='{0}';".format(item)).fetchall()
        quantity = int(quantity) + int(currentStock[0][0])
        q = "update table5 set sold = {0} where stockID='{1}'".format(str(quantity), item)
        cur.execute(q)
        con.commit()

# function to add new date column to Prediction table
def addPredictionColumn(count):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        day = "day" + str(count + 2)
        var = cur.execute("alter table prediction add column '" + str(day) + "' int;")
        con.commit()

# function to load the model and predict
def getItemPrediction1():
    with open(pathToCache) as f:
        c = json.load(f)
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        var = cur.execute("select * from daily_sales order by rowid DESC limit 1;").fetchall()
        # print(var[0])
        # model.main()
        load_main()
        res = weekdata(list(var[0]), 3)
        #print(res[0])
        count = c["count"]
        addPredictionColumn(count)

        for i in range(50):
            itemNO = 'ITEM_'
            if(i<9):
                itemNO += '0'
            itemNO += str(i+1)
            for j in range(3):
                day = 'day'+str(count)
                val = int(res[i][j])                
                cur.execute("update prediction set '" + str(day) +"' = '" + str(val)+"' where stockID = '" + itemNO +"';")
                con.commit()
                count+=1
            count-=3

# function to update Table daily_sales
def updateDailySalesToDB():
    with open(pathToCache) as f:
        c = json.load(f)
    date = c["dbDate"]
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        var = cur.execute("select * from table5;").fetchall()
        up = "insert into daily_sales(daily_date) values ('"+ str(date)+"');"
        cur.execute(up)
        con.commit()
        for i in range(len(var)):
            q = "update daily_sales set '"+str(var[i][0]+"' = " +str(var[i][1])+ " where daily_date='"+str(date)+"';")
            # print(q)
            cur.execute(q)
            con.commit()

# function to predict sales for an itemID
def getItemPrediction(itemID):
    with open(pathToCache) as f:
        c = json.load(f)
    date = c["date"]
    count = c["count"]
    dbDate = c["dbDate"]
    currDate = datetime.date.today()
    currDate = currDate.strftime("%d/%m/%Y")
    if(currDate>date):
        dateval = datetime.datetime.strptime(str(dbDate),'%d-%m-%Y').date()
        #print(dateval)
        dateval+=datetime.timedelta(days=1)
        #print(dateval)
        dateval = str(dateval)
        dateval = dateval.split('-')
        dateval = dateval[::-1]
        dateval =  '-'.join(dateval)
        count+=1

        c = {"count":count, "date":currDate, "dbDate":dateval}
        with open(pathToCache, 'w') as outfile:
            json.dump(c, outfile)
        updateDailySalesToDB()
        resetTable5()
        getItemPrediction1()
    
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        #count = c["count"]
        day = "day"+str(count)
        q = "select "+day+" from prediction where stockID =  '" + str(itemID)+ "';"
        #print(q)
        var = cur.execute(q).fetchall()
        return(int(var[0][0]))
#getItemPrediction("ITEM_02")

#function returns items placed for an orders 
def getPlacedOrder():
    with open(pathToPlacedOrder) as f:
        data = json.load(f)
    return data

# function to reset Table 5 after the end of the day
def resetTable5(itemID):
    itemID = itemID[-2:]
    itemID = int(itemID)
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        for i in range(50):
            itemNO = 'ITEM_'
            if(i<9):
                itemNO += '0'
            itemNO += str(i+1)
            q = "update table5 set sold = 0 where stockID = '"+itemNO+"';"
            cur.execute(q)
            con.commit()


# Return the sales prediction and date for the graph
def getItemPredictionFromDB(itemID):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select day1, day2, day3, day4, day5, day6, day7 from prediction where stockID =   '" +str(itemID)+"' ;"
        var = cur.execute(q).fetchall()
        lis = []
        for i in var[0]:
            lis.append(i)
        res = getLast7dates()
        res = res[:4]
        res = res[::-1]
        for i in range(3):
            if i == 0:
                dateval = res[-1]
            # print(dateval)
            dateval = datetime.datetime.strptime(str(dateval), '%d-%m-%Y').date()
            # print(dateval)
            dateval += datetime.timedelta(days=1)
            # print(dateval)
            dateval = str(dateval)
            dateval = dateval.split('-')
            dateval = dateval[::-1]
            dateval = '-'.join(dateval)
            res.append(dateval)
        return {"xaxis": res, "yaxis": lis}

# function to repredict for any particular itemID
def intermediatePrediction(itemID, limit):
    with open(pathToCache) as f:
        c = json.load(f)
    date = c["dbDate"]
    date = date.replace('/','-')
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        var = cur.execute("select * from table5;").fetchall()
        # print(var)
        lis = [date]
        for i in var:
            lis.append(i[1])
        load_main()
        res = weekdata(lis,limit)
        #print(itemID)
        itmNo = itemID[-2:]
        #print(itmNo)
        count = c["count"]
        lis = []
        for i in res[int(itmNo)-1]:
            lis.append(int(i))
        day1 = 'day'+str(count+1)
        day2 = 'day'+str(count+2)
        val1 = int(lis[0])
        val2 = int(lis[1])
        cur.execute("update prediction set '" + str(day1) +"' = '" + str(val1)+"' , '" + str(day2) +"' = '" + str(val2)+"' where stockID = '" + str(itemID) +"';")
        con.commit()
        var1 = cur.execute("select quantity from table1 where stockID = '" + str(itemID) +"';").fetchall()
        curr = var1[0][0]
        return sum(lis)

#function to return 7 days prediction for graph
def getPredictedSales():
    with open(pathToCache) as f:
        c = json.load(f)
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        count = c["count"]
        day = "day" + str(int(count) - 4) + ", day" + str(int(count) - 3) + ", day" + str(
            int(count) - 2) + ", day" + str(int(count) - 1) + ", day" + str(int(count)) + ", day" + str(
            int(count) + 1) + ", day" + str(int(count) + 2)
        q = "select " + day + " from prediction;"
        # print(q)
        var = cur.execute(q).fetchall()
        # print(len(var))
        # print(len(var[0]))
        lis = []
        for i in range(7):
            ch = 0
            for j in range(50):
                ch += var[j][i]
            lis.append(ch)
        res = getLast7dates()
        res = res[:4]
        res = res[::-1]
        for i in range(3):
            if i == 0:
                dateval = res[-1]
            #print(dateval)
            dateval = dateval.replace('/','-')
            dateval = datetime.datetime.strptime(str(dateval),'%d-%m-%Y').date()
            #print(dateval)
            dateval+=datetime.timedelta(days=1)
            #print(dateval)
            dateval = str(dateval)
            dateval = dateval.split('-')
            dateval = dateval[::-1]
            dateval = '-'.join(dateval)
            res.append(dateval)
        return {"xaxis": res, "yaxis": lis}

# function to structure the prediction table initially
def initialPrediction():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        var = cur.execute("select * from daily_sales order by rowid DESC limit 7;").fetchall()
        var = list(var)
        var = var[::-1]
        load_main()
        for i in range(0,7):
            res = weekdata(var[i], 1)
            print(res)
            print(res[0])
            day = 'day'+str(i+1)
            for j in range(50):
                itemNO = 'ITEM_'
                if(j<9):
                    itemNO += '0'
                itemNO += str(j+1)
                val = int(res[j])
                cur.execute("update prediction set '" + str(day) +"' = '" + str(val)+"' where stockID = '" + itemNO +"';")
                con.commit()

# function to set the stocks in table 1 initially
def initialStocks():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select day5, day6, day7 from prediction;"
        var = cur.execute(q).fetchall()
        print(var[0])
        print(len(var))
        print(len(var[0]))
        lis = []
        for i in range(len(var)):
            s = 0
            for j in var[i]:
                s += int(j)
            itemNO = 'ITEM_'
            if(i<9):
                itemNO += '0'
            itemNO += str(i+1)
            cur.execute("update table1 set quantity = " + str(s) +" where stockID = '" + itemNO +"';")
            con.commit()
        print(cur.execute("select * from table1").fetchall())

#initialStocks()

# function to update the stocks in table1 after a sale
def updateCurrentStocks(item, quantity):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        q = "select quantity from table1 where stockID = '"+item+"';"
        var = cur.execute(q).fetchall()
        quan = int(var[0][0]) - int(quantity)
        q = "update table1 set quantity = {0} where stockID='{1}'".format(str(quan), item)
        cur.execute(q)
        con.commit()