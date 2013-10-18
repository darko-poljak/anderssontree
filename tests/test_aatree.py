#!/usr/bin/env python
# Author: Darko Poljak <darko.poljak@gmail.com>
# License: GPLv3

import unittest
import pickle
from random import randint, shuffle
from anderssontree import AnderssonTree


class AATreeException(Exception):
    pass


def test_items_seq(maxval=200):
    x = list(range(0, maxval))
    y = list(zip(x, x))
    return y


def test_items_dict(maxval=200):
    return {x: x for x in range(0, maxval)}


class TestAATree(unittest.TestCase):
    def test_init_empty(self):
        tree = AnderssonTree()
        self.assertEqual(len(tree), 0)

    def test_init_dict(self):
        d = test_items_dict()
        tree = AnderssonTree(d)
        self.assertEqual(len(tree), len(d))
        self.check_aatree_properties(tree)

    def test_init_seq(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        self.assertEqual(len(tree), len(s))
        self.check_aatree_properties(tree)

    def test_pickle_protocol(self):
        s = test_items_seq()
        tree1 = AnderssonTree(s)
        pickle_str = pickle.dumps(tree1, -1)
        tree2 = pickle.loads(pickle_str)
        self.assertEqual(len(tree1), len(tree2))
        self.assertEqual(list(tree1.keys()), list(tree2.keys()))
        self.assertEqual(list(tree1.values()), list(tree2.values()))
        self.check_aatree_properties(tree1)
        self.check_aatree_properties(tree2)

    def test_max_btree_level(self):
        def _map_levels(node, level, map_):
            if node is not None:
                map_[node.key] = level
                next_level = level + 1
                _map_levels(node.left, next_level, map_)
                _map_levels(node.right, next_level, map_)

        def _map_bin_tree_levels(root):
            """ level is binary tree level, not AATree level """
            map_ = {}
            _map_levels(root, 0, map_)
            max_level = max(map_.values())
            for k, v in map_.items():
                map_[k] = max_level - map_[k] + 1
            return map_
        keys = range(1, 14)
        tree = AnderssonTree(zip(keys, keys))
        mapping = _map_bin_tree_levels(tree.root())
        maxl = max(mapping.values())
        self.assertEqual(maxl, 5, 'Invalid max level %s!' % maxl)

    def check_aatree_properties(self, tree, dump=True):
        """
        The level of every leaf node is one.
        The level of every left child is exactly one less than that of
        its parent.
        The level of every right child is equal to or one less than
        that of its parent.
        The level of every right grandchild is strictly less than that
        of its grandparent.
        Every node of level greater than one has two children.
        """
        def _check_child_level(node, maxlevel):
            if node is not None:
                if node.level >= maxlevel:
                    msg = 'grandchild level >= grandparent level ' \
                        'at %s' % str(node.key)
                    raise AATreeException(msg)
                _check_child_level(node.left, maxlevel)
                _check_child_level(node.right, maxlevel)

        def _check_properties(node, parent, grandparent):
            if node is not None:
                if node.left is None and node.right is None:
                    if node.level != 1:
                        raise AATreeException('leaf level is not 1 at '
                                              '%s' % node.key)
                if parent is not None and node.left is not None:
                    if node.left.level != node.level - 1:
                        raise AATreeException(
                            'left child level not exactly'
                            ' one less than that of its parent at '
                            '%s' % str(node.key))
                if parent is not None and node.right is not None:
                    if not (node.right.level == node.level or
                            node.right.level == node.level - 1):
                            raise AATreeException(
                                'right child level is'
                                ' not equal to or one less than of its'
                                ' parent at %s' % str(node.key))
                if grandparent is not None:
                    maxl = grandparent.level
                    x = grandparent.right
                    if x:
                        _check_child_level(x.right, maxl)
                        _check_child_level(x.left, maxl)
                        if node.level > 1:
                            if node.left is None or node.right is None:
                                raise AATreeException(
                                    'node with level > 1'
                                    ' does not have two children at'
                                    ' %s' % str(node.key))
                _check_properties(node.left, node, parent)
                _check_properties(node.right, node, parent)
        try:
            _check_properties(tree._root, None, None)
        except AATreeException as e:
            if dump:
                print('')
                tree.dump()
            self.fail(str(e) + " - see tree dump")

    def test_update(self):
        d = test_items_seq()
        tree = AnderssonTree()
        tree.update(d)
        self.assertEqual(len(tree), len(d))
        self.assertEqual(set(tree.keys()), set(x[0] for x in d))
        self.assertEqual(set(tree.values()), set(x[1] for x in d))
        self.check_aatree_properties(tree)

    def test_root(self):
        x = [5, 6, 4]
        tree = AnderssonTree(zip(x, x))
        self.assertEqual(tree.root().key, 5)

    def test_insert(self):
        s = test_items_seq()
        tree = AnderssonTree()
        size = len(tree)
        keys = [x[0] for x in s]
        keyset = set()
        shuffle(keys)
        for k in keys:
            keyset.add(k)
            tree.insert(k, k)
            size += 1
            self.assertEqual(len(tree), size)
            self.assertEqual(set(tree.keys()), keyset)
            self.check_aatree_properties(tree)

    def test_clear(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        self.check_aatree_properties(tree)
        tree.clear()
        self.assertEqual(len(tree), 0)

    def test_get(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        self.check_aatree_properties(tree)
        keys = [x[0] for x in s]
        shuffle(keys)
        for k in keys:
            self.assertEqual(tree.get(k), k)
            self.assertEqual(tree[k], k)
        max_ = max(keys)
        self.assertEqual(tree[max_ + 1], None)

    def test_setitem(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        self.check_aatree_properties(tree)
        keys = [x[0] for x in s]
        shuffle(keys)
        for k in keys:
            val = k * 10
            tree[k] = val
            self.assertEqual(tree.get(k), val)

    def test_contains(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        self.check_aatree_properties(tree)
        keys = [x[0] for x in s]
        shuffle(keys)
        for k in keys:
            self.assertTrue(k in tree)
        self.assertFalse(max(keys) + 10 in tree)

    def test_is_empty(self):
        s = test_items_seq()
        tree = AnderssonTree()
        self.assertTrue(tree.is_empty())
        tree.update(s)
        self.assertFalse(tree.is_empty())
        tree.clear()
        self.assertTrue(tree.is_empty())

    def test_keys(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        keys = set(x[0] for x in s)
        self.assertEqual(set(tree.keys()), keys)

    def test_values(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        values = set(x[1] for x in s)
        self.assertEqual(set(tree.values()), values)

    def test_reversed(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        keys = list(reversed([x[0] for x in s]))
        self.assertEqual(list(reversed(tree)), keys)

    def test_copy(self):
        s = test_items_seq()
        tree1 = AnderssonTree(s)
        tree2 = tree1.copy()
        self.assertEqual(len(tree1), len(tree2))
        self.assertEqual(repr(tree1), repr(tree2))

    def test_repr(self):
        s = [test_items_seq()]
        keys = [x[0] for x in s]
        shuffle(keys)
        s = zip(keys, keys)
        tree = AnderssonTree(s)
        gen = ("(%r, %r)" % (x, x) for x in keys)
        spam = ", ".join(gen)
        spam = "%s([%s])" % (tree.__class__.__name__, spam)
        self.assertEqual(repr(tree), spam)

    def test_iter_items(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        items = [x for x in tree.iter_items()]
        self.assertEqual(items, sorted(s))

    def test_iter_items_reversed(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        items = [x for x in tree.iter_items(reverse=True)]
        self.assertEqual(items, sorted(s, reverse=True))

    def test_traverse(self):
        s = test_items_seq()
        tree = AnderssonTree(s)
        visited = set()

        def visit(node):
            visited.add(node.key)

        tree.traverse(visit)
        keys = set([x[0] for x in s])
        self.assertEqual(keys, visited)

    def test_remove(self):
        for i in range(10):
            s = test_items_seq(100)
            tree = AnderssonTree(s)
            self.check_aatree_properties(tree)
            size = len(tree)
            keys = [x[0] for x in s]
            keyset = set(keys)
            shuffle(keys)
            for k in keys:
                keyset.remove(k)
                tree.remove(k)
                size -= 1
                self.assertEqual(len(tree), size)
                self.assertEqual(set(tree.keys()), keyset)
                self.check_aatree_properties(tree, dump=False)

    def test_remove_root(self):
        s = test_items_seq(1000)
        tree = AnderssonTree(s)
        self.check_aatree_properties(tree)
        size = len(tree)
        keys = [x[0] for x in s]
        keyset = set(keys)
        while len(keyset) > 0:
            k = tree.root().key
            keyset.remove(k)
            tree.remove(k)
            size -= 1
            self.assertEqual(len(tree), size)
            self.assertEqual(set(tree.keys()), keyset)
            self.check_aatree_properties(tree)


if __name__ == '__main__':
    unittest.main()
