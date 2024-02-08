class SoSHashTable:
    __initial_value = (-1, 'start')

    def __init__(self, capacity):
        self.__capacity = capacity
        self.__contains = 0
        self.table = [self.__initial_value] * self.__capacity

    def insert(self, key, item):
        if not (self.__contains < self.__capacity):
            print('Table is full')
            return False
        bucket_index = hash(key) % self.__capacity
        while self.table[bucket_index][0] != -1:
            if bucket_index == self.__capacity-1:
                bucket_index = 0
            else:
                bucket_index += 1
        self.table[bucket_index] = (key, item)
        self.__contains += 1
        return True

    # def retrieve(self, key):
    #     if self.__contains == 0:
    #         print('Table is empty')
    #         return False
    #     bucket_index = hash(key) % self.__capacity
    #     while self.table[bucket_index]
