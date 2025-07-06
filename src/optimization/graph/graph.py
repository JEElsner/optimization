from __future__ import annotations

from typing import TypeVar, Generic, Collection, Tuple, Set, Iterable

import warnings

import re

from abc import ABCMeta, abstractmethod

V = TypeVar('V')
W = TypeVar('W')
G = TypeVar('G', bound=Graph)

class Edge(Generic[V]):
    """Represents an (undirected) edge in a graph.
    
    Subclasses exist for directed and weighted edges.
    """

    def __init__(self, v1: V, v2: V, label: str | None = None):
        self._v1 = v1
        self._v2 = v2
        
        self._label = label
        
    @property
    def v1(self) -> V:
        return self._v1
    
    @property
    def v2(self) -> V:
        return self._v2
       
    def __str__(self) -> str:
        if self._label:
            return self._label
        else:
            return f"{self.v1}-{self.v2}"
        
    def __repr__(self) -> str:
        return f"Edge(v1={self.v1!r}, v2={self.v2!r}, label={self._label!r})"
    
    def __getitem__(self, i) -> V:
        if i == 0:
            return self.v1
        elif i == 1:
            return self.v2
        else:
            # TODO: hypergraph support?
            raise IndexError("Edge does not have more than two vertices")
        
    def __iter__(self):
        return iter((self.v1, self.v2))
    
    def __tuple__(self):
        return (self.v1, self.v2)
            
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        
        if self._label != value._label:
            return False
        
        return (self.v1 == value.v1 and self.v2 == value.v2) or (self.v1 == value.v2 and self.v2 == value.v1)
    
    def __hash__(self) -> int:
        edge_hash = min(hash(self.v1), hash(self.v2))

        return hash((edge_hash, self._label))
    
class WeightedEdge(Generic[V, W], Edge[V]):
    """Represents a weighted edge in a graph."""

    def __init__(self, v1: V, v2: V, weight: W, label: str | None = None):
        super().__init__(v1, v2, label)

        self.weight = weight
        """The weight of the edge."""
        
    def __str__(self) -> str:
        if self._label:
            return f"{self._label}={self.weight}"
        else:
            return f"{self.v1}-({self.weight})-{self.v2}"
        
    def __repr__(self) -> str:
        return f"WeightedEdge(v1={self.v1}, v2={self.v2}, weight={self.weight}, label={self._label})"

    def __eq__(self, value: object) -> bool:
        if super().__eq__(value):
            return self.weight == value.weight # type: ignore
        else:
            return False
        
    def __hash__(self) -> int:
        return hash((super().__hash__(), self.weight))
    
class DirectedEdge(Edge[V]):
    """Represents a directed edge in a graph."""

    def __str__(self) -> str:
        if self._label:
            return self._label
        else:
            return f"{self.v1}>{self.v2}"
        
    def __repr__(self) -> str:
        return f"DirectedEdge(v1={self.v1!r}, v2={self.v2!r}, label={self._label!r})"
            
    def __eq__(self, value: object) -> bool:
        if super().__eq__(value):
            return self.v1 == value.v1 and self.v2 == value.v2 # type: ignore
        else:
            return False
        
    def __hash__(self) -> int:
        return hash((self.v1, self.v2, self._label))
    
class DirectedWeightedEdge(DirectedEdge[V], WeightedEdge[V, W]):
    """Represents a directed and weighted edge in a graph."""

    def __str__(self) -> str:
        if self._label:
            return f"{self._label}={self.weight}"
        else:
            return f"{self.v1}-({self.weight})->{self.v2}"
        
    def __repr__(self) -> str:
        return f"DirectedWeightedEdge(v1={self.v1!r}, v2={self.v2!r}, weight={self.weight}, label={self._label!r})"

