import pytest

from optimization.graph import Edge, Graph, NaiveGraph, AdjacencySet, IncidenceMatrix

@pytest.fixture(params=[NaiveGraph, AdjacencySet, IncidenceMatrix])
def any_graph(request) -> type:
    return request.param

@pytest.fixture
def empty_graph(any_graph) -> Graph:
    return any_graph._empty_graph()

@pytest.fixture
def vertices():
    return {"a", "b", "c", "d"}

@pytest.fixture
def edges(vertices):
    vertices = list(vertices)
    return [Edge(vertices[0], vertices[1]),
            Edge(vertices[1], vertices[2]),
            Edge(vertices[2], vertices[3]),
            Edge(vertices[3], vertices[0]),
            ]

@pytest.fixture
def singleton(any_graph) -> Graph:
    return Graph.from_vertices_and_edges({"a"}, list())

def test_empty_graph(empty_graph: Graph):
    assert set(empty_graph.vertices) == set()
    assert set(empty_graph.edges) == set()

def test_from_vertices_and_edges(any_graph: Graph, vertices, edges):
    g = any_graph.from_vertices_and_edges(vertices, edges)
    assert set(g.vertices) == set(vertices)
    assert set(g.edges) == set(edges)