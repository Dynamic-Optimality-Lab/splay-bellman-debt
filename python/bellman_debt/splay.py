"""Exact BST + ordinary bottom-up Splay, independent v0.2 implementation.

Contract: keys [n]={1..n}; root depth 0; cost c(T,x)=depth+1;
five splay cases ZIG/LL/RR/LR/RL; canonical tree encoding inherited
from parent shapes (tuple grammar). No parent code imported.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


class Node:
    __slots__ = ("key", "left", "right", "parent")

    def __init__(self, key: int):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


def build_tree(shape: tuple, keys: list) -> Node | None:
    # shape: nested tuple (left, right) with None leaves; keys inorder
    it = iter(keys)

    def rec(s):
        if s is None:
            return None
        left, right = s
        node = Node(next(it))
        node.left = rec(left)
        if node.left is not None:
            node.left.parent = node
        node.right = rec(right)
        if node.right is not None:
            node.right.parent = node
        return node

    return rec(shape)


def shapes(n: int) -> list:
    # All BST shapes with n nodes as nested tuples; None = empty.
    if n == 0:
        return [None]
    out = []
    for l in range(n):
        r = n - 1 - l
        for ls in shapes(l):
            for rs in shapes(r):
                out.append((ls, rs))
    return out


def enumerate_trees(n: int) -> list:
    # Canonical order: ASCII sort of serialized shape; tree_id = index.
    all_shapes = shapes(n)
    ser = sorted(serialize_shape(s) for s in all_shapes)
    result = []
    for tid, ss in enumerate(ser):
        shape = parse_shape(ss)
        keys = list(range(1, n + 1))
        # inorder assignment by subtree sizes
        assign(shape, keys)
        result.append({"tree_id": tid, "shape": ss})
    return result


def serialize_shape(s) -> str:
    if s is None:
        return "."
    return "(" + serialize_shape(s[0]) + serialize_shape(s[1]) + ")"


def parse_shape(ss: str):
    pos = [0]

    def rec():
        if ss[pos[0]] == ".":
            pos[0] += 1
            return None
        assert ss[pos[0]] == "("
        pos[0] += 1
        left = rec()
        right = rec()
        assert ss[pos[0]] == ")"
        pos[0] += 1
        return (left, right)

    return rec()


def _size(s) -> int:
    if s is None:
        return 0
    return 1 + _size(s[0]) + _size(s[1])


def assign(shape, keys: list) -> dict:
    # Returns {key: (shape-node path)} via inorder rank; implemented on
    # mutable tree objects for splay computation.
    mapping: dict = {}

    def rec(s, key_iter):
        if s is None:
            return None
        left = rec(s[0], key_iter)
        key = next(key_iter)
        right = rec(s[1], key_iter)
        node = Node(key)
        node.left = left
        if left is not None:
            left.parent = node
        node.right = right
        if right is not None:
            right.parent = node
        mapping[key] = node
        return node

    root = rec(shape, iter(keys))
    return {"root": root, "nodes": mapping}


def find_path(root: Node | None, x: int) -> list[Node]:
    path = []
    cur = root
    while cur is not None:
        path.append(cur)
        if x == cur.key:
            return path
        cur = cur.left if x < cur.key else cur.right
    raise KeyError(f"key {x} not found")


def depth_of(root: Node | None, x: int) -> int:
    return len(find_path(root, x)) - 1


def _rotate_right(root: Node, v: Node) -> Node:
    p = v.parent
    if p is None or p.left is not v:
        raise ValueError("bad right rotation")
    g = p.parent
    b = v.right
    v.right = p
    p.parent = v
    p.left = b
    if b is not None:
        b.parent = p
    v.parent = g
    if g is not None:
        if g.left is p:
            g.left = v
        else:
            g.right = v
    return v if g is None else root


def _rotate_left(root: Node, v: Node) -> Node:
    p = v.parent
    if p is None or p.right is not v:
        raise ValueError("bad left rotation")
    g = p.parent
    b = v.left
    v.left = p
    p.parent = v
    p.right = b
    if b is not None:
        b.parent = p
    v.parent = g
    if g is not None:
        if g.left is p:
            g.left = v
        else:
            g.right = v
    return v if g is None else root


def splay(root: Node, x: int) -> tuple[Node, list[str]]:
    # Ordinary bottom-up splay; returns (new_root, case_list).
    cases: list[str] = []
    nodes = {}
    cur = root
    while cur is not None:
        nodes[cur.key] = cur
        cur = cur.left if x < cur.key else (cur.right if x > cur.key else None)
    v = nodes[x]
    while v.parent is not None:
        p = v.parent
        g = p.parent
        if g is None:
            if p.left is v:
                root = _rotate_right(root, v)
            else:
                root = _rotate_left(root, v)
            cases.append("ZIG")
        elif g.left is p and p.left is v:
            root = _rotate_right(root, p)
            root = _rotate_right(root, v)
            cases.append("LL")
        elif g.right is p and p.right is v:
            root = _rotate_left(root, p)
            root = _rotate_left(root, v)
            cases.append("RR")
        elif g.left is p and p.right is v:
            root = _rotate_left(root, v)
            root = _rotate_right(root, v)
            cases.append("LR")
        else:
            root = _rotate_right(root, v)
            root = _rotate_left(root, v)
            cases.append("RL")
    return root, cases


def tree_to_parent_map(root: Node | None) -> dict:
    out: dict = {}

    def rec(node, parent_key):
        if node is None:
            return
        out[node.key] = parent_key
        rec(node.left, node.key)
        rec(node.right, node.key)

    rec(root, 0)
    return out


def access(tree_shape: tuple, n: int, x: int) -> dict:
    # Single access from canonical labeled tree; returns after-shape key.
    info = assign(tree_shape, list(range(1, n + 1)))
    root = info["root"]
    cost = depth_of(root, x) + 1
    path_keys = [nd.key for nd in find_path(root, x)]
    root2, cases = splay(root, x)
    shape2 = root_to_shape(root2)
    return {"cost": cost, "after_shape": shape2, "path": path_keys, "cases": cases}


def root_to_shape(root: Node | None) -> tuple:
    if root is None:
        return None
    return (root_to_shape(root.left), root_to_shape(root.right))


def single_table(n: int):
    # console.log equivalent [WP2-SPLAY-01]: single table build
    console_log(f"[WP2-SPLAY-01] single table n={n} start")
    trees = enumerate_trees(n)
    shape_to_id = {t["shape"]: t["tree_id"] for t in trees}
    table: dict = {}
    for t in trees:
        shape = parse_shape(t["shape"])
        for x in range(1, n + 1):
            r = access(shape, n, x)
            after_id = shape_to_id[serialize_shape(r["after_shape"])]
            table[(t["tree_id"], x)] = {
                "cost": r["cost"],
                "after": after_id,
                "path": r["path"],
                "cases": r["cases"],
            }
    # console.log equivalent [WP2-SPLAY-02]: single table done
    console_log(f"[WP2-SPLAY-02] single table n={n} done records={len(table)}")
    return {"trees": trees, "table": table}
