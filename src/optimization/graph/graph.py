from __future__ import annotations

from typing import TypeVar, Generic, Collection, Tuple, Set

from abc import ABCMeta, abstractmethod

V = TypeVar('V')

class Graph(Generic[V], metaclass=ABCMeta):
    @abstractmethod
    def is_adjacent(self, v1: V, v2: V) -> bool:
        pass

    @abstractmethod
    def neighbors_of(self, v: V) -> Set[V]:
        pass

    @abstractmethod
    def add_vertex(self, v: V):
        pass
    
    @abstractmethod
    def remove_vertex(self, v: V):
        pass
    
    @abstractmethod
    def add_edge(self, edge: Tuple[V, V]):
        pass

    @abstractmethod
    def remove_edge(self, edge: Tuple[V, V]):
        pass

    @property
    @abstractmethod
    def vertex_count(self) -> int:
        pass

    @property
    @abstractmethod
    def edge_count(self) -> int:
        pass
    
    @classmethod
    @abstractmethod
    def from_vertices_and_edges(cls, vertices: Collection[V], edges: Collection[Tuple[V, V]]) -> Graph[V]:
        pass

    @classmethod
    def from_edges(cls, edges: Collection[Tuple[V, V]]) -> Graph[V]:
        vertices = set()
        
        for v1, v2 in edges:
            vertices.update({v1, v2})
            
        return cls.from_vertices_and_edges(vertices, edges)

    @classmethod
    def from_str(cls, s: str) -> Graph[V]:
        """Read graphs stored in a simple format string.
        
        Note, this method WILL NOT COMPLAIN OR ERROR if any edge has more than two characters.
        
        Args:
            s:  A string of edges comprising two non-space characters (typically letters or numbers), each edge separated by whitespace.
            
        Returns:
            A graph from the parsed string
        """
        
        if len(s.strip()) == 0:
            return cls._empty_graph()
        
        edges = [(e[0], e[1]) for e in s.strip().split()]
        return cls.from_edges(edges) # type: ignore
    
    @classmethod
    @abstractmethod
    def _empty_graph(cls) -> Graph[V]:
        pass

    @abstractmethod
    def to_char_string(self) -> str:
        pass
