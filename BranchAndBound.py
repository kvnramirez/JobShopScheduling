# -*- coding: utf-8 -*-

# pip install anytree
from anytree import Node, RenderTree


def main():
    print("Job Shop Scheduling con Branch and Bound")

    udo = Node("Udo", val=0)
    marc = Node("Marc", parent=udo, val=1)
    lian = Node("Lian", parent=marc, val=2)
    dan = Node("Dan", parent=udo, val=65)
    jet = Node("Jet", parent=dan, val=10)
    jan = Node("Jan", parent=dan, val=12)
    joe = Node("Joe", parent=dan, val=81)

    for pre, fill, node in RenderTree(udo):
        print("%s%s(%s)" % (pre, node.name, node.val))


def findMinCost():
    pass

if __name__ == "__main__":
    main()
