class SoSHashTable:
    _initial_value = (-1, 'start')

    def __init__(self, capacity):
        self._capacity = capacity
        self._contains = 0
        self.table = [self._initial_value] * self._capacity
        self._i = -1

    def insert(self, key, item):
        if not (self._contains < self._capacity):
            print('Table is full')
            return False
        bucket_index = self._get_bucket_index(key)
        while self.table[bucket_index][0] != -1:
            bucket_index = self._get_next_bucket_index(bucket_index)
        self.table[bucket_index] = (key, item)
        self._contains += 1
        return True

    def get(self, key):
        bucket_index = self._get_bucket_index(key)
        while self.table[bucket_index][0] != key:
            bucket_index = self._get_next_bucket_index(bucket_index)
        return self.table[bucket_index][1]

    def get_capacity(self):
        return self._capacity

    def _get_bucket_index(self, key):
        return int.from_bytes(key.encode()) % self._capacity

    def _get_next_bucket_index(self, bucket_index):
        if bucket_index == self._capacity - 1:
            bucket_index = 0
        else:
            bucket_index += 1
        return bucket_index

    def __iter__(self):
        return self

    def __next__(self):
        if self._i < self._capacity -1:
            self._i += 1
            return self.table[self._i][1]
        raise StopIteration
