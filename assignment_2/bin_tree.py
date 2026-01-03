class BinaryTree:
    class Node:
        __slots__ = ('data', 'left', 'right')
        def __init__(self, d):
            self.data = d
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None
        self.size = 0

    def add(self, data):
        if self.root is None:
            self.root = self.Node(data)
            self.size = 1
            return True
        
        cur = self.root
        while True:
            if data == cur.data:
                return False
            elif data < cur.data:
                if cur.left is None:
                    cur.left = self.Node(data)
                    self.size += 1
                    return True
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = self.Node(data)
                    self.size += 1
                    return True
                cur = cur.right
    
    def find(self, data):
        cur = self.root
        while cur is not None:
            if data == cur.data:
                return cur
            cur = cur.left if data < cur.data else cur.right
        return None

    def clear(self):
        self.root = None
        self.size = 0

    def inorder(self):
        stack = []
        cur = self.root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            yield cur.data
            cur = cur.right

if __name__ == "__main__":
    oTree = BinaryTree()
    oTree.add(5)
    oTree.add(3)
    oTree.add(7)
    oTree.add(2)
    oTree.add(4)
    oTree.add(6)
    oTree.add(8)
    print("inorder:", list(oTree.inorder()))
