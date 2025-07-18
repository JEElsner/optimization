from __future__ import annotations
from typing import Collection, Set, List, Dict, TypeVar, Tuple, Hashable, Self

import numpy as np

from .graph import Edge, AbstractGraph, GraphRepresentation

V = TypeVar('V', bound=Hashable)

class NaiveGraph(GraphRepresentation[V]):
    def __init__(self, vertices: Collection[V], edges: Collection[Edge[V]]):
        self._vertices = set(vertices)
        self._edges = list(edges)

    @property
    def vertices(self) -> Set[V]:
        return self._vertices

    @property
    def edges(self) -> List[Edge[V]]:
        return self._edges # type: ignore
        
    def neighbors_of(self, v: V) -> Set[V]:
        if v not in self._vertices:
            raise ValueError(f"{v!r} not a vertex in graph")
        
        neighbors = set()
        for edge in self._edges:
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
        return len(self._vertices)
    
    @property
    def edge_count(self) -> int:
        return len(self._edges)
        
    @property
    def vertex_indices(self) -> Dict[V, int]:
        d = dict()
        for i, v in enumerate(self._vertices):
            d[v] = i

        return d
    
    @property
    def adjacency_matrix(self) -> np.typing.NDArray:
        matrix = np.zeros((self.vertex_count, self.vertex_count))
        
        for v1, v2 in self._edges:
            matrix[self.vertex_indices[v1], self.vertex_indices[v2]] = 1
            matrix[self.vertex_indices[v2], self.vertex_indices[v1]] = 1

        return matrix
    
    @classmethod
    def from_adjacency_matrix(cls, matrix: np.typing.NDArray) -> NaiveGraph[int]:
        if len(matrix.shape) != 2:
            raise ValueError("Adjacency matrix is not 2D!")
        elif matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Adjacency matrix is not square!")
        
        _vertices = range(matrix.shape[0])
        _edges = list()

        for i in _vertices:
            for j in range(0, i):
                if matrix[i, j]:
                    _edges.append((i, j))
                    
        # TODO: remove ignore type. I have a feeling this will cause an error
        return cls(_vertices, _edges) # type: ignore
    
    def to_char_string(self) -> str:
        """Return a compact string representing the _edges of graphs with
        single-character _vertices that can be read by `from_str`.
        
        Note, neither this method, nor `from_str` complain if _vertices are not
        single characters. These methods are not suitable for arbitrary
        _vertices, but they will still attempt to convert the graphs and a round
        trip will result in malformed graphs.
        
        Returns:
            A string of two-character _edges separated by a single space.
        """
        
        return " ".join(f"{v1}{v2}" for v1, v2 in self._edges)

        return s
    
    def __eq__(self, value) -> bool:
        if not isinstance(value, self.__class__):
            return False
        
        # TODO: this does not account for _edges being out of order
        return self.__dict__ == value.__dict__

    @classmethod
    def from_vertices_and_edges(cls, vertices: Collection[V], edges: Collection[Edge[V]]) -> NaiveGraph[V]:
        return cls(vertices, edges)

    @classmethod
    def _empty_graph(cls) -> NaiveGraph[V]:
        return cls(set(), set())

    def is_adjacent(self, v1: V, v2: V) -> bool:
        if v1 not in self.vertices:
            raise ValueError(f'v1: {v1!r} not in vertices')

        if v2 not in self.vertices:
            raise ValueError(f'v2: {v2!r} not in vertices')

        # TODO deal with other types of edges
        return Edge(v1, v2) in self._edges

    def add_vertex(self, v: V):
        self._vertices.add(v)

    def remove_vertex(self, v: V):
        self._vertices.remove(v)

    def add_edge(self, v1: V, v2: V, weight = None):
        if self.is_adjacent(v1, v2):
            return
        else:
            edge = self.create_edge_from_vertices(v1, v2, weight)
            self._edges.append(edge)

    def remove_edge(self, edge: Edge):
        self._edges.remove(edge)
