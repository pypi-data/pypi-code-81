import uuid

from pyheapfile.heap import HeapFile, to_bytes, from_bytes
from pydllfile.dllist import DoubleLinkedListFile, LINK_SIZE
from pybtreecore.btnode import Node
from pybtreecore.btnodelist import NodeList

KEYS_PER_NODE = 16

KEY_SIZE = 32
DATA_SIZE = 32


def newid():
    return uuid.uuid4().hex


class BTreeElement(object):
    def __init__(self, node, elem, nodelist):
        self.node = node
        self.elem = elem
        self.nodelist = nodelist

    def __repr__(self):
        return (
            self.__class__.__name__
            + "( "
            # + str(self.node)
            + str(self.elem)
            + ", "
            + str(self.nodelist)
        )


class BTreeCoreFile(object):
    def __init__(
        self,
        heap_fd,
        keys_per_node=KEYS_PER_NODE,
        key_size=KEY_SIZE,
        data_size=DATA_SIZE,
        link_size=LINK_SIZE,
    ):

        self.keys_per_node = keys_per_node
        self.key_size = key_size
        self.data_size = data_size

        self.alloc_max_size = self._calc_empty()

        self.heap_fd = heap_fd
        self.fd = DoubleLinkedListFile(heap_fd=self.heap_fd, link_size=link_size)

    def _calc_empty_list(self, leaf=True, set_right=True):
        """this calculates more space than required by default since using 2 link pointer"""
        nodelist = NodeList()
        node = Node()
        node.set_key("".join([" " for i in range(0, self.key_size)]))
        if leaf == True:
            node.set_data("".join([" " for i in range(0, self.data_size)]))
        else:
            node.set_left(1)
            if set_right:
                node.set_right(2)
        # this nodelist is not written to heap
        # just created to get the max size on heap
        [nodelist.insert(node) for i in range(0, self.keys_per_node)]
        buf = nodelist.to_bytes()
        alloc_size = len(buf)
        return alloc_size

    def _calc_empty(self):
        size_leaf = self._calc_empty_list(leaf=True)
        size_inner = self._calc_empty_list(leaf=False)
        return max(size_leaf, size_inner)

    def create_empty_list(self, max_data_alloc=None):
        if max_data_alloc == None:
            max_data_alloc = self.alloc_max_size
        node, elem, other_elem = self.fd.insert_elem(max_data_alloc=max_data_alloc)
        return BTreeElement(node, elem, NodeList())

    def read_list(self, pos, conv_key=None, conv_data=None, free_unused=True):
        node, elem = self.fd.read_elem(pos)
        nodelist = NodeList()
        if elem.data != None and len(elem.data) > 0:
            nodelist.from_bytes(elem.data, conv_key=conv_key, conv_data=conv_data)
        if free_unused == True:
            elem.data = None
        return BTreeElement(node, elem, nodelist)

    def write_list(self, bt_elem, conv_key=None, conv_data=None, free_unused=True):
        bt_elem.elem.data = bt_elem.nodelist.to_bytes(
            conv_key=conv_key, conv_data=conv_data
        )
        self.fd.write_elem(bt_elem.node, bt_elem.elem)
        if free_unused == True:
            bt_elem.elem.data = None
