from typing import Collection, Set, Tuple, List
import numpy as np

from .graph import AbstractGraph, GraphRepresentation, Edge, V

class IncidenceMatrix(GraphRepresentation[V]):
    def __init__(self, vertices: List[V], matrix: np.typing.ArrayLike):
        # TODO: maybe make vertices a one-to-one mapping in the future, so that there's no possibility of duplicate vertices
        self._vertices = vertices
        self.matrix = np.array(matrix)
        
    @property
    def vertices(self) -> List[V]:
        return self._vertices
    
    @property
    def edges(self) -> Set[Edge[V]]:
        edges: Set[Edge[V]] = set()

        for j, col in enumerate(self.matrix.T):
            indices = np.where(col)[0]
            edge = Edge(self.vertices[indices[0]], self.vertices[indices[1]])
            edges.add(edge)

        return edges

    def is_adjacent(self, v1: V, v2: V) -> bool:
        return np.any(self.matrix[self.get_vertex_index(v1)] * self.matrix[self.get_vertex_index(v2)]) # type: ignore

    def neighbors_of(self, v: V) -> Set[V]:
        # product of incidence matrix and vertex row gives number of connections to each vertex
        neighbors = list(np.where(self.matrix @ self.matrix[self.get_vertex_index(v)] >= 1)[0])
        neighbors = set(map(lambda i: self.vertices[i], neighbors))
        neighbors.remove(v) # remove self from neighbor list (TODO: removes loops, which we would want to keep)
        return neighbors

    def add_vertex(self, v: V):
        self._vertices.append(v) # add vertex to vertex list
        
        # extend matrix for new vertex
        self.matrix = np.pad(self.matrix, ((0, 1), (0, 0)), mode='constant', constant_values='0')

    def remove_vertex(self, v: V):
        idx = self.get_vertex_index(v)
        self._vertices.remove(v)
        self.matrix =  np.concat((self.matrix[:idx], self.matrix[idx+1:]))

    def add_edge(self, v1: V, v2: V, weight = None):
        self.matrix = np.pad(self.matrix, ((0, 0), (0, 1)), mode='constant', constant_values='0')
        self.matrix[self.get_vertex_index(v1), -1] = self.matrix[self.get_vertex_index(v2), -1] = 1

    def remove_edge(self, edge: Edge[V]):
        idx = self.get_edge_index(edge).pop()
        self.matrix =  np.concat((self.matrix[:, :idx], self.matrix[:, idx+1:]), axis=1)
        
    def get_vertex_index(self, v: V) -> int:
        """Get the incidence matrix row index of the vertex."""
        return self.vertices.index(v)
    
    def get_edge_index(self, edge: Edge[V]) -> Set[int]:
        """Get the incidence matrix column index of the provided edge."""
        v1 = self.get_vertex_index(edge.v1)
        v2 = self.get_vertex_index(edge.v2)
        return set(np.where(self.matrix[v1] * self.matrix[v2])[0]) # type: ignore

    @property
    def vertex_count(self) -> int:
        return self.matrix.shape[0]

    @property
    def edge_count(self) -> int:
        return self.matrix.shape[1]

    @classmethod
    def from_vertices_and_edges(cls, vertices: Collection[V], edges: Collection[Edge[V]]) -> AbstractGraph[V]:
        m = len(vertices)
        n = len(edges)
        
        vertices = list(vertices)

        matrix = np.zeros(shape=(m, n))
        for i, (v1, v2) in enumerate(edges):
            matrix[vertices.index(v1), i] = matrix[vertices.index(v2), i] = 1

        return cls(vertices, matrix)

    @classmethod
    def _empty_graph(cls) -> AbstractGraph[V]:
        return cls(list(), np.zeros(shape=(0, 0)))

class IntIncidenceMatrix(IncidenceMatrix[int]):
    def __init__(self, matrix: np.typing.ArrayLike):
        matrix = np.array(matrix)
        m = matrix.shape[0]
        vertices = list(range(m))

        super().__init__(vertices, matrix)
    
    def get_vertex_index(self, v: int) -> int:
        # since in this case the vertex is the index itself, this is the identity
        return v