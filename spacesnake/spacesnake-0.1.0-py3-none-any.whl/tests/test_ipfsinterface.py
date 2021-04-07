import pytest

@pytest.fixture
def ipfs_interface():
    from spacesnake import IPFSInterface

    interface = IPFSInterface()

    yield interface


def test_add(tmp_dir, ipfs_interface):
    
    ipfs_interface.add()