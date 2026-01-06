#C++ Vector implementation

import ctypes

class Vector:
    def __init__(self, init_cap: int = 1):
        if init_cap < 1:
            init_cap = 1
        self._cap = init_cap
        self._n = 0
        self._data = (ctypes.c_int * self._cap)()
    
    def capacity(self) -> int:
        return self._cap
    
    def size(self) -> int:
        return self._n
    
    def buffer_address(self) -> int:
        return ctypes.addressof(self._data)
    
    def __len__(self) -> int:
        return self._n
    
    def __getitem__(self, i: int) -> int:
        if not (0 <= i < self._n):
            raise IndexError("Index out of range")
        return int(self._data[i])
    
    def __setitem__(self, i: int, value: int) -> None:
        if not (0 <= i < self._n):
            raise IndexError("Index out of range")
        self._data[i] = int(value)

    def _ensure_cap(self, min_cap: int) -> None:
        if self._cap >= min_cap:
            return

        new_cap = self._cap
        while new_cap < min_cap:
            new_cap *= 2

        new_data = (ctypes.c_int * new_cap)()
        for i in range(self._n):
            new_data[i] = self._data[i]

        self._data = new_data
        self._cap = new_cap

    def push_back(self, value: int) -> None:
        if self._n >= self._cap:
            self._ensure_cap(self._cap * 2)
        self._data[self._n] = int(value)
        self._n += 1

    def resize(self, new_size: int, fill: int = 0) -> None:
        if new_size < 0:
            raise ValueError("New size must be >= 0")
        
        if new_size < self._n:
            self._n = new_size
            return
        
        if new_size > self._cap:
            self._ensure_cap(new_size)

        for i in range(self._n, new_size):
            self._data[i] = int(fill)
        self._n = new_size

    def erase(self, pos: int) -> None:
        if not (0 <= pos < self._n):
            raise IndexError("Index out of range")
        for i in range(pos, self._n - 1):
            self._data[i] = self._data[i + 1]
        self._n -= 1

    def erase_range(self, start: int, end: int) -> None:
        """[start, end)"""
        if not (0 <= start <= end <= self._n):
            raise IndexError("Index out of range")
        count = end - start
        for i in range(start, self._n - count):
            self._data[i] = self._data[i + count]
        self._n -= count

    def to_list(self) -> list:
        return [int(self._data[i]) for i in range(self._n)]
    
if __name__ == "__main__":
    oVec = Vector()
    prev = oVec.buffer_address()

    for i in range(1000000):
        oVec.push_back(i)
        addr = oVec.buffer_address()
        if addr != prev:
            print("reallocated at size =", oVec.size(), "new cap =", oVec.capacity())
            prev = addr