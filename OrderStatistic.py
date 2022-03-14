#!/usr/bin/python3

#from BSTwithDuplicates import *
import math
import os
import random
import re
import sys




class TreeNode:
    def __init__(self,key,val,left=None,right=None,parent=None,height=1,size=1,copies=1):
        self.key = key
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.height = height
        self.size = size
        self.copies = copies
    def isLeft(self):
        return self.parent and self.parent.left == self
    def isRight(self):
        return self.parent and self.parent.right == self
    def isRoot(self):
        return not self.parent
    def isLeaf(self):
        return not (self.right or self.left)
    def hasAnyChild(self):
        return self.right or self.left
    def hasBothChild(self):
        return self.right and self.left
    def hasOneChildOnly(self):
        return (not self.right and self.left) or (self.right and not self.left)

    def changeNodeData(self,key,val,height,left,right,size,copies):
        self.key = key
        self.val = val
        self.left = left
        self.right = right
        self.height = height
        self.size = size
        self.copies = copies
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self

    def adjustHeightSize(self):
        # print(f'adjusting height of {self.key}')
        # print(f'height of {self.key} was {self.height}')
        if self.hasBothChild():
            self.height = 1 + max([self.left.height, self.right.height])
            self.size = self.copies + self.left.size + self.right.size
        elif self.left:
            self.height = 1 + self.left.height
            self.size = self.copies + self.left.size
        elif self.right:
            self.height = 1 + self.right.height
            self.size = self.copies + self.right.size
        else:
            self.height = 1
            self.size = self.copies
        # print(f'height, size of {self.key} adjusted to {self.height}, {self.size}. adjusting {self.parent}')
        if self.parent:
            self.parent.adjustHeightSize()

    def leftDescendant(self):
        if self.left:
            return self.left.leftDescendant()
        else:
            return self

    def successor(self):
        # succ = None
        if self.right:
            return self.right.leftDescendant()
        else:
            if self.parent:
                   if self.isLeft():
                       succ = self.parent
                   # else:
                   #     self.parent.right = None
                   #     succ = self.parent.successor()
                   #     self.parent.right = self
        return succ

    def sliceOut(self):
        if self.isLeaf():
            if self.isLeft():
                   self.parent.left = None
            else:
                   self.parent.right = None
            return self.parent #from here, weight adjustment should propagate up
        elif self.hasAnyChild():
            if self.left:
                   if self.isLeft():
                      self.parent.left = self.left
                   else:
                      self.parent.right = self.left
                   self.left.parent = self.parent
                   return self.left #from here, weight adjustment should propagate up
            else:
                   if self.isLeft():
                      self.parent.left = self.right
                   else:
                      self.parent.right = self.right
                   self.right.parent = self.parent
                   return self.right #from here, weight adjustment should propagate up


    def __iter__(self):

        """ return the iterator that iterates through the elements in the BST
        rooted at this node in an inorder sequence """

        if self.left:
            # The following iterates through all the nodes in the left subtree.
            # The first thing that python does when the for loop is encountered
            # is to obtain an iterator object for the left subtree.
            # This is done ("under the covers") by recursively calling
            # the __iter__ method on the left child.
            for elt in self.left:
                yield elt

        # at this point we "visit" the current node
        yield (self.key, self.val, self.height, self.size, self.copies)

        if self.right:
            # we now visit all the nodes in the right subtree
            for elt in self.right:
                yield elt

