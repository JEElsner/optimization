from __future__ import annotations

from typing import TypeVar, Generic, Collection, Tuple, Set

from abc import ABCMeta, abstractmethod

V = TypeVar('V')

class Graph(Generic[V], metaclass=ABCMeta):
    @abstractmethod
    def is_adjacent(self, v1: V, v2: V) -> bool:
        """Returns true if v1 and v2 are adjacent.
        
        If the graph is directed, this is true only if v2 is accessible from v1.
        """
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
    def add_edge(self, edge: Tuple[V, V]):
        """Add an edge to the graph.

        Raises a ValueError if either vertex of the edge is not present in the graph.
        """
        pass

    @abstractmethod
    def remove_edge(self, edge: Tuple[V, V]):
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
    def from_vertices_and_edges(cls, vertices: Collection[V], edges: Collection[Tuple[V, V]]) -> Graph[V]:
        """Construct a graph from a collection of vertices and a collection of edges.
        
        Args:
            vertices: A collection of vertex objects.
            edges: A collection of 2-tuples whose elements are the vertices connected by each edge
        """
        pass

    @classmethod
    def from_edges(cls, edges: Collection[Tuple[V, V]]) -> Graph[V]:
        """Construct a graph from a collection of 2-tuple edges consisting of the two connected vertices by each edge."""
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
        """Returns an empty graph."""
        # Necessary for constructors to return empty graphs of different representations
        pass

    @abstractmethod
    def to_char_string(self) -> str:
        pass
