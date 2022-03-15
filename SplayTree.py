#!/usr/bin/python3

# Splay tree implementation

class Node:
    '''Create a node of a Splay tree with appropriate fields.'''
    def __init__(self, key, sum, left, right, parent):
        (self.key, self.sum,
         self.left, self.right, self.parent) = (key, sum, left, right, parent)

    def update(self):
        '''Update node sum attitude.'''
        self.sum = self.key + (self.left.sum if self.left != None else 0) \
                            + (self.right.sum if self.right != None else 0)
        if self.left is not None:
            self.left.parent = self
        if self.right is not None:
            self.right.parent = self

    def smallRotation(self):
        '''Perform a rotation to switch a node with its parent.'''
        parent = self.parent
        if parent is None:
            return None
        grandparent = self.parent.parent
        if parent.left == self:
            m = self.right
            self.right = parent
            parent.left = m
        else:
            m = self.left
            self.left = parent
            parent.right = m
        parent.update()
        self.update()
        self.parent = grandparent
        if grandparent is not None:
            if grandparent.left == parent:
                grandparent.left = self
            else:
                grandparent.right = self

    def bigRotation(self):
        '''Perform a rotation involving a node, its parent and its grandparent.'''
        if (self.parent.left == self and
            self.parent.parent.left == self.parent):
            # Zig-zig
            self.parent.smallRotation()
            self.smallRotation()
        elif (self.parent.right == self and
              self.parent.parent.right == self.parent):
            # Zig-zig
            self.parent.smallRotation()
            self.smallRotation()
        else:
            # Zig-zag
            self.smallRotation()
            self.smallRotation()


class SplayTree:
    def __init__(self):
        self.root = None
    # Makes splay of the given node and makes it the new root.
    def splay(self, currentNode):
        if currentNode is None:
            return None
        while currentNode.parent is not None:
            if currentNode.parent.parent is None:
                currentNode.smallRotation()
                break
            currentNode.bigRotation()
        self.root = currentNode
        return self.root
    # Searches for the given key in the tree with the given root and calls
    # splay for the deepest visited node after that.
    # Returns pair of the result and the new root.
    # If found, result is a pointer to the node with the given key.
    # Otherwise, result is a pointer to the node with the smallest
    # bigger key (next value in the order).
    # If the key is bigger than all keys in the tree,
    # then result is None.
    def find(self, key):
        v = self.root
        last = self.root
        next = None
        while v != None:
            if v.key >= key and (next == None or v.key < next.key):
                next = v
            last = v
            if v.key == key:
                break
            if v.key < key:
                v = v.right
            else:
                v = v.left
        self.splay(last)
        return next

    def split(self, key):
        '''Splits the tree at key. Smaller values go to left, equal or bigger
        values go to the right subtree.'''
        result = self.find(key)
        if result is None:
            return (self.root, None)
        right = self.splay(result)
        left = right.left
        right.left = None
        if left is not None:
            left.parent = None
            left.update()
        right.update()
        return (left, right)

    def merge(self, left, right):
        '''Merge two subtrees into one single tree.'''
        if left is None:
            return right
        if right is None:
            return left
        while right.left is not None:
            right = right.left
        right = self.splay(right)
        right.left = left
        right.update()
        return right

    def insert(self, x):
        '''Create a new node with a new key.'''
        (left, right) = self.split(x)
        new_vertex = None
        if right is None or right.key != x:
            new_vertex = Node(x, x, None, None, None)
        self.root = self.merge(self.merge(left, new_vertex), right)

    def erase(self, x):
        next = self.find(x)
        N = self.root
        if N.right:
            M = N.right
            while M.left:
                M = M.left
            M = self.splay(M)
        N = self.splay(N)
        L = N.left
        R = N.right
        if L:
            L.parent = R
        if R:
            R.left = L
            R.parent = None
            self.root = R
        else:
            self.root = L

    def search(self, x):
        self.find(x)
        if self.root:
            if self.root.key == x:
                return True
        return False

    def sum(self, fr, to):
        '''Find the sum of elements within a range.'''
        (left, middle) = self.split(fr)
        (middle, right) = self.split(to + 1)
        if middle:
            ans = middle.sum
        else:
            ans = 0
        self.root = self.merge(left, self.merge(middle, right))
        return ans

stree = SplayTree()
MODULO = 1000000001
n = int(stdin.readline())
last_sum_result = 0
for i in range(n):
  line = stdin.readline().split()
  if line[0] == '+':
    x = int(line[1])
    stree.insert((x+last_sum_result) % MODULO)
  elif line[0] == '-':
    x = int(line[1])
    stree.erase((x+last_sum_result) % MODULO)
  elif line[0] == '?':
    x = int(line[1])
    print('Found' if stree.search((x+last_sum_result) % MODULO) else 'Not found')
  elif line[0] == 's':
    l = int(line[1])
    r = int(line[2])
    res = stree.sum((l+last_sum_result) % MODULO, (r+last_sum_result) % MODULO)
    print(res)
    last_sum_result = res % MODULO
