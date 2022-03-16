#!/usr/bin/python3

# Splay tree implementation

from sys import stdin


class Node:
    '''Create a node of a Splay tree with appropriate fields.'''
    def __init__(self, key, sum, left, right, parent):
        (self.key, self.sum, self.left,
         self.right, self.parent) = (key, sum, left, right, parent)

def update(node):
    '''Update node sum attitude.'''
    if node is None:
        return None
    node.sum = node.key + (node.left.sum if node.left is not None else 0) \
                        + (node.right.sum if node.right is not None else 0)
    if node.left is not None:
        node.left.parent = node
    if node.right is not None:
        node.right.parent = node

def smallRotation(node):
    '''Perform a rotation to switch a node with its parent.'''
    parent = node.parent
    if parent is None:
        return None
    grandparent = node.parent.parent
    if parent.left == node:
        m = node.right
        node.right = parent
        parent.left = m
    else:
        m = node.left
        node.left = parent
        parent.right = m
    update(parent)
    update(node)
    node.parent = grandparent
    if grandparent is not None:
        if grandparent.left == parent:
            grandparent.left = node
        else:
            grandparent.right = node

def bigRotation(node):
    '''Perform a rotation involving a node, its parent and its grandparent.'''
    if (node.parent.left == node and
        node.parent.parent.left == node.parent):
        # Zig-zig
        smallRotation(node.parent)
        smallRotation(node)
    elif (node.parent.right == node and
          node.parent.parent.right == node.parent):
        # Zig-zig
        smallRotation(node.parent)
        smallRotation(node)
    else:
        # Zig-zag
        smallRotation(node)
        smallRotation(node)

# Makes splay of the given node and makes it the new root.
def splay(node):
    if node is None:
        return None
    while node.parent is not None:
        if node.parent.parent is None:
            smallRotation(node)
            break
        bigRotation(node)
    return node

# Searches for the given key in the tree with the given root and calls
# splay for the deepest visited node after that.
# Returns pair of the result and the new root.
# If found, result is a pointer to the node with the given key.
# Otherwise, result is a pointer to the node with the smallest
# bigger key (next value in the order).
# If the key is bigger than all keys in the tree,
# then result is None.

def find(root, key):
    v = root
    last = root
    next = None
    while v is not None:
        if v.key >= key and (next == None or v.key < next.key):
            next = v
        last = v
        if v.key == key:
            break
        if v.key < key:
            v = v.right
        else:
            v = v.left
    root = splay(last)
    return next, root

def split(root, key):
    '''Splits the tree at key and returns left and right subtrees.
    Smaller values go to the left subtree, equal or bigger values go to
    the right subtree.'''
    result, root = find(root, key)
    if result is None:
        return root, None
    right = splay(result)
    left = right.left
    right.left = None
    if left is not None:
        left.parent = None
        update(left)
    update(right)
    return left, right

def merge(left, right):
    '''Merge left and right subtrees into a single tree.'''
    if left is None:
        return right
    if right is None:
        return left
    while right.left is not None:
        right = right.left
    right = splay(right)
    right.left = left
    update(right)
    return right


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, x):
        '''Create a new node with a new key.'''
        left, right = split(self.root, x)
        new_vertex = None
        if right is None or right.key != x:
            new_vertex = Node(x, x, None, None, None)
        self.root = merge(merge(left, new_vertex), right)

    def erase(self, x):
        next, root = find(self.root, x)
        N = root
        if N.right:
            M = N.right
            while M.left:
                M = M.left
            M = splay(M)
        N = splay(N)
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
        _, self.root = find(self.root, x)
        if self.root:
            if self.root.key == x:
                return True
        return False

    def sum(self, fr, to):
        '''Find the sum of elements within a range.'''
        (left, middle) = split(self.root, fr)
        (middle, right) = split(middle, to + 1)
        if middle:
            ans = middle.sum
        else:
            ans = 0
        self.root = merge(left, merge(middle, right))
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
