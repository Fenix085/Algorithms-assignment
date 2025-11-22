#C++ Vector implementation

class Vector:
    def __init__(self):
        self.data = []
        self.cap = 1
    
    def push_back(self, value):
        self.data.append(value)
        if len(self.data) > self.cap:
            self.cap *= 2

    def pop_back(self):
        if not self.is_empty():
            return self.data.pop()
        raise IndexError("pop_back from empty Vector")
    
    def front(self):
        if not self.is_empty():
            return self.data[0]
        raise IndexError("front from empty Vector")
    
    def back(self):
        if not self.is_empty():
            return self.data[-1]
        raise IndexError("back from empty Vector")
    
    def at(self, index):
        if 0 <= index < len(self.data):
            return self.data[index]
        raise IndexError("index out of range")

    def is_empty(self):
        return len(self.data) == 0
    
    def clear(self):
        self.data = []
        self.cap = 1

    def capacity(self):
        return self.cap
    
    def size(self):
        return len(self.data)
    
if __name__ == "__main__":
    oVector = Vector()
    for i in range(10):
        oVector.push_back(2**i)
    print("Vector contents:", [oVector.at(i) for i in range(oVector.size())])
    print("Vector size:", oVector.size())
    print("Vector capacity:", oVector.capacity())
    print("Front element:", oVector.front())
    print("Back element:", oVector.back())
    oVector.pop_back()
    print("After pop_back, Vector contents:", [oVector.at(i) for i in range(oVector.size())])
    oVector.clear()
    print("After clear, Vector size:", oVector.size())
    print("After clear, Vector is empty:", oVector.is_empty())