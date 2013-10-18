AATree Package
===================

Abstract
========

This package provides Andersson Tree implementation written in pure Python.

Sources of Algorithms
---------------------

    http://en.wikipedia.org/wiki/Andersson_tree
    http://user.it.uu.se/~arnea/abs/simp.html
    http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_andersson.aspx

    Some concepts are inspired by bintrees package at
    http://bitbucket.org/mozman/bintrees, although this implementation does not
    support dict, heap, set compatibility.

Constructor
~~~~~~~~~~~

    * AnderssonTree() -> new empty tree;
    * AnderssonTree(mapping) -> new tree initialized from a mapping (requires only an items() method)
    * AnderssonTree(seq) -> new tree initialized from seq [(k1, v1), (k2, v2), ... (kn, vn)]

Methods
~~~~~~~

    * __contains__(k) -> True if T has a key k, else False
    * __delitem__(y) <==> del T[y]
    * __getitem__(y) <==> T[y]
    * __iter__() <==> iter(T) <==> keys()
    * __len__() <==> len(T)
    * __repr__() <==> repr(T)
    * __reversed__() <==> reversed(T), reversed keys
    * __setitem__(k, v) <==> T[k] = v
    * __copy__() <==> copy()
    * clear() -> None, remove all items from T
    * copy() -> a shallow copy of T, tree structure, i.e. key insertion order is preserved
    * dump([order]) -> None, dumps tree according to order
    * get(k) -> T[k] if k in T, else None
    * insert(k, v) -> None, insert node with key k and value v, replace value if key exists
    * is_empty() -> True if len(T) == 0
    * iter_items([, reverse]) -> generator for (k, v) items of T
    * keys([reverse]) -> generator for keys of T
    * remove(key) -> None, remove item by key
    * remove_items(keys) -> None, remove items by keys
    * root() -> root node
    * traverse(f, [order]) -> visit all nodes of tree according to order and call f(node) for each node
    * update(E) -> None.  Update T from dict/iterable E
    * values([reverse]) -> generator for values of T

Order values
~~~~~~~~~~~~

    * ORDER_INFIX_LEFT_RIGHT - infix order, left child first, then right
    * ORDER_INFIX_RIGHT_LEFT - infix order, right child first, then left
    * ORDER_PREFIX_LEFT_RIGHT - prefix order, left child first, then right
    * ORDER_PREFIX_RIGHT_LEFT - prefix order, right child first, then left
    * ORDER_POSTFIX_LEFT_RIGHT - postfix order, left child first, then right
    * ORDER_POSTFIX_RIGHT_LEFT - postfix order, right child first, then left

Installation
============

from source::

    python setup.py install

or from PyPI::

    pip install anderssontree

Documentation
=============

this README.rst, code itself, docstrings

bintrees can be found on github.com at:

https://github.com/darko-poljak/andersontree

Tested With
===========

Python2.7.5, Python3.3.2

