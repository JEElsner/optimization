from typing import Collection, Iterable, Set, Tuple, Dict
from .graph import Edge, AbstractGraph, GraphRepresentation, V, DirectedGraph

class AdjacencySet(GraphRepresentation[V]):
    def __init__(self, neighbor_dict: Dict[V, Set[V]]):

        if not isinstance(self, DirectedGraph):
            for v1, neighbors in neighbor_dict.items():
                for v2 in neighbors:
                    neighbor_dict.setdefault(v2, set()).add(v1)

        self.neighbor_dict = neighbor_dict

    @property
    def vertices(self) -> Iterable[V]:
        return self.neighbor_dict.keys()

    @property
    def edges(self) -> Set[Edge[V]]:
        edges: Set[Edge[V]] = set()

        for v1, neighbors in self.neighbor_dict.items():
            edges.update({Edge(v1, v2) for v2 in neighbors})

        return edges


    def is_adjacent(self, v1: V, v2: V) -> bool:
        if v1 not in self.neighbor_dict.keys():
            raise ValueError(f'v1: {v1!r} not in vertices')

        if v2 not in self.neighbor_dict.keys():
            raise ValueError(f'v2: {v2!r} not in vertices')

        return v2 in self.neighbor_dict[v1]

    def neighbors_of(self, v: V) -> Set[V]:
        res = self.neighbor_dict.get(v, None)
        
        if res is None:
            raise ValueError(f"{v} not a vertex in graph")
        
        return res

    def add_vertex(self, v: V):
        self.neighbor_dict.setdefault(v, set())

    def remove_vertex(self, v: V):
        self.neighbor_dict.pop(v)
        
        for v1, neighbors in self.neighbor_dict.items():
            neighbors.discard(v)

    def add_edge(self, v1: V, v2: V, weight=None):
        if v1 not in self.neighbor_dict.keys():
            raise ValueError(f"edge[0]: {v1!r} not in vertices")
        if v2 not in self.neighbor_dict.keys():
            raise ValueError(f"edge[1]: {v2!r} not in vertices")
        
        self.neighbor_dict[v1].add(v2)

        if not isinstance(self, DirectedGraph):
            self.neighbor_dict[v2].add(v1)

    def remove_edge(self, edge: Edge):
        self.neighbor_dict[edge[0]].remove(edge[1])
        
        if not isinstance(self, DirectedGraph):
            self.neighbor_dict[edge[1]].remove(edge[0])

    @property
    def vertex_count(self) -> int:
        return len(self.neighbor_dict.keys())

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @classmethod
    def from_vertices_and_edges(cls, vertices: Collection[V], edges: Collection[Edge[V]]) -> AbstractGraph[V]:
        d = {v: set() for v in vertices}
        for edge in edges:
            d.setdefault(edge[0], set()).add(edge[1])

        return cls(d)

    @classmethod
    def _empty_graph(cls) -> AbstractGraph[V]:
        return cls(dict())

    def to_char_string(self) -> str:
        raise NotImplementedError