from os import listdir
from hashlib import sha256
from os.path import isdir
from pathlib import Path
from merkle_tree import MerkleTree


class MerkleDAGNode:

    def __init__(self, filepath : str):
        self.pointers = {}
        self.dirtype = isdir(filepath)
        self.filename = Path(filepath).name
        if not self.dirtype:
            with open(filepath) as f:
                self.content = f.read()
            self.hash = self._hash((self.filename + self.content).encode('utf-8'))
        else:
            self.content = self._iterate_directory_contents(filepath)
            nodes_in_str_array = list(map(lambda x: str(x), self.content))
            if nodes_in_str_array:
                self.hash = self._hash((self.filename + MerkleTree(nodes_in_str_array).root_hash).encode('utf-8'))
            else:
                self.hash = self._hash(self.filename.encode('utf-8'))

    def _hash(self, data : bytes) -> bytes:
        return sha256(data).hexdigest()

    def _iterate_directory_contents(self, directory : str):
        nodes = []
        for f in listdir(directory):
            merkle_dag_node = MerkleDAGNode(directory + '/' + f)
            nodes.append(merkle_dag_node)
            self.pointers[f] = merkle_dag_node
        return nodes

    def __repr__(self):
        return 'MerkleDAGNode: ' + self.hash + ' || ' + self.filename

    def __eq__(self, other):
        if isinstance(other, MerkleDAGNode):
            return self.hash == other.hash
        return False
