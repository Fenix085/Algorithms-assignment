class AVLTree:
    class Node:
        __slots__ = ('data', 'left', 'right', 'height')
        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def _h(node):
        return node.height if node else 0
    
    @classmethod
    def _update(cls, node):
        node.height = 1 + max(cls._h(node.left), cls._h(node.right))

    @classmethod
    def _balance(cls, node):
        return cls._h(node.left) - cls._h(node.right) if node else 0
    
    @classmethod
    def _r_right(cls, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        cls._update(y)
        cls._update(x)

        return x
    
    @classmethod
    def _r_left(cls, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        cls._update(x)
        cls._update(y)

        return y
    
    def add(self, data):
        self.root, added = self._add(self.root, data)
        if added:
            self.size += 1
        return added
    
    def _add(self, node, data):
        if node is None:
            return self.Node(data), True
        
        if data < node.data:
            node.left, added = self._add(node.left, data)
        elif data > node.data:
            node.right, added = self._add(node.right, data)
        else:
            return node, False  # data is already in the tree, ignore
        
        self._update(node)
        balance = self._balance(node)

        if balance > 1 and data < node.left.data:
            return self._r_right(node), added
        
        if balance < -1 and data > node.right.data:
            return self._r_left(node), added
        
        if balance > 1 and data > node.left.data:
            node.left = self._r_left(node.left)
            return self._r_right(node), added
        
        if balance < -1 and data < node.right.data:
            node.right = self._r_right(node.right)
            return self._r_left(node), added
        
        return node, added
    
    def find(self, data):
        cur = self.root
        while cur is not None:
            if data == cur.data:
                return cur
            cur = cur.left if data < cur.data else cur.right
        return None
    
    def height(self):
        return self.root.height if self.root else 0
    
if __name__ == "__main__":
    avl = AVLTree()
    avl.add(10)
    avl.add(20)
    avl.add(30)
    avl.add(40)
    avl.add(50)
    avl.add(25)
    print("Height of AVL tree is:", avl.height())