#!/usr/bin/python3

# AVL- Python Implementation

class AVLNode:
    '''Create nodes with their associated methods.'''
    def __init__(self, key, val, left=None, right=None,
                 parent=None, height=1, size=1, copies=1):
        self.key = key
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.height = height
        self.size = size
        self.copies = copies

    def is_left(self):
        return self.parent and self.parent.left == self

    def is_right(self):
        return self.parent and self.parent.right == self

    def is_root(self):
        return not self.parent

    def is_leaf(self):
        return not (self.right or self.left)

    def has_any_child(self):
        return self.right or self.left

    def has_both_child(self):
        return self.right and self.left

    def has_one_child_only(self):
        return ((not self.right and self.left) or
                (self.right and not self.left))

    def adjust_height_size(self):
        '''Recursively adjust the height and the size of self and its ancesters
        up to the root.'''
        if self.has_both_child():
            self.height = 1 + max([self.left.height, self.right.height])
            self.size = self.copies + self.left.size + self.right.size
        elif self.left:
            self.height = 1 + self.left.height
            self.size = self.copies + self.left.size
        elif self.right:
            self.height = 1 + self.right.height
            self.size = self.copies + self.right.size
        else:   # It's a leaf
            self.height = 1
            self.size = self.copies
        if self.parent:
            self.parent.adjust_height_size()

    def left_descendant(self):
        if self.left:
            return self.left.left_descendant()
        else:
            return self

    def successor(self):
        '''Find the immediate successor to self in the tree and return it.'''
        if self.right:
            return self.right.left_descendant()
        if self.parent:
            if self.is_left():
               succ = self.parent
        return succ

    def slice_out(self):
        '''Cut out self and return its parent from where height-size adjustment
        is propagated up towards the root.'''
        if self.is_leaf():
            if self.is_left():
                self.parent.left = None
            else:
                self.parent.right = None
            return self.parent
        elif self.has_any_child():
            if self.left:
                if self.is_left():
                   self.parent.left = self.left
                else:
                   self.parent.right = self.left
                self.left.parent = self.parent
                return self.left
            else:
                if self.is_left():
                   self.parent.left = self.right
                else:
                   self.parent.right = self.right
                self.right.parent = self.parent
                return self.right

    def __iter__(self):
        '''Iterate through the elements in the BST rooted at self in an
        in-order sequence and yield nodes with all their contents.'''
        if self.left:
            yield from self.left
        yield (self.key, self.val, self.height, self.size, self.copies)
        if self.right:
            yield from self.right


