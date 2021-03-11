class Table:

    def __init__(self, tableNo, waiterName, status):
        self.tableNo = tableNo
        self.waiterName = waiterName
        self.status = status

def findWaiterWiseTotalNoOfTables(listOfTables):
    dict = {}
    for table in listOfTables:
        if(table.waiterName in dict.keys()):
            dict[table.waiterName] += 1
        else:
            dict[table.waiterName] = 1
    
    return dict

def findWaiterNameByTableNo(listOfTables, tableNo):
    for table in listOfTables:
        if(table.tableNo == tableNo):
            return table.waiterName
    
    return None

if __name__ == "__main__":
    count = int(input())
    tables = []
    for i in range(count):
        tableNo = int(input())
        waiterName = input()
        status = input()
        tableObj = Table(tableNo, waiterName, status)
        tables.append(tableObj)
    
    inp = int(input())
    ret1 = findWaiterWiseTotalNoOfTables(tables)
    waiterRet = findWaiterNameByTableNo(tables, inp)

    for name in sorted(ret1):
        print(name + "-" + str(ret1[name]))
    
    if(waiterRet == None):
        print("No Table Found")
    else:
        print(waiterRet)