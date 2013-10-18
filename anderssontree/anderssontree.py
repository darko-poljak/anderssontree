#!/usr/bin/env python
# Author: Darko Poljak <darko.poljak@gmail.com>
# License: GPLv3

__all__ = [
    'AATree', 'AnderssonTree', 'ORDER_INFIX_LEFT_RIGHT',
    'ORDER_INFIX_RIGHT_LEFT', 'ORDER_PREFIX_LEFT_RIGHT',
    'ORDER_PREFIX_RIGHT_LEFT', 'ORDER_POSTFIX_LEFT_RIGHT',
    'ORDER_POSTFIX_RIGHT_LEFT'
]


ORDER_INFIX_LEFT_RIGHT = 0
ORDER_INFIX_RIGHT_LEFT = 1
ORDER_PREFIX_LEFT_RIGHT = 2
ORDER_PREFIX_RIGHT_LEFT = 3
ORDER_POSTFIX_LEFT_RIGHT = 4
ORDER_POSTFIX_RIGHT_LEFT = 5


class Node(object):
    """Internal object, represents a tree node."""
    __slots__ = ['key', 'value', 'left', 'right', 'level']

    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.level = level
        self.left = None
        self.right = None

    def __getitem__(self, key):
        """x[key], where key is 0 (left) or 1 (right)"""
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """x[key]=value, where key is 0 (left) or 1 (right)"""
        if key == 0:
            self.left = value
        else:
            self.right = value

    def free(self):
        """Set references to None."""
        self.left = None
        self.right = None
        self.value = None
        self.key = None

    def __repr__(self):
        return "%s(%r, %r, %r)" % (self.__class__.__name__, self.key,
                                   self.value, self.level)

    def copy(self):
        return Node(self.key, self.value, self.level)