class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def __iter__(self):
        """ returns an iterator for the binary search tree """
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

    def rotateRight(self, currentNode):
        # print(f'node {currentNode.key} is rotating right')
        P, Y = currentNode.parent, currentNode.left
        B = Y.right
        Y.parent = P
        if currentNode.isLeft():
            P.left = Y
        if currentNode.isRight():
            P.right = Y
        currentNode.parent = Y
        if B:
            B.parent = currentNode
        Y.right, currentNode.left = currentNode, B
        if P is None: # Y becomes new root
            self.root = Y
        #     print(f'Root change to {Y.key}')
        # print(f'Right rotation of {currentNode.key} complete')

    def rotateLeft(self, currentNode): # Opposite of rotateRight
        # print(f'node {currentNode.key} is rotating left')
        P, X = currentNode.parent, currentNode.right
        B = X.left
        X.parent = P
        if currentNode.isLeft():
            P.left = X
        if currentNode.isRight():
            P.right = X
        currentNode.parent = X
        if B:
            B.parent = currentNode
        X.left, currentNode.right = currentNode, B
        if P is None: # X becomes the new root
            self.root = X
        #     print(f'Root change to {X.key}')
        # print(f'Left rotation of {currentNode.key} complete')

    def rebalanceRight(self, currentNode):
        # print(f'rebalancing {currentNode.key} towards right')
        M = currentNode.left
        if M.hasBothChild():
            if M.right.height > M.left.height:
                self.rotateLeft(M)
                M.adjustHeightSize()
        if M.hasOneChildOnly():
            if M.left:
                self.rotateRight(M)
            else:
                self.rotateLeft(M)
            M.adjustHeightSize()

        self.rotateRight(currentNode)
        # print(f'adjusting {currentNode.key} after right rotation')
        currentNode.adjustHeightSize()
        # print(f'Right rebalanced of {currentNode.key}')


    def rebalanceLeft(self, currentNode):
        # print(f'rebalancing {currentNode.key} towards left')
        M = currentNode.right
        if M.hasBothChild():
            if M.left.height > M.right.height:
                self.rotateRight(M)
                M.adjustHeightSize()
        if M.hasOneChildOnly():
            if M.left:
                self.rotateRight(M)
            else:
                self.rotateLeft(M)
            M.adjustHeightSize()
        self.rotateLeft(currentNode)
        currentNode.adjustHeightSize()
        # print(f'Left rebalanced of {currentNode.key}')


    def rebalance(self,currentNode):
        # print(f'rebalancing {currentNode.key}')
        if currentNode.hasBothChild():
            if currentNode.left.height > currentNode.right.height+1:
                self.rebalanceRight(currentNode)
            elif currentNode.right.height > currentNode.left.height+1:
                self.rebalanceLeft(currentNode)
        if currentNode.hasOneChildOnly():
            if currentNode.left:
                # print(f'{currentNode.key} has only a left child')
                if currentNode.left.height > 1:
                    self.rebalanceRight(currentNode)
            else:
                # print(f'{currentNode.key} has only a right child')
                if currentNode.right.height > 1:
                    self.rebalanceLeft(currentNode)
        # print(f'Tree rebalanced at {currentNode.key}')
        if currentNode.parent:
            self.rebalance(currentNode.parent)


    def put(self,key,val=None):
        if self.root:
            self._put(key,val,self.root)
        else:
            self.root = TreeNode(key,val)
            # print(f'Creating root node {self.root.key}')
        self.size += 1

    def _put(self,key,val,currentNode):
        # print(f'Starting from node {currentNode.key} ...')
        if key == currentNode.key: #duplicate key
            currentNode.copies += 1
            currentNode.adjustHeightSize()
            return
        elif key < currentNode.key:
            if currentNode.left:
                self._put(key,val,currentNode.left)
            else:
                currentNode.left = TreeNode(key,val,parent=currentNode)
                # print(f'{key} attached to left of {currentNode.key}')
                # print(f'height {currentNode.key} is {currentNode.height}. New node created as left child of {currentNode.key}')
                currentNode.adjustHeightSize()
                self.rebalance(currentNode)
        else:
            if currentNode.right:
                self._put(key,val,currentNode.right)
            else:
                currentNode.right = TreeNode(key,val,parent=currentNode)
                # print(f'{key} attached to right of {currentNode.key}')
                currentNode.adjustHeightSize()
                self.rebalance(currentNode)


    '''With the put method defined, we can easily overload the [] operator for assignment by having the __setitem__ method call the put method.
    This allows us to write Python statements like myZipTree['Plymouth'] = 55446, just like a Python dictionary.'''
    def __setitem__(self,k,v):
        self.put(k,v)

    def get(self,key):
        if self.root:
            res = self._get(key,self.root)
            if res:
                   return res.val
            else:
                   return None
        else:
            return None

    def _get(self,key,currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key,currentNode.left)
        else:
            return self._get(key,currentNode.right)

    def __getitem__(self,key):
        return self.get(key)

    def __contains__(self,key):
        if self._get(key,self.root):
            return True
        else:
            return False

    def delete(self,key):
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

    def __delitem__(self,key):
        self.delete(key)

    def remove(self,currentNode):
        if currentNode.copies > 1:
            currentNode.copies -= 1
            currentNode.adjustHeightSize()
        elif currentNode.isLeaf():
            p = currentNode.sliceOut() #leaf
            p.adjustHeightSize()
            self.rebalance(p)

        elif currentNode.hasBothChild(): #interior
            succ = currentNode.successor()
            parent = succ.parent
            p = succ.sliceOut()
            currentNode.key = succ.key
            currentNode.val = succ.val
            p.adjustHeightSize()
            self.rebalance(p)

        else: # this node has one child
            P = None
            if currentNode.left:
                P = currentNode.left
                if currentNode.isLeft():
                    currentNode.left.parent = currentNode.parent
                    currentNode.parent.left = currentNode.left
                elif currentNode.isRight():
                    currentNode.left.parent = currentNode.parent
                    currentNode.parent.right = currentNode.left
                else:   #it is the root
                    currentNode.changeNodeData(currentNode.left.key,
                                        currentNode.left.val,
                                        currentNode.left.height,
                                        currentNode.right.size,
                                        currentNode.left.left,
                                        currentNode.left.right)
            else:
                P = currentNode.right
                if currentNode.isLeft():
                    currentNode.right.parent = currentNode.parent
                    currentNode.parent.left = currentNode.right
                elif currentNode.isRight():
                    currentNode.right.parent = currentNode.parent
                    currentNode.parent.right = currentNode.right
                else:
                    currentNode.changeNodeData(currentNode.right.key,
                                        currentNode.right.val,
                                        currentNode.right.height,
                                        currentNode.right.size,
                                        currentNode.right.left,
                                        currentNode.right.right)
            P.adjustHeightSize()
            self.rebalance(P)


def findByRank(root, k):
    if root is None:
        print('Error: not found')
    if root.left is None:
        leftcount = 0
    else:
        leftcount = root.left.size
    if k <= leftcount:
        return findByRank(root.left, k)
    elif k > leftcount and k <= leftcount + root.copies:
        return root.key
    elif k > leftcount + root.copies:
        return findByRank(root.right, k-leftcount-root.copies)


def median(tree):
    size = tree.size
    if size % 2 == 1:
        mid = (size + 1)//2
        return findByRank(tree.root, mid)
    else:
        return (findByRank(tree.root, size//2) + findByRank(tree.root, size//2+1))/2



bst = BinarySearchTree()

def activityNotifications(expend, d):
    s = 0
    for i in range(d):
        bst.put(expend[i])
    for i in range(d,n):
        med = median(bst)
        #print(med)
        if expend[i] >= 2*med:
            s += 1
        del bst[expend[i-d]]
        bst.put(expend[i])
    return s


if __name__ == '__main__':

    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    d = int(first_multiple_input[1])

    expenditure = list(map(int, input().rstrip().split()))

    result = activityNotifications(expenditure, d)

    fptr.write(str(result) + '\n')
    
    fptr.close()
