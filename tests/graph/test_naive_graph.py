import pytest

from optimization.graph import NaiveGraph

@pytest.fixture
def square_graph():
    return NaiveGraph.from_str("ab bc cd da")

@pytest.fixture
def empty_graph():
    return NaiveGraph(set(), set())

@pytest.fixture
def singleton():
    return NaiveGraph(set("a"), set())

def test_from_str(empty_graph):
    g = NaiveGraph.from_str("a-b b-c c-d d-a")
    assert g.vertices == {"a", "b", "c", "d"}
    assert g.edges == [("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")]

    assert NaiveGraph.from_str("") == empty_graph

@pytest.mark.xfail("not in same order every time")
def test_to_str(square_graph, empty_graph, singleton):
    assert square_graph.to_char_string() == "a-b b-c c-d d-a"
    assert empty_graph.to_char_string() == ""

    assert singleton.to_char_string() == "a"

def test_eq(square_graph):
    # TODO: probably better to make a deep copy
    assert square_graph == square_graph

@pytest.mark.xfail(reason="Vertices not sorted in same way every time")
def test_vertex_indices(square_graph):
    assert square_graph.vertex_indices == {"a": 0, "b": 1, "c": 2, "d": 3}
    
@pytest.mark.xfail(reason="Vertices not sorted in same way every time")
def test_adjacency_matrix(square_graph):
    assert square_graph.adjacency_matrix == False

def test_neighbors(square_graph, singleton):
    assert square_graph.neighbors_of("a") == {"b", "d"}
    assert square_graph.neighbors_of("c") == {"b", "d"}

    assert singleton.neighbors_of("a") == set()
