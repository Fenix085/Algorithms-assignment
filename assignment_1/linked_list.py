class LinkedList:
    class Node:
        __slots__ = ['data', 'next']
        def __init__(self, data):
            self.data = data
            self.next = None
    
    def __init__(self):
        self.head = None
        self.tail = None
        self._n = 0

    def push_back(self, x: int) -> None:
        node = self.Node(int(x))
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._n += 1

    def size(self) -> int:
        return self._n