import pytest

from optimization.set.sorted_set import SortedSet

def test_find_insert():
    s = SortedSet(list())
    s.items = [0, 1, 2]

    assert s._try_insert(-1) == (True, 0)
    assert s._try_insert(0) == (False, 0)
    assert s._try_insert(1) == (False, 1)
    assert s._try_insert(2) == (False, 2)
    assert s._try_insert(3) == (True, 3)
    
    assert s._try_insert(0.5) == (True, 1)
    assert s._try_insert(1.5) == (True, 2)

    s = SortedSet(list())
    s.items = [0, 1, 2, 3]
    
    assert s._try_insert(-1) == (True, 0)
    assert s._try_insert(0) == (False, 0)
    assert s._try_insert(1) == (False, 1)
    assert s._try_insert(4) == (True, 4)
    
    assert s._try_insert(0.5) == (True, 1)
    assert s._try_insert(1.5) == (True, 2)
    assert s._try_insert(2.5) == (True, 3)

def test_try_insert_with_tuples():
    s = SortedSet(sort_key=lambda t: t[0])
    s.items = [(1, 2)]

    assert s._try_insert((1, 2)) == (False, 0)
    assert s._try_insert((1, 3)) == (True, 0)

def test_create():
    assert SortedSet([1, 2, 3]).items == [1, 2, 3]
    assert SortedSet([1, 2, 3, 3]).items == [1, 2, 3]
    
def test_iter():
    s = SortedSet([1, 2, 3])
    for i, item in enumerate(s):
        assert item == i + 1

def test_union():
    s = SortedSet([1,2,3])
    a = set([3,4,5,6])
    b = set([2,3,4,7])

    assert s.union(a, b).items == [1,2,3,4,5,6,7]

    s = SortedSet([1,2,3])
    assert s.union(set([0])).items == [0,1,2,3]

    sk = lambda t: t[0]
    s = SortedSet([(1, 2)], sort_key=sk)
    a = set([(3, 4)])
    assert (s | a).items == [(1, 2), (3, 4)]
    
def test_intersection():
    s = SortedSet([1,2,3,4])
    a = set([1,2,3])
    b = set([2,3,4])

    assert s.intersection(a, b).items == [2, 3]
    assert (s & a & b).items == [2, 3]
    
def test_difference():
    s1 = SortedSet([1,2,3])
    s2 = SortedSet([2,3,4])

    assert s1.difference(s2).items == [1]
    assert (s1 - s2).items == [1]

def test_intersection_update():
    s1 = SortedSet([1, 2])
    s2 = SortedSet([2, 3])
    s3 = SortedSet([2, 4])

    s1.intersection_update(s2, s3)

    assert s1.items == [2]

def test_symmetric_difference():
    s1 = SortedSet([1, 2])
    s2 = SortedSet([2, 3])

    assert s1.symmetric_difference(s2).items == [1, 3]
    assert (s1 ^ s2).items == [1, 3]