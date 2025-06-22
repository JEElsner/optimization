from typing import TypeVar, Generic, Collection, Dict

from .graph import Graph, V

P = TypeVar('P')

class Multigraph(Graph[V], Generic[V, P]):
    def __init__(self, vertices: Collection[V]):
        self._vertices = set(vertices)
        self.planes: Dict[P, Graph[V]] = dict()

    def __getitem__(self, plane: P):
        return self.planes[plane]

    def __setitem__(self, plane: P, graph: Graph[V]):
        self.planes[plane] = graph