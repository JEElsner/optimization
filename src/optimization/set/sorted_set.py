from __future__ import annotations

from typing import Any, TypeVar, Generic, Iterable, Optional, Tuple, Iterator
from collections.abc import Callable, Sequence, MutableSet

T = TypeVar('T')
V = TypeVar('V')

class SortedSet(Generic[T, V], Sequence, MutableSet):
    def __init__(self, values: Iterable[T] = list(), sort_key: Callable[[T], V] = lambda x: x):
        self.items = list()
        self.sort_key = sort_key
        
        for item in values:
            self.add(item)

    def add(self, item: T) -> int:
        do_insert, loc = self._try_insert(item)
        if do_insert:
            self.items.insert(loc, item)

    def remove(self, element: Any) -> None:
        try:
            idx = self.index(element)
        except ValueError:
            raise KeyError(f'{element} does not exist in {self}')

        del self.items[idx]
        
    def discard(self, element: Any) -> None:
        try:
            idx = self.index(element)
        except ValueError:
            return
        
        del self.items[idx]
    
    def _try_insert(self, item: T) -> Tuple[bool, int]:
        item_val = self.sort_key(item)
        lo, hi = 0, len(self.items)

        while lo != hi:
            mid = (lo + hi) // 2
            mid_val = self.value_at(mid)

            if mid_val < item_val:
                lo = mid + 1
            elif mid_val > item_val:
                hi = mid
            else:
                return (self.items[mid] != item, mid)
            
        return (True, hi)
    
    def index(self, item: T, start=0, stop=-1) -> int:
        if stop == -1:
            stop = len(self.items)

        item_val = self.sort_key(item)

        while start != stop:
            mid = (start + stop) // 2
            mid_val = self.value_at(mid)

            if mid_val < item_val:
                start = mid + 1
            elif mid_val > item_val:
                stop = mid
            elif self.items[mid] == item:
                return mid
            else:
                break

        raise ValueError(f'{item} not in {self}')
    
    def search_value(self, value) -> int:
        lo, hi = 0, len(self.items)

        while lo != hi:
            mid = (lo + hi) // 2
            mid_val = self.value_at(mid)

            if mid_val < value:
                lo = mid + 1
            elif mid_val > value:
                hi = mid
            else:
                return mid

        return hi
        
    
    @property
    def values(self) -> Iterable[V]:
        return map(self.sort_key, self.items)
    
    def value_at(self, idx) -> V:
        return self.sort_key(self.items[idx])
    
    def __contains__(self, item: T) -> bool:
        return item in self.items
    
    def __iter__(self) -> Iterator[T]:
        yield from self.items

    def __len__(self) -> int:
        return len(self.items)
    
    def __length_hint__(self) -> int:
        return self.items.__length_hint__()
    
    def __getitem__(self, idx) -> int:
        return self.items[idx]
    
    def __delitem__(self, idx) -> None:
        del self.items[idx]

    def __reversed__(self, idx) -> Iterator[T]:
        return reversed(self.items)
    
    def isdisjoint(self, s: Iterable[Any], sort_key=lambda x: x) -> bool:
        return set(self.items).isdisjoint(set(s))
        
    def issubset(self, s: Iterable[Any]) -> bool:
        s = set(s)

        for item in self:
            if item not in s:
                return False
        
        return True
    
    def issuperset(self, s: Iterable[Any]) -> bool:
        for item in s:
            if item not in self:
                return False
            
        return True
    
    def union(self, *s: Iterable) -> SortedSet[Any]:
        new_set = self.copy()

        for st in s:
            for item in st:
                new_set.add(item)
                
        return new_set

    def intersection(self, *s: Iterable[Any]) -> SortedSet:
        new_set = SortedSet(sort_key=self.sort_key)

        for item in self:
            for st in map(set, s):
                if item not in st:
                    break
            else: # no break
                new_set.add(item)

        return new_set
    
    def difference(self, *s: Iterable[Any]) -> SortedSet:
        new_set = self.copy()

        for st in s:
            for item in st:
                new_set.discard(item)
                
        return new_set

    def symmetric_difference(self, s: Iterable) -> set:
        return self.union(s).difference(self.intersection(s))
    
    def update(self, *s: Iterable) -> None:
        for st in s:
            for item in st:
                self.add(item)

    def intersection_update(self, *s: Iterable[Any]) -> None:
        # The lazy way
        new_set = self.intersection(*s)
        self.items = new_set.items

    def pop(self) -> Any:
        return self.items.pop()

    def clear(self) -> None:
        self.items.clear()

    def copy(self) -> set:
        new_set = SortedSet(sort_key=self.sort_key)
        new_set.items = self.items.copy()

        return new_set
    
    def __str__(self):
        return f'{{{", ".join(map(str, self.items))}}}'
    
    def __repr__(self):
        return f'{{{", ".join(map(repr, self.items))}}}'
    
    def __set__(self):
        return set(self.items)
