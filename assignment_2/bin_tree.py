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

    def add(self, data=None):
        if self.root is None:
            self.root = self.Node(data)
            self.size = 1
            return

        cur = self.root
        while True:
            if data < cur.data:
                if cur.left is None:
                    cur.left = self.Node(data)
                    self.size += 1
                    return
                cur = cur.left
            elif data > cur.data:
                if cur.right is None:
                    cur.right = self.Node(data)
                    self.size += 1
                    return
                cur = cur.right
            else:
                return  # data is already in the tree, igonre
            
    def find(self, data):
        cur = self.root
        while cur is not None:
            if data == cur.data:
                return cur
            cur = cur.left if data < cur.data else cur.right
        return None

    def remove(self, data):
        self.root, removed = self._remove(self.root, data)
        if removed:
            self.size -= 1
        return removed

    def _remove(self, node, data):
        if node is None:
            return None, False
        
        if data < node.data:
            node.left, removed = self._remove(node.left, data)
            return node, removed
        elif data > node.data:
            node.right, removed = self._remove(node.right, data)
            return node, removed
        
        if node.left is None:
            return node.right, True
        elif node.right is None:
            return node.left, True
        
        succ_value, node.right = self._pop_min(node.right)
        node.data = succ_value
        return node, True
    
    def _pop_min(self, node):
        if node.left is None:
            return node.data, node.right
        min_value, node.left = self._pop_min(node.left)
        return min_value, node

    def clear(self):
        self.root = None
        self.size = 0

    def inorder(self, curr=None):
        if curr is None:
            curr = self.root

        out = []

        def dfs(node):
            if node is None:
                return
            dfs(node.left)
            out.append(node.data)
            dfs(node.right)

        dfs(curr)
        return out

if __name__ == "__main__":
    oTree = BinaryTree()
    oTree.add(5)
    oTree.add(10)
    oTree.add(7)
    oTree.add(2)
    oTree.add(4)
    oTree.add(6)
    oTree.add(8)
    print("inorder:", oTree.inorder(oTree.root))
    oTree.remove(5)
    print("inorder after removing 5:", oTree.inorder(oTree.root))
