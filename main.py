from src.classes.SoSHashTable import SoSHashTable

sosHashTable = SoSHashTable(10)

sosHashTable.get(5)

sosHashTable.insert(1, {'key': 1})
sosHashTable.insert(2, {'key': 2})
sosHashTable.insert(3, {'key': 3})
sosHashTable.insert(4, {'key': 4})
sosHashTable.insert(5, {'key': 5})
sosHashTable.insert(6, {'key': 6})
sosHashTable.insert(7, {'key': 7})
sosHashTable.insert(8, {'key': 8})
sosHashTable.insert(9, {'key': 9})
sosHashTable.insert(10, {'key': 10})
sosHashTable.insert(11, {'key': 11})

for x in sosHashTable.table:
    print(x[1])

for i in range(1, 11):
    print(sosHashTable.get(i))

print('tuple test')

my_tuple = ('first', {'test': 'problem'})

print(my_tuple[1])

my_tuple[1]['test'] = 'changed'

print(my_tuple[1])