class BinarySearchTree:
    '''Build a AVL binary search tree.'''
    def __init__(self):
        self.root = None
        self.size = 0

    def __iter__(self):
        """ Return an iterator for the binary search tree."""

        class EmptyIterator:
            def next(self):
                raise StopIteration

        if self.root:
            # if the tree is not empty, just return the root's iterator
            return iter(self.root)
        else:
            # otherwise return the iterator that immediately raises
            # a StopIteration exception
            return EmptyIterator()

    def rotate_right(self, currentNode):
        '''Perform local rotation to right and update children and parents.'''
        P, Y = currentNode.parent, currentNode.left
        B = Y.right
        Y.parent = P
        if currentNode.is_left():
            P.left = Y
        if currentNode.is_right():
            P.right = Y
        currentNode.parent = Y
        if B:
            B.parent = currentNode
        Y.right, currentNode.left = currentNode, B
        if P is None:   # Y becomes the new root
            self.root = Y

    def rotate_left(self, currentNode):
        '''Perform local rotation to left and update children and parents.'''
        P, X = currentNode.parent, currentNode.right
        B = X.left
        X.parent = P
        if currentNode.is_left():
            P.left = X
        if currentNode.is_right():
            P.right = X
        currentNode.parent = X
        if B:
            B.parent = currentNode
        X.left, currentNode.right = currentNode, B
        if P is None:   # X becomes the new root
            self.root = X

    def rebalance_right(self, currentNode):
        '''Rebalance the tree to right at current node if left subtree is
        longer. Perform rotations and update heights/sizes.'''
        M = currentNode.left
        if M.has_both_child():
            if M.right.height > M.left.height:
                self.rotate_left(M)
                M.adjust_height_size()
        if M.has_one_child_only():
            if M.left:
                self.rotate_right(M)
            else:
                self.rotate_left(M)
            M.adjust_height_size()
        self.rotate_right(currentNode)
        currentNode.adjust_height_size()

    def rebalance_left(self, currentNode):
        '''Rebalance the tree to right at current node if left subtree is
        longer. Perform rotations and update heights/sizes.'''
        M = currentNode.right
        if M.has_both_child():
            if M.left.height > M.right.height:
                self.rotate_right(M)
                M.adjust_height_size()
        if M.has_one_child_only():
            if M.left:
                self.rotate_right(M)
            else:
                self.rotate_left(M)
            M.adjust_height_size()
        self.rotate_left(currentNode)
        currentNode.adjust_height_size()

    def rebalance(self,currentNode):
        '''Recursively balance the tree starting at current node upwards to the
        root using methods `rebalance_right` or `rebalance_left`.'''
        if currentNode.has_both_child():
            if currentNode.left.height > currentNode.right.height+1:
                self.rebalance_right(currentNode)
            elif currentNode.right.height > currentNode.left.height+1:
                self.rebalance_left(currentNode)
        if currentNode.has_one_child_only():
            if currentNode.left:
                if currentNode.left.height > 1:
                    self.rebalance_right(currentNode)
            else:
                if currentNode.right.height > 1:
                    self.rebalance_left(currentNode)
        if currentNode.parent:
            self.rebalance(currentNode.parent)

    def insert(self, key, val=None):
        '''Insert a given key into BST by calling the private
        method _insert. Default value of a key is None.'''
        if self.root:
            self._insert(key, val, self.root)
        else:
            self.root = AVLNode(key, val)
        self.size += 1

    def _insert(self, key, val, currentNode):
        if key == currentNode.key:  # Duplicate key
            currentNode.copies += 1
            currentNode.adjust_height_size()
            return None
        elif key < currentNode.key:
            if currentNode.left:
                self._insert(key, val, currentNode.left)
            else:
                currentNode.left = AVLNode(key, val, parent=currentNode)
                currentNode.adjust_height_size()
                self.rebalance(currentNode)
        else:
            if currentNode.right:
                self._insert(key, val, currentNode.right)
            else:
                currentNode.right = AVLNode(key, val, parent=currentNode)
                currentNode.adjust_height_size()
                self.rebalance(currentNode)

    # With the insert method defined, we can easily overload the [] operator for
    # assignment by having the __setitem__ method call the insert method.
    # This allows us to write Python statements like myTree['Plymouth']=55446,
    # just like a Python dictionary.
    def __setitem__(self, key, value):
        self.insert(key, value)

    def get(self, key):
        '''Return the value for a given key.'''
        if self.root:
            res = self._get(key, self.root)
            if res:
                   return res.val
            else:
                   return None
        return None

    def _get(self, key, currentNode):
        '''Recursively search for a node with given key in the subtree
        under the current node.'''
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.left)
        else:
            return self._get(key, currentNode.right)

    # Overloads the [] operator for getting value for given key.
    def __getitem__(self, key):
        return self.get(key)

    # Allows `in` operator to work, in a for loop for instance.
    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        '''Find the node with a given key and remove it from the tree or reduce
        its multiplicity (copies).'''
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size -= 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Error, key not in tree')

    # Allows for `del` operator to work
    def __delitem__(self, key):
        self.delete(key)

    def remove(self, currentNode):
        '''Implement the process of removing a node or reducing
        its multiplicity (copies).'''
        if currentNode.copies > 1:
            currentNode.copies -= 1
            currentNode.adjust_height_size()
        elif currentNode.is_leaf():
            p = currentNode.slice_out()
            p.adjust_height_size()
            self.rebalance(p)
        elif currentNode.has_both_child():
            # The node should be replaced by its successor
            succ = currentNode.successor()
            parent = succ.parent
            p = succ.slice_out()
            currentNode.key = succ.key
            currentNode.val = succ.val
            p.adjust_height_size()
            self.rebalance(p)
        else:   # This node has only one child
            if currentNode.left:
                P = currentNode.left
                if currentNode.is_left():
                    currentNode.left.parent = currentNode.parent
                    currentNode.parent.left = currentNode.left
                elif currentNode.is_right():
                    currentNode.left.parent = currentNode.parent
                    currentNode.parent.right = currentNode.left
                else:   # It is the root
                    self.root = currentNode.left
                    currentNode.left.parent = None
            else:
                P = currentNode.right
                if currentNode.is_left():
                    currentNode.right.parent = currentNode.parent
                    currentNode.parent.left = currentNode.right
                elif currentNode.is_right():
                    currentNode.right.parent = currentNode.parent
                    currentNode.parent.right = currentNode.right
                else:
                    self.root = currentNode.right
                    currentNode.right.parent = None
            P.adjust_height_size()
            self.rebalance(P)


# Different funtionalities can be deriven from BSTs by adding appropriate
# fields, such as node size. One of these applications is to caculate rolling
# statstics such as median, percentiles and so on.

def find_by_rank(root, k):
    '''Find the k th smallest element in the tree.'''
    if root is None:
        print('Error: not found')
    if root.left is None:
        leftcount = 0
    else:
        leftcount = root.left.size
    if k <= leftcount:
        return find_by_rank(root.left, k)
    elif (k>leftcount) and (k<=leftcount+root.copies):
        return root.key
    elif k > leftcount+root.copies:
        return find_by_rank(root.right, k-leftcount-root.copies)

def median(tree):
    '''Find the median of the tree using rank function.'''
    size = tree.size
    if size%2 == 1:
        mid = (size+1) // 2
        return find_by_rank(tree.root, mid)
    else:
        return (find_by_rank(tree.root, size//2)
                + find_by_rank(tree.root, size//2+1))/2


if __name__ == '__main__':
    # Let's find median of a list of numbers with repetition:
    bst = BinarySearchTree()
    List = [3.7, 2, 4, 5.5, 4, 6.1, 7, 2, 3]
    for elem in List:
        bst.insert(elem)     # or we can say "bst[elem]"
    print('Nodes in the tree are:')
    for node in bst:
        print(node)
    print('\n')
    print('median({}) = {}'.format(List, median(bst)))
