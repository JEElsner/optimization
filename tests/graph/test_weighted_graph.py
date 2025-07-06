import pytest

from collections import namedtuple

VEG = namedtuple('VEG', ['vertices', 'edges', 'graph'])
"""vertices, edges, and graph"""

from optimization.graph.graph import WeightedGraph, WeightedEdge, Graph, AbstractGraph
from optimization.graph import NaiveGraph, AdjacencySet, IncidenceMatrix

@pytest.fixture(params=[NaiveGraph, AdjacencySet, IncidenceMatrix])
def any_graph(request) -> type[AbstractGraph]:
    return Graph.from_types(WeightedGraph, request.param)

@pytest.fixture
def empty_graph(any_graph: type[AbstractGraph]):
    return any_graph._empty_graph()

@pytest.fixture
def square_graph(any_graph: type[AbstractGraph]) -> VEG:
    vertices = ["a", "b", "c", "d"]
    edges = [WeightedEdge(vertices[0], vertices[1], 1),
             WeightedEdge(vertices[1], vertices[2], 2),
             WeightedEdge(vertices[2], vertices[3], 3),
             WeightedEdge(vertices[3], vertices[0], 4)]

    return VEG(vertices, edges, any_graph.from_vertices_and_edges(vertices, edges))

def test_add_edge(square_graph: VEG):
    vertices, edges, graph = square_graph
    graph.add_edge(vertices[0], vertices[2], 5)

    assert WeightedEdge(vertices[0], vertices[2], 5) in graph.edges