from unfolded.map_sdk import UnfoldedMap


def test_example_creation_blank() -> None:
    w = UnfoldedMap()
    assert w.value == 'Hello from Jupyter'
