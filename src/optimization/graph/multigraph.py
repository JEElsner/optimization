from typing import TypeVar, Generic, Collection, Dict

from .graph import AbstractGraph, GraphRepresentation, V

P = TypeVar('P')

class Multigraph(GraphRepresentation[V], Generic[V, P]):
    def __init__(self, vertices: Collection[V]):
        self._vertices = set(vertices)
        self.planes: Dict[P, AbstractGraph[V]] = dict()

    def __getitem__(self, plane: P):
        return self.planes[plane]

    def __setitem__(self, plane: P, graph: AbstractGraph[V]):
        self.planes[plane] = graph