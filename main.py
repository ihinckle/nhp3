from src.classes.SoSHashTable import SoSHashTable

sosHashTable = SoSHashTable(10)

sosHashTable.insert(1, {'key': 1})
sosHashTable.insert(2, {'key': 2})
sosHashTable.insert(3, {'key': 1})
sosHashTable.insert(4, {'key': 1})
sosHashTable.insert(5, {'key': 1})
sosHashTable.insert(6, {'key': 1})
sosHashTable.insert(7, {'key': 1})
sosHashTable.insert(8, {'key': 1})
sosHashTable.insert(9, {'key': 1})
sosHashTable.insert(10, {'key': 1})
sosHashTable.insert(11, {'key': 1})

for x in sosHashTable.table:
    print(x['key'])
