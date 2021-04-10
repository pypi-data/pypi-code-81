from grid.core.base import GridObject


def test_grid_object_update_meta(monkeypatch):
    class TestObject(GridObject):
        def __init__(self):
            # Prevents Grid from instantiating
            self._data = None
            pass

    G = TestObject()
    previous = dir(G)

    G._update_meta()
    not_changed = dir(G)

    assert previous == not_changed

    # Assert dict keys are added as attributes
    G._data = {"test": True}
    G._update_meta()
    changed = dir(G)
    assert previous != changed
    assert G.test
