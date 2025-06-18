from __future__ import annotations

from typing import TypeVar, Generic, Collection, Tuple, Set

import re

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

                # TODO deal with digraphs
                if splits[1] == ">":
                    raise NotImplementedError

                edges.add(tuple(splits[::2]))
            else:
                raise ValueError(f"Malformed edge notation: {edge_str}")
            
        return cls.from_vertices_and_edges(vertices, edges)
            
    
    @classmethod
    @abstractmethod
    def _empty_graph(cls) -> Graph[V]:
        """Returns an empty graph."""
        # Necessary for constructors to return empty graphs of different representations
        pass

    @abstractmethod
    def to_char_string(self) -> str:
        pass
