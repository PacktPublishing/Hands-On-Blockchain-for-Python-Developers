from hashlib import sha256
from typing import List
from math import ceil


class MerkleTree:

    def __init__(self, leaf_nodes : List[str]):
        self.hash_nodes : List[str] = []
        self.leaf_nodes : List[str] = leaf_nodes
        self._turn_leaf_nodes_to_hash_nodes()
        if len(leaf_nodes) < 4:
            self.root_hash = self._hash_list()
        else:
            self.root_hash = self._build_root_hash()

    def _hash_list(self):
        long_node = "".join(self.hash_nodes)
        return self._hash(long_node.encode('utf-8'))

    def _turn_leaf_nodes_to_hash_nodes(self):
        for node in self.leaf_nodes:
            self.hash_nodes.append(self._hash(node.encode('utf-8')))

    def _hash(self, data : bytes) -> bytes:
        return sha256(data).hexdigest()

    def _build_root_hash(self) -> bytes:
        parent_amount = ceil(len(self.hash_nodes) / 2)
        nodes : List[str] = self.hash_nodes

        while parent_amount > 1:
            parents : List[bytes] = []
            i = 0
            while i < len(nodes):
                node1 = nodes[i]
                if i + 1 >= len(nodes):
                    node2 = None
                else:
                    node2 = nodes[i+1]
                parents.append(self._convert_parent_from_two_nodes(node1, node2))
                i += 2
            parent_amount = len(parents)
            nodes = parents

        return parents[0]

    def _convert_parent_from_two_nodes(self, node1 : bytes, node2) -> bytes:
        if node2 == None:
            return self._hash((node1 + node1).encode('utf-8'))
        return self._hash((node1 + node2).encode('utf-8'))


if __name__ == '__main__':
    leaf_nodes = ['cat', 'dog', 'bird', 'whale']
    merkle_tree = MerkleTree(leaf_nodes)
    # ba2b19423245563949658c3f98ebbc337671706e037267a7d95be78dc95f0f31
    print(merkle_tree.root_hash)

    leaf_nodes = ['cat', 'dog', 'bird', 'whale', 'unicorn', 'pegasus', 'elephant', 'mouse']
    merkle_tree = MerkleTree(leaf_nodes)
    # 20a9a6aa60cc29d62189a5a4d2388a272b2a0f249264dd0da3a7eecdfdc044bd
    print(merkle_tree.root_hash)

    leaf_nodes = ['cat', 'dog', 'bird', 'whale', 'unicorn']
    merkle_tree = MerkleTree(leaf_nodes)
    # 6182e4e70b821ecc35d788bb4801f9b26bec75e935129e3fcd66648a5fdd79f4
    print(merkle_tree.root_hash)

    leaf_nodes = ['cat', 'dog', 'bird', 'whale', 'unicorn', 'pegasus', 'elephant']
    merkle_tree = MerkleTree(leaf_nodes)
    # 8149c6504e532f0b03631ab3779f44b4f72edcef7e842120fe2a9198fac8a08e
    print(merkle_tree.root_hash)

    leaf_nodes = ['cat', 'dog']
    merkle_tree = MerkleTree(leaf_nodes)
    # d2cc68f933eebbeb605e65d4fa80ab8a76b87a40fce6fab348431f2f0c199603
    print(merkle_tree.root_hash)
