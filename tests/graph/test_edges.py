import pytest

from optimization.graph.graph import Edge, WeightedEdge, DirectedEdge, DirectedWeightedEdge

@pytest.fixture
def v1():
    return "v1"

@pytest.fixture
def v2():
    return "v2"

@pytest.fixture(params=[Edge, WeightedEdge, DirectedEdge, DirectedWeightedEdge])
def any_edge(request, v1, v2):
    params = dict()
    if request.param in [WeightedEdge, DirectedWeightedEdge]:
        params['weight'] = 1
    
    return request.param(v1, v2, **params)

def test_nondirectionality():
    assert Edge("a", "b") == Edge("b", "a")
    assert WeightedEdge("a", "b", 1) == WeightedEdge("b", "a", 1)

def test_tuple_likeness():
    edge = Edge("a", "b")

    assert edge[0] == "a"
    assert edge[1] == "b"

    assert "a" in edge
    assert "b" in edge

def test_directed_edge(v1, v2):
    assert DirectedEdge(v1, v2) != DirectedEdge(v2, v1)
    assert DirectedEdge(v1, v2) == DirectedEdge(v1, v2)

    assert DirectedWeightedEdge(v1, v2, 1) != DirectedWeightedEdge(v2, v1, 1)
    assert DirectedWeightedEdge(v1, v2, 1) == DirectedWeightedEdge(v1, v2, 1)
    
    assert DirectedWeightedEdge(v1, v2, 1) != DirectedWeightedEdge(v1, v2, 2)
    
def test_weighted_edge(v1, v2):
    assert WeightedEdge(v1, v2, 1) == WeightedEdge(v1, v2, 1)
    assert WeightedEdge(v1, v2, 1) == WeightedEdge(v2, v1, 1)
    assert WeightedEdge(v1, v2, 1) != WeightedEdge(v1, v2, 2)
    
    assert WeightedEdge(v1, v2, 1) != WeightedEdge(v1, "v3", 1)
    
def test_hashes(v1, v2):
    # "Two objects that compare equal must also have the same hash value, but the reverse is not necessarily true."
    # i.e. two objects that are not equal do not necessarily have different hash values
    e = Edge(v1, v2)
    oe = Edge(v2, v1)
    assert hash(e) == hash(Edge(v1, v2))
    assert hash(e) == hash(oe)
    
    e = WeightedEdge(v1, v2, 1)
    oe = WeightedEdge(v2, v1, 1)
    assert hash(e) == hash(WeightedEdge(v1, v2, 1))
    assert hash(e) == hash(oe)
    
    assert hash(WeightedEdge(v1, v2, 1)) == hash(WeightedEdge(v1, v2, 1))
    # assert hash(WeightedEdge(v1, v2, 1)) != hash(WeightedEdge(v1, v2, 2))
    
    assert hash(DirectedWeightedEdge(v1, v2, 1)) == hash(DirectedWeightedEdge(v1, v2, 1))
    # assert hash(DirectedWeightedEdge(v1, v2, 1)) != hash(DirectedWeightedEdge(v2, v1, 1))
    # assert hash(DirectedWeightedEdge(v1, v2, 1)) != hash(DirectedWeightedEdge(v1, v2, 2))
    
def test_tuple_equality(any_edge, v1, v2):
    # Assert casted as tuple equal
    assert tuple(any_edge) == (v1, v2)
    
    # Assert edge matches tuple under edge equality
    assert any_edge == (v1, v2)
    
    if not isinstance(any_edge, DirectedEdge):
        assert any_edge == (v2, v1)
        
    def unwrapper(ev1, ev2):
        assert ev1 == v1
        assert ev2 == v2
        
    unwrapper(*any_edge)
    
def test_bad_getitem(any_edge):
    with pytest.raises(IndexError):
        any_edge[3]

def test_eq_not_edge(any_edge):
    assert any_edge != 3
    
@pytest.fixture()
def labeled(v1, v2):
    return Edge(v1, v2, "foo")

@pytest.fixture()
def unlabeled(v1, v2):
    return Edge(v1, v2)

def test_label_equality(labeled, unlabeled):
    assert Edge(v1, v2, "foo") == Edge(v1, v2, "foo")
    assert hash(Edge(v1, v2, "foo")) == hash(Edge(v1, v2, "foo"))

    assert WeightedEdge(v1, v2, 1, "foo") == WeightedEdge(v1, v2, 1, "foo")
    assert hash(WeightedEdge(v1, v2, 1, "foo")) == hash(WeightedEdge(v1, v2, 1, "foo"))

    assert DirectedEdge(v1, v2, "foo") == DirectedEdge(v1, v2, "foo")
    assert hash(DirectedEdge(v1, v2, "foo")) == hash(DirectedEdge(v1, v2, "foo"))

    assert DirectedWeightedEdge(v1, v2, 1, "foo") == DirectedWeightedEdge(v1, v2, 1, "foo")
    assert hash(DirectedWeightedEdge(v1, v2, 1, "foo")) == hash(DirectedWeightedEdge(v1, v2, 1, "foo"))
    
    assert unlabeled != labeled
    # assert hash(unlabeled) == hash(labeled)

@pytest.mark.xfail
def test_to_dict(any_edge, v1, v2):
    d = dict(any_edge)
    assert d["v1"] == v1
    assert d["v2"] == v2

    if isinstance(any_edge, WeightedEdge):
        assert d["weight"] == 1
        
    def unwrapper(dv1, dv2, d_weight = None):
        assert dv1 == v1
        assert dv2 == v2

        if isinstance(any_edge, WeightedEdge):
            assert d_weight == 1

        if isinstance(any_edge, WeightedEdge):
            assert d["weight"] == 1
            
    # unwrapper(**any_edge)
        
    
def test_mro():
    # Not really a test, but I want this to be known
    print("MRO:", DirectedWeightedEdge.mro())