class _AATree(object):
    """
    AATree implements a balanced Andersson tree.

    An AA tree in computer science is a form of balanced tree used for
    storing and retrieving ordered data efficiently. AA trees are named
    for Arne Andersson, their inventor.

    AA trees are a variation of the red-black tree, which in turn is an
    enhancement to the binary search tree. Unlike red-black trees, red
    nodes on an AA tree can only be added as a right subchild. In other
    words, no red node can be a left sub-child. This results in the
    imulation of a 2-3 tree instead of a 2-3-4 tree, which greatly
    simplifies the maintenance operations. The maintenance algorithms
    for a red-black tree need to consider seven different shapes to
    properly balance the tree:
    *        *        *        *        *        *        *
     \      /        / \        \      /        /          \
      *    *        *   *        *    *        *            *
                                /      \      /              \
                               *        *    *                *

    An AA tree on the other hand only needs to consider two shapes due
    to the strict requirement that only right links can be red:
    *        *
     \        \
      *        *
                \
                 *

    Whereas red-black trees require one bit of balancing metadata per
    node (the color), AA trees require O(log(N)) bits of metadata per
    node, in the form of an integer "level". The following invariants
    hold for AA trees:
        1. The level of every leaf node is one.
        2. The level of every left child is exactly one less than that
           of its parent.
        3. The level of every right child is equal to or one less than
           that of its parent.
        4. The level of every right grandchild is strictly less than
           that of its grandparent.
        5. Every node of level greater than one has two children.

    A link where the child's level is equal to that of its parent is
    called a horizontal link, and is analogous to a red link in the
    red-black tree. Individual right horizontal links are allowed, but
    consecutive ones are forbidden; all left horizontal links are
    forbidden. These are more restrictive constraints than the
    analogous ones on red-black trees, with the result that
    re-balancing an AA tree is procedurally much simpler than
    re-balancing a red-black tree.

    see: http://en.wikipedia.org/wiki/Andersson_tree
    http://user.it.uu.se/~arnea/abs/simp.html
    http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_andersson.aspx
    """
    def __init__(self, items=None):
        """ AATree() -> new empty tree.
            AATree(mapping,) -> new tree initialized from a mapping
            AATree(seq) -> new tree initialized from seq
                       [(k1, v1), (k2, v2), ... (kn, vn)]

        """
        self._root = None
        self._count = 0
        # store keys in order of tree creation - preserve for copy, repr, ...
        self._keys = []
        if items is not None:
            self.update(items)

    def update(self, *args):
        """ Update tree with items from mapping or seq
            [(k1, v1), (k2, v2), ... (kn, vn)]
        """
        for items in args:
            try:
                # if dict
                gen = items.items()
            except AttributeError:
                # if sequence
                gen = iter(items)
            for k, v in gen:
                self.insert(k, v)

    def _new_node(self, key, value):
        return Node(key, value, 1)

    def root(self):
        """ return root node """
        return self._root

    def _skew(self, node):
        """         |                    |
               L <- T         ==>>       L -> T
              / \    \                  /    / \
             A   B    R                A    B   R
        """
        if node is None:
            return None
        elif node.left is None:
            return node
        elif node.left.level == node.level:
            # swap the pointers of horizontal left links
            lnode = node.left
            node.left = lnode.right
            lnode.right = node
            return lnode
        else:
            return node

    def _split(self, node):
        """   |                      |
              T -> R -> X  ==>>      R
             /    /                 / \
           A     B                 T   X
                                  / \
                                 A   B
        """
        if node is None:
            return None
        elif node.right is None or node.right.right is None:
            return node
        elif node.level == node.right.right.level:
            # two horizontal right links: take the middle node,
            # elevate it and return it
            rnode = node.right
            node.right = rnode.left
            rnode.left = node
            rnode.level += 1
            return rnode
        else:
            return node

    def insert(self, key, value):
        """ insert item into tree, if key exists change value """
        def _insert(node, key, value):
            # do the nromal binary tree insertion
            if node is None:
                return self._new_node(key, value)
            elif key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                node.value = value
            # perform skew and split - whether or not a rotation
            # will occur or not is determined inside skew and split
            node = self._skew(node)
            node = self._split(node)
            return node

        # insert above will only change value for existing key
        if key not in self._keys:
            self._keys.append(key)
        self._count += 1
        self._root = _insert(self._root, key, value)

    def remove(self, key):
        """ remove item from tree """
        def _remove(t, key):
            if t is not None:
                _remove.last = t
                if key < t.key:
                    t.left = _remove(t.left, key)
                else:
                    _remove.deleted = t
                    t.right = _remove(t.right, key)
                if t == _remove.last and _remove.deleted is not None and \
                        key == _remove.deleted.key:
                    _remove.deleted.key = t.key
                    _remove.deleted.value = t.value
                    _remove.deleted = None
                    t = t.right
                    _remove.found = _remove.last
                else:
                    left_level = 0 if t.left is None else t.left.level
                    right_level = 0 if t.right is None else t.right.level
                    if left_level < t.level - 1 or right_level < t.level - 1:
                        t.level -= 1
                        if right_level > t.level:
                            t.right.level = t.level
                        t = self._skew(t)
                        if t.right:
                            t.right = self._skew(t.right)
                            if t.right.right:
                                t.right.right = self._skew(t.right.right)
                        t = self._split(t)
                        if t.right:
                            t.right = self._split(t.right)
            return t
        _remove.found = None

        if self._root is None:
            return
        self._root = _remove(self._root, key)
        if _remove.found:
            _remove.found.free()
            self._keys.remove(key)
            self._count -= 1

    def clear(self):
        """ empty tree """
        def _clear(node):
            if node is not None:
                _clear(node.left)
                _clear(node.right)
                node.free()
        _clear(self._root)
        self._root = None
        self._count = 0
        self._keys = []

    def remove_items(self, keys):
        """ remove item with keys in keys """
        for key in keys:
            self.remove(key)

    def get(self, key):
        """ return value for key """
        node = self._root
        while node and node.key != key:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
        if node:
            return node.value
        else:
            return None

    def __getitem__(self, x):
        return self.get(x)

    def __delitem__(self, x):
        self.remove(x)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __contains__(self, x):
        return self.get(x) is not None

    def is_empty(self):
        return self._root is None

    def traverse(self, func, order=ORDER_INFIX_LEFT_RIGHT):
        """ traverse tree with defined order,
        execute func for each node
        """
        def _traverse(node, func, order):
            if node is not None:
                if order == ORDER_INFIX_LEFT_RIGHT:
                    _traverse(node.left, func, order)
                    func(node)
                    _traverse(node.right, func, order)
                elif order == ORDER_INFIX_RIGHT_LEFT:
                    _traverse(node.right, func, order)
                    func(node)
                    _traverse(node.left, func, order)
                elif order == ORDER_PREFIX_LEFT_RIGHT:
                    func(node)
                    _traverse(node.left, func, order)
                    _traverse(node.right, func, order)
                elif order == ORDER_PREFIX_RIGHT_LEFT:
                    func(node)
                    _traverse(node.right, func, order)
                    _traverse(node.left, func, order)
                elif order == ORDER_POSTFIX_LEFT_RIGHT:
                    _traverse(node.left, func, order)
                    _traverse(node.right, func, order)
                    func(node)
                elif order == ORDER_POSTFIX_RIGHT_LEFT:
                    _traverse(node.right, func, order)
                    _traverse(node.left, func, order)
                    func(node)
        _traverse(self._root, func, order)

    def keys(self, reverse=False):
        """ return keys """
        return (x[0] for x in self.iter_items(reverse=reverse))

    __iter__ = keys

    def __reversed__(self):
        return self.keys(reverse=True)

    def values(self, reverse=False):
        """ return values """
        return (x[1] for x in self.iter_items(reverse=reverse))

    def copy(self):
        """ shallow copy of tree - tree structure, i.e. key insertion
            order is preserved
        """
        copytree = self.__class__()
        for k in self._keys:
            copytree[k] = self.get(k)
        return copytree
    __copy__ = copy

    def __repr__(self):
        selfname = self.__class__.__name__
        gen = ("(%r, %r)" % (k, self.get(k)) for k in self._keys)
        items = ", ".join(gen)
        return "%s([%s])" % (selfname, items)

    def __len__(self):
        return self._count

    def iter_items(self, reverse=False):
        """ generator over (key, value) items """
        if self.is_empty():
            raise StopIteration

        def _iter_items(node, reverse):
            if node is not None:
                if reverse:
                    n1 = node.right
                    n2 = node.left
                else:
                    n1 = node.left
                    n2 = node.right
                for item in _iter_items(n1, reverse):
                    yield item
                yield node.key, node.value
                for item in _iter_items(n2, reverse):
                    yield item
        for item in _iter_items(self.root(), reverse):
            yield item

    def dump(self, order=ORDER_INFIX_LEFT_RIGHT):
        if self._root is not None:
            max_level = self._root.level
        else:
            max_level = 0

        def _dump(node):
            if node is not None:
                level = max_level - node.level
                print("%s(%r, %r)" % ('--' * level, node.key, node.value))
        self.traverse(_dump, order)
        print(repr(self))


class AnderssonTree(_AATree):
    pass


class AATree(_AATree):
    pass
