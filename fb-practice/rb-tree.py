import pytest
from collections import deque

BLACK = False
RED = True


class RBTreeNode:
    def __init__(self, key, val, color):
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.color = color


def isred(node):
    if node is None:
        return False
    else:
        return node.color == RED


def rotate_left(node):
    right_node = node.right
    node.right = right_node.left
    right_node.left = node
    right_node.color = node.color
    node.color = RED
    return right_node


def rotate_right(node):
    left_node = node.left
    node.left = left_node.right
    left_node.right = node
    left_node.color = node.color
    node.color = RED
    return left_node


def flip_colors(node):
    node.left.color = BLACK
    node.right.color = BLACK
    node.color = RED


def balance(node):
    if isred(node.right) and not isred(node.left):
        node = rotate_left(node)
    if isred(node.left) and isred(node.left.left):
        node = rotate_right(node)
    if isred(node.left) and isred(node.right):
        flip_colors(node)
    return node


def move_red_left(node):
    flip_colors(node)
    if isred(node.right.left):
        node.right = rotate_right(node.right)
        node = rotate_left(node)
    return node


class RBTree:

    def __init__(self):
        self.__root = None
        self.__size = 0

    def set(self, key, val):
        def insert(node, key, val):
            if node is None:
                self.__size += 1
                return RBTreeNode(key, val, RED)
            if key < node.key:
                node.left = insert(node.left, key, val)
            elif key > node.key:
                node.right = insert(node.right, key, val)
            else:
                node.val = val
            return balance(node)
        self.__root = insert(self.__root, key, val)
        self.__root.color = BLACK

    def delete_min(self):
        def del_min(node):
            if node.left is None:
                return None
            if not isred(node.left) and not isred(node.right):
                node = move_red_left(node)
            node.left = del_min(node.left)
            return balance(node)

        if self.__root is None:
            return
        if not isred(self.__root.left) and not isred(self.__root.right):
            self.__root.color = RED
        self.__root = del_min(self.__root)
        if self.__root is not None:
            self.__root.color = BLACK


    def __str__(self):
        s = ''
        nodes = deque()
        current_depth = 0
        nodes.append((current_depth, self.__root))
        while len(nodes) > 0:
            depth, node = nodes.pop()
            if depth > current_depth:
                s += '\n'
                current_depth = depth
            if node is not None:
                nodes.appendleft((depth + 1, node.left))
                nodes.appendleft((depth + 1, node.right))
                s += '\033[93m' if node.color == RED else ''
                s += str(node.key) + ' '
                s += '\033[0m' if node.color == RED else ''
            else:
                s += '. '
        return s

    def __len__(self):
        return self.__size;

if __name__ == '__main__':
    tree = RBTree()
    for i in range(31, 0, -1):
        tree.set(i, i)
    print(tree)
    print(len(tree))
