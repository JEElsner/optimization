import pytest

from optimization.graph import Edge, Graph, NaiveGraph, AdjacencySet, IncidenceMatrix

@pytest.fixture(params=[NaiveGraph, AdjacencySet, IncidenceMatrix])
def any_graph(request) -> type:
    return request.param

@pytest.fixture
def empty_graph(any_graph) -> Graph:
    return any_graph._empty_graph()

@pytest.fixture
def square_graph(any_graph, vertices, edges):
    return any_graph.from_vertices_and_edges(vertices, edges)

@pytest.fixture
def vertices():
    return ["a", "b", "c", "d"]

@pytest.fixture
def edges(vertices):
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
    
def test_from_edges(any_graph, vertices, edges):
    g = any_graph.from_edges(edges)
    assert set(g.vertices) == set(vertices)
    assert set(g.edges) == set(edges)
    
def test_from_str(any_graph, vertices, edges):
    g = any_graph.from_str("a-b b-c c-d d-a")
    assert set(g.vertices) == set(vertices)
    assert set(g.edges) == set(edges)

def test_is_adjacent(square_graph: Graph):
    assert square_graph.is_adjacent("a", "b")
    assert not square_graph.is_adjacent("a", "c")
    
    with pytest.raises(ValueError):
        square_graph.is_adjacent("foobar", "b")
        square_graph.is_adjacent("a", "foobar")
    
def test_neighbors_of(square_graph: Graph):
    assert square_graph.neighbors_of("a") == {"b", "d"}
    
    with pytest.raises(ValueError):
        square_graph.neighbors_of("foobar")

def test_num_vertices(square_graph: Graph):
    assert square_graph.vertex_count == 4

def test_num_edges(square_graph: Graph):
    assert square_graph.edge_count == 4