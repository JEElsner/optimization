from typing import Collection, Set, Tuple
import numpy as np

from .graph import Graph

class IncidenceMatrix(Graph[int]):
    def __init__(self, matrix: np.typing.ArrayLike):
        self.matrix = np.array(matrix)

    def is_adjacent(self, v1: int, v2: int) -> bool:
        return np.any(self.matrix[v1] & self.matrix[v2]) # type: ignore

    def neighbors_of(self, v: int) -> Set[int]:
        # product of incidence matrix and vertex row gives number of connections to each vertex
        neighbors = set(self.matrix @ self.matrix[v])
        neighbors.remove(v) # remove self from neighbor list (TODO: removes loops, which we would want to keep)
        return neighbors

    def add_vertex(self, v: int):
        if v != self.matrix.shape[0]:
            raise ValueError(f"Error: next vertex must be the next integer not already a vertex ({self.vertex_count=})")

        self.matrix = np.pad(self.matrix, ((0, 1), (0, 0)), mode='constant', constant_values='0')

    def remove_vertex(self, v: int):
        self.matrix =  np.concat((self.matrix[:v], self.matrix[v+1:]))

    def add_edge(self, edge: Tuple[int, int]):
        self.matrix = np.pad(self.matrix, ((0, 0), (0, 1)), mode='constant', constant_values='0')
        self.matrix[edge[0], -1] = self.matrix[edge[1], -1] = 1

    def remove_edge(self, edge: Tuple[int, int]):
        idx = self.get_edge_index(edge).pop()
        self.matrix =  np.concat((self.matrix[:, :idx], self.matrix[idx+1:]), axis=1)
        
    
    def get_edge_index(self, edge: Tuple[int, int]) -> Set[int]:
        return set(np.where(self.matrix[edge[0]] & self.matrix[edge[1]])) # type: ignore

    @property
    def vertex_count(self) -> int:
        return self.matrix.shape[0]

    @property
    def edge_count(self) -> int:
        return self.matrix.shape[1]

    @classmethod
    def from_vertices_and_edges(cls, vertices: Collection[int], edges: Collection[Tuple[int, int]]) -> Graph[int]:
        m = len(vertices)
        n = len(edges)

        matrix = np.zeros(shape=(m, n))
        for i, (v1, v2) in enumerate(edges):
            matrix[v1, i] = matrix[v2, i] = 1

        return IncidenceMatrix(matrix)

    @classmethod
    def _empty_graph(cls) -> Graph[int]:
        return IncidenceMatrix(np.zeros(shape=(0, 0)))

    def to_char_string(self) -> str:
        raise NotImplementedError
