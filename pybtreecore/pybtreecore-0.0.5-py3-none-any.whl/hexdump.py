from pyheapfile.hexdump import hexdumps


def main():
    import os
    import argparse
    import string

    from pyheapfile.heap import HeapFile, Node

    from pydllfile.dllist import DoubleLinkedListFile, LINK_SIZE

    from pybtreecore.btcore import BTreeCoreFile
    from pybtreecore.conv import Convert
    from pybtreecore import VERSION

    from pybtreecore.btnode import (
        F_LEAF,
        F_KEY,
        F_DATA,
        F_LEFT,
        F_RIGHT,
    )

    FLAGS = [
        (F_LEAF, "X"),
        (F_KEY, "K"),
        (F_DATA, "D"),
        (F_LEFT, "L"),
        (F_RIGHT, "R"),
    ]

    parser = argparse.ArgumentParser(
        prog="hexdump",
        usage="python3 -m pybtreecore.%(prog)s [options]",
        description="dump heapfile b-tree elements",
    )
    parser.add_argument(
        "-v",
        "--version",
        dest="show_version",
        action="store_true",
        help="show version info and exit",
        default=False,
    )
    parser.add_argument(
        "-V",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="show more info",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="file_name",
        action="store",
        help="input file",
        required=True,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-n",
        "--node",
        type=str,
        dest="node_no",
        action="store",
        help="""hex address of node. blanks in a quoted string are ignored.
                address of 0x0 will read the 2nd heap node since a dll element node
                can not be stored in first heap node.
                (default: %(default)s)""",
        default=f"{0:06x}",
    )
    group.add_argument(
        "-l",
        "--link",
        type=str,
        dest="link_no",
        action="store",
        help="""hex address of dll element node. blanks in a quoted string are ignored.
                (default: %(default)s)""",
        default=f"{0:06x}",
    )
    parser.add_argument(
        "-aw",
        "--addess_width",
        type=int,
        dest="addess_width",
        action="store",
        help="hex address width. (default: %(default)s)",
        default=6,
    )
    parser.add_argument(
        "-ls",
        "--link_size",
        type=int,
        dest="link_size",
        action="store",
        help="link size. (default: %(default)s)",
        default=LINK_SIZE,
    )
    parser.add_argument(
        "-r",
        "--relative",
        type=int,
        dest="rel_no",
        action="store",
        help="""relative position of dll element node.
            can be combined with -n or -l option.
            when negative it reads backwards starting from the -n/-l node.
            keep in mind that -n is an address and -r is a position.
            (default: %(default)s)""",
        default="0",
    )
    parser.add_argument(
        "-nav",
        "--navigate",
        type=str,
        dest="navigate",
        action="store",
        help="""combined navigate string such as: 
                {hexnumber[p|l|r]}+, where
                p: parent,
                l: left,
                r: right
                -: prev leaf node in double linked list 
                +: succ leaf node in double linked list
                e.g. "-nav 0l1lpp"
                will navigate node[0].left -> node[1].left -> node.parent -> node.parent
                (will be again the starting node)
            """,
        default="",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        dest="width",
        action="store",
        help="with of data output (default: %(default)s)",
        default=16,
    )
    parser.add_argument(
        "-g",
        "--group",
        type=int,
        dest="group",
        action="store",
        help="group bytes in data output (default: %(default)s)",
        default=1,
    )
    parser.add_argument(
        "-ho",
        "--header_only",
        dest="header_only",
        action="store_false",
        help="prints only header, no data.",
        default=True,
    )

    args = parser.parse_args()

    if args.show_version:
        print("Version:", VERSION)
        return

    fnam = os.path.expanduser(args.file_name)
    node_nr = int(args.node_no.replace(" ", ""), 16)
    link_nr = int(args.link_no.replace(" ", ""), 16)
    rel_no = args.rel_no
    link_size = args.link_size
    header_only = args.header_only
    width = args.width
    addess_width = args.addess_width
    group = args.group
    verbose = args.verbose
    navigate = args.navigate

    hpf = HeapFile(fnam).open()
    btcore = BTreeCoreFile(hpf, link_size=link_size)
    dllfile = btcore.fd

    def calc_node(elem_pos):
        if elem_pos == 0:
            return 0
        return elem_pos - Node.node_size()

    if link_nr == 0:
        node = hpf.read_node(node_nr)
        if node_nr == 0:
            node = hpf.read_next(node)
    else:
        node = Node()
        node.id = calc_node(link_nr)

    node, elem = dllfile.read_from_node(node.id)

    rel_dir_fw = True if rel_no > 0 else False
    rel_no = abs(rel_no)

    while rel_no > 0:
        rel_no -= 1
        prev = calc_node(elem.prev)
        succ = calc_node(elem.succ)
        node_pos = succ if rel_dir_fw else prev
        if verbose:
            print("next", hex(node_pos), "prev", hex(prev), "succ", hex(succ))
        if node_pos > 0:
            node, elem = dllfile.read_from_node(node_pos)
        else:
            node = None
            break

    if node == None:
        print("out of border")
        return

    SEPS = "plr"

    def _navi(nav):
        nav = list(nav)
        while len(nav) > 0:
            idx = ""
            while len(nav) > 0:
                ch = nav.pop(0)
                if ch in string.hexdigits:
                    idx += ch
                    continue
                if len(idx) == 0:
                    yield [0, ch]
                else:
                    yield [int(idx, 16), ch]
                break
        return

    btelem = btcore.read_list(
        node.id + Node.node_size(), conv_key=Convert(), conv_data=Convert()
    )

    for idx, ln in _navi(navigate):
        n = (
            btelem.nodelist[idx]
            if ln
            in [
                "p",
                "l",
                "r",
            ]
            else None
        )
        npos = btelem.nodelist.parent
        if ln == "p":
            pass  # default set already above
        elif ln == "l":
            npos = n.left
        elif ln == "r":
            npos = n.right
        elif ln == "-":
            npos = btelem.elem.prev
        elif ln == "+":
            npos = btelem.elem.succ
        else:
            raise Exception("unknown navigation link", ln)

        if npos <= 0:
            print("out of border")
            return

        if verbose:
            print("navigate", idx, ln, "link", f"0x{npos:0{addess_width}x}")

        btelem = btcore.read_list(npos, conv_key=Convert(), conv_data=Convert())

    print("Node", ":", hex(btelem.node.id), "link", hex(btelem.elem.pos), end=" : ")
    print(
        "prev",
        "/",
        "succ",
        ":",
        hex(btelem.elem.prev),
        "/",
        hex(btelem.elem.succ),
        end=" : ",
    )
    print(
        "Node",
        ":",
        hex(calc_node(btelem.elem.prev)),
        "/",
        hex(calc_node(btelem.elem.succ)),
    )

    parent = btelem.nodelist.parent
    print("parent", hex(parent), "Node", hex(calc_node(parent)))

    def the_flags(flags):
        out = ""
        for fl in FLAGS:
            f, ch = fl
            out += ch if flags & f > 0 else "."
        return out

    print("=" * 7, "left and right is link address use with -l option")
    for idx, n in enumerate(btelem.nodelist):
        print(
            f"{idx:0{addess_width}x} :",
            the_flags(n.flags),
            "l:",
            f"0x{n.left:0{addess_width}x}",
            "r:",
            f"0x{n.right:0{addess_width}x}",
            "k:",
            n.key,
        )
        if header_only and n.data != None:
            hexdumps(
                n.data,
                start_adr=idx,
                width=width,
                group=group,
                addess_width=addess_width,
            )
            if idx < len(btelem.nodelist) - 1:
                print("-" * 7)
    print("=" * 7)

    hpf.close()


if __name__ == "__main__":
    main()
