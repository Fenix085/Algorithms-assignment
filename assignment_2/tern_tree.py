class TernaryTree:
    class Node:
        __slots__ = ('data_l', 'data_r', 'left', 'middle', 'right')
        def __init__(self, dl, dr = None):
            self.data_l = dl
            self.data_r = dr
            self.left = None
            self.middle = None
            self.right = None

    def __init__(self):
        self.root = None
        self.size = 0
    
    def add(self, data):
        if self.root is None:
            self.root = self.Node(data)
            self.size = 1
            return
        
        cur = self.root
        while True:
            if data == cur.data_l or (cur.data_r is not None and data == cur.data_r):
                return  # data is already in the tree, ignore
            
            if data < cur.data_l:
                if cur.left is None:
                    cur.left = self.Node(data)
                    self.size += 1
                    return
                cur = cur.left
            elif cur.data_r is None or data < cur.data_r:
                if cur.data_r is None:
                    cur.data_r = data
                    self.size += 1
                    return
                if cur.middle is None:
                    cur.middle = self.Node(data)
                    self.size += 1
                    return
                cur = cur.middle
            else:
                if cur.right is None:
                    cur.right = self.Node(data)
                    self.size += 1
                    return
                cur = cur.right

    def find(self, data):
        cur = self.root
        while cur is not None:
            if data == cur.data_l or (cur.data_r is not None and data == cur.data_r):
                return cur
            
            if data < cur.data_l:
                cur = cur.left
            elif cur.data_r is None or data < cur.data_r:
                cur = cur.middle
            else:
                cur = cur.right

    def height(self, node=None):
        if node is None:
            node = self.root
        
        def _height(n):
            if n is None:
                return 0
            return 1 + max(_height(n.left), _height(n.middle), _height(n.right))

        return _height(node)
    
if __name__ == "__main__":
    tTree = TernaryTree()
    tTree.add(5)
    tTree.add(3)
    tTree.add(7)
    tTree.add(4)
    tTree.add(6)
    tTree.add(8)
    print("height:", tTree.height())