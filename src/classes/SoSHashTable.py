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
        bucket_index = self.__get_bucket_index(key)
        while self.table[bucket_index][0] != -1:
            self.__get_next_bucket_index(bucket_index)
        self.table[bucket_index] = (key, item)
        self.__contains += 1
        return True

    def get(self, key):
        if self.__contains == 0:
            print('Table is empty')
            return False
        bucket_index = self.__get_bucket_index(key)
        while self.table[bucket_index][0] != key:
            self.__get_next_bucket_index(bucket_index)
        return self.table[bucket_index][1]

    def __get_bucket_index(self, key):
        return hash(key) % self.__capacity

    def __get_next_bucket_index(self, bucket_index):
        if bucket_index == self.__capacity - 1:
            bucket_index = 0
        else:
            bucket_index += 1
        return bucket_index