class AbstractGraph(Generic[V], metaclass=ABCMeta):
    @abstractmethod
    def is_adjacent(self, v1: V, v2: V) -> bool:
        """Returns true if v1 and v2 are adjacent.
        
        If the graph is directed, this is true only if v2 is accessible from v1.
        """
        pass
    
    @property
    @abstractmethod
    def vertices(self) -> Iterable[V]:
        """Get the vertices in the graph"""
        pass

    @property
    @abstractmethod
    def edges(self) -> Iterable[Edge[V]]:
        """Get the edges in the graph"""
        pass

    @abstractmethod
    def neighbors_of(self, v: V) -> Set[V]:
        """Returns the neighboring vertices of v."""
        pass

    @abstractmethod
    def add_vertex(self, v: V):
        """Add vertex v to the graph"""
        pass
    
    @abstractmethod
    def remove_vertex(self, v: V):
        """Remove vertex v from the graph.
        
        Raises a ValueError if v is not in the graph.
        """
        pass
    
    @abstractmethod
    def add_edge(self, edge: Edge[V]):
        """Add an edge to the graph.

        Raises a ValueError if either vertex of the edge is not present in the graph.
        """
        pass

    @abstractmethod
    def remove_edge(self, edge: Edge[V]):
        """Remove an edge from the graph.

        Raises a ValueError if the edge is not present in the graph.
        """
        pass

    @property
    @abstractmethod
    def vertex_count(self) -> int:
        """Returns the number of vertices in the graph."""
        pass

    @property
    @abstractmethod
    def edge_count(self) -> int:
        """Returns the number of edges in the graph."""
        pass
    
    @classmethod
    @abstractmethod
    def from_vertices_and_edges(cls, vertices: Collection[V], edges: Collection[Edge[V]]) -> AbstractGraph[V]:
        """Construct a graph from a collection of vertices and a collection of edges.
        
        Args:
            vertices: A collection of vertex objects.
            edges: A collection of 2-tuples whose elements are the vertices connected by each edge
        """
        pass

    @classmethod
    def from_edges(cls, edges: Collection[Edge[V]]) -> AbstractGraph[V]:
        """Construct a graph from a collection of 2-tuple edges consisting of the two connected vertices by each edge."""
        vertices = set()
        
        for v1, v2 in edges:
            vertices.update({v1, v2})
            
        return cls.from_vertices_and_edges(vertices, edges)

    @classmethod
    def from_str(cls, s: str) -> AbstractGraph[V]:
        """Read graphs stored in a simple format string.
        
        A string representation of a graph consists of edges and vertices
        separated by whitespace. An edge is represented by two vertices
        separated by either a '-' or a '>' with no whitespace. A '>' indicates
        the directionality of the edge.

        >>> from optimization.graph import NaiveGraph
        >>> NaiveGraph.from_str("a b c d") # A graph with no edges
        >>> NaiveGraph.from_str("a>b b>c c>d d>a") # A directed square graph
        >>> NaiveGraph.from_str("a b b-c c>d")
        
        Args:
            s: A string representation of a graph, described above. 
            
        Returns:
            A graph from the parsed string
        """
        s = s.strip()
        
        vertices = set()
        edges = set()

        for edge_str in s.split():
            splits = re.split("([->])", edge_str)

            if len(splits) == 1:
                vertices.add(splits[0])
            elif len(splits) == 3:
                vertices.update(splits[::2])

                edgetype = Edge
                if splits[1] == ">":
                    edgetype = DirectedEdge
                elif splits[1] == "<":
                    edgetype = DirectedEdge

                    tmp = splits[0]
                    splits[0] = splits[2]
                    splits[2] = tmp

                edges.add(edgetype(*splits[::2])) # type: ignore
            else:
                raise ValueError(f"Malformed edge notation: {edge_str}")
            
        return cls.from_vertices_and_edges(vertices, edges)
            
    
    @classmethod
    @abstractmethod
    def _empty_graph(cls) -> AbstractGraph[V]:
        """Returns an empty graph."""
        # Necessary for constructors to return empty graphs of different representations
        pass

    def to_char_string(self) -> str:
        return " ".join(map(str, self.vertices)) + " " + " ".join(map(lambda e: f"{e[0]}-{e[1]}", self.edges))
    

class GraphRepresentation(AbstractGraph[V]):
    pass

class GraphType(AbstractGraph[V]):
    pass

class WeightedGraph(Generic[V, W], GraphType[V]):
    @abstractmethod
    def get_edge_weight(self, edge: Edge[V] | Tuple[V, V]) -> W:
        """Get the weight associated with the given edge."""
        
        if isinstance(edge, WeightedEdge):
            warnings.warn("Warning: edge is weighted edge (possibly with different weight)")

        pass

    @abstractmethod
    def set_edge_weight(self, edge: Edge[V] | Tuple[V, V], weight: W):

        if isinstance(edge, WeightedEdge):
            warnings.warn("Warning: edge is weighted edge (possibly with different weight)")

        pass

class DirectedGraph(GraphType[V]):
    pass

class DirectedWeightedGraph(DirectedGraph[V], WeightedGraph[V, W]):
    pass

class Graph(GraphType[V], GraphRepresentation[V]):
    @classmethod
    def from_types[G](cls, type_: GraphType[V], repr: GraphRepresentation[V]) -> G: # type: ignore
        pass