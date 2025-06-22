from typing import Collection, Set, Tuple, List
import numpy as np

from ..set.sorted_set import SortedSet
from .graph import Graph, V

class IncidenceMatrix(Graph[V]):
    def __init__(self, vertices: List[V], matrix: np.typing.ArrayLike):
        # TODO: maybe make vertices a one-to-one mapping in the future, so that there's no possibility of duplicate vertices
        self._vertices = vertices
        self.matrix = np.array(matrix)
        
    @property
    def vertices(self) -> List[V]:
        return self._vertices
    
    @property
    def edges(self) -> Set[Tuple[V, V]]:
        edges: Set[Tuple[V, V]] = set()

        for j, col in enumerate(self.matrix.T):
            indices = np.where(col)
            edge = (self.vertices[indices[0]], self.vertices[indices[1]])
            edges.add(edge)

        return edges

    def is_adjacent(self, v1: V, v2: V) -> bool:
        return np.any(self.matrix[v1] & self.matrix[v2]) # type: ignore

    def neighbors_of(self, v: V) -> Set[V]:
        # product of incidence matrix and vertex row gives number of connections to each vertex
        neighbors = set(self.matrix @ self.matrix[self.get_vertex_index(v)])
        neighbors.remove(v) # remove self from neighbor list (TODO: removes loops, which we would want to keep)
        return neighbors

    def add_vertex(self, v: V):
        if v != self.matrix.shape[0]:
            raise ValueError(f"Error: next vertex must be the next Veger not already a vertex ({self.vertex_count=})")

        self.matrix = np.pad(self.matrix, ((0, 1), (0, 0)), mode='constant', constant_values='0')

    def remove_vertex(self, v: V):
        idx = self.get_vertex_index(v)
        self.matrix =  np.concat((self.matrix[:idx], self.matrix[idx+1:]))

    def add_edge(self, edge: Tuple[V, V]):
        self.matrix = np.pad(self.matrix, ((0, 0), (0, 1)), mode='constant', constant_values='0')
        self.matrix[self.get_vertex_index(edge[0]), -1] = self.matrix[self.get_vertex_index(edge[1]), -1] = 1

    def remove_edge(self, edge: Tuple[V, V]):
        idx = self.get_edge_index(edge).pop()
        self.matrix =  np.concat((self.matrix[:, :idx], self.matrix[idx+1:]), axis=1)
        
    def get_vertex_index(self, v: V) -> int:
        """Get the incidence matrix row index of the vertex."""
        return self.vertices.index(v)
    
    def get_edge_index(self, edge: Tuple[V, V]) -> Set[int]:
        """Get the incidence matrix column index of the provided edge."""
        return set(np.where(self.matrix[edge[0]] & self.matrix[edge[1]])) # type: ignore

    @property
    def vertex_count(self) -> int:
        return self.matrix.shape[0]

    @property
    def edge_count(self) -> int:
        return self.matrix.shape[1]

    @classmethod
    def from_vertices_and_edges(cls, vertices: Collection[V], edges: Collection[Tuple[V, V]]) -> Graph[V]:
        m = len(vertices)
        n = len(edges)
        
        vertices = list(vertices)

        matrix = np.zeros(shape=(m, n))
        for i, (v1, v2) in enumerate(edges):
            matrix[vertices.index(v1), i] = matrix[vertices.index(v2), i] = 1

        return IncidenceMatrix(vertices, matrix)

    @classmethod
    def _empty_graph(cls) -> Graph[V]:
        return IncidenceMatrix(list(), np.zeros(shape=(0, 0)))

class IntIncidenceMatrix(IncidenceMatrix[int]):
    def __init__(self, matrix: np.typing.ArrayLike):
        matrix = np.array(matrix)
        m = matrix.shape[0]
        vertices = list(range(m))

        super().__init__(vertices, matrix)
    
    def get_vertex_index(self, v: int) -> int:
        # since in this case the vertex is the index itself, this is the identity
        return v