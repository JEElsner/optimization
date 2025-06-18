from __future__ import annotations
from typing import Collection, Set, List, Dict, Iterable, Any, Generic, TypeVar, Tuple, Hashable

import numpy as np

V = TypeVar('V', bound=Hashable)

class Graph(Generic[V]):
    def __init__(self, vertices: Collection[V], edges: Collection[Tuple[V, V]]):
        self.vertices = set(vertices)
        self.edges = list(edges)
        
    def neighbors_of(self, v: V) -> Set[V]:
        if v not in self.vertices:
            raise ValueError(f"{v!r} not a vertex in graph")
        
        neighbors = set()
        for edge in self.edges:
            if edge[0] == v:
                neighbors.add(edge[1])
            elif edge[1] == v:
                neighbors.add(edge[0])
                
        return neighbors
    
    def breadth_first_search(self, start: V, end: V) -> List[V]:
        raise NotImplementedError()
    
    def depth_first_search(self, start: V, end: V) -> List[V]:
        raise NotImplementedError()
        
    @property
    def vertex_count(self) -> int:
        return len(self.vertices)
    
    @property
    def edge_count(self) -> int:
        return len(self.edges)
        
    @property
    def vertex_indices(self) -> Dict[V, int]:
        d = dict()
        for i, v in enumerate(self.vertices):
            d[v] = i

        return d
    
    @property
    def adjacency_matrix(self) -> np.typing.NDArray:
        matrix = np.zeros((self.vertex_count, self.vertex_count))
        
        for v1, v2 in self.edges:
            matrix[self.vertex_indices[v1], self.vertex_indices[v2]] = 1
            matrix[self.vertex_indices[v2], self.vertex_indices[v1]] = 1

        return matrix
    
    @classmethod
    def from_adjacency_matrix(cls, matrix: np.typing.NDArray) -> Graph[int]:
        if len(matrix.shape) != 2:
            raise ValueError("Adjacency matrix is not 2D!")
        elif matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Adjacency matrix is not square!")
        
        vertices = range(matrix.shape[0])
        edges = list()

        for i in vertices:
            for j in range(0, i):
                if matrix[i, j]:
                    edges.append((i, j))
                    
        return Graph(vertices, edges)
    
    @classmethod
    def from_edges(cls, edges: Collection[Tuple[V, V]]) -> Graph[V]:
        vertices = set()
        
        for v1, v2 in edges:
            vertices.update({v1, v2})
            
        return Graph(vertices, edges)
    
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
            return Graph(set(), set())
        
        edges = [(e[0], e[1]) for e in s.strip().split()]
        return cls.from_edges(edges) # type: ignore

    def to_char_string(self) -> str:
        """Return a compact string representing the edges of graphs with
        single-character vertices that can be read by `from_str`.
        
        Note, neither this method, nor `from_str` complain if vertices are not
        single characters. These methods are not suitable for arbitrary
        vertices, but they will still attempt to convert the graphs and a round
        trip will result in malformed graphs.
        
        Returns:
            A string of two-character edges separated by a single space.
        """
        
        return " ".join(f"{v1}{v2}" for v1, v2 in self.edges)

        return s
    
    def __eq__(self, value) -> bool:
        if not isinstance(value, self.__class__):
            return False
        
        # TODO: this does not account for edges being out of order
        return self.__dict__ == value.__dict__
