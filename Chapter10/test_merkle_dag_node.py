import unittest
from merkle_dag import MerkleDAGNode


outer_directory = 'sample_directory'
file1 = 'hello.txt'
file2 = 'hello2.txt'
file3 = 'hello3.txt'
inner_directory = 'inner_directory'
inner_file = 'hello4.txt'


class TestMerkleDAGNode(unittest.TestCase):

    def test_file_node(self):
        file_node = MerkleDAGNode(outer_directory + '/' + file1)
        self.assertEqual(file_node.filename, file1)
        self.assertEqual(file_node.hash, '8ced218a323755a7d4969187449177bb2338658c354c7174e21285b579ae2bca')
        self.assertEqual(file_node.content, 'I am a good boy.\n')

    def test_directory_with_single_file_node(self):
        dir_node = MerkleDAGNode(outer_directory + '/' + inner_directory)
        self.assertEqual(dir_node.filename, inner_directory)
        self.assertEqual(dir_node.hash, 'c075280aef64223bd38b1bed1017599852180a37baa0eacce28bb92ac5492eb9')
        content_of_directory = [
            MerkleDAGNode(outer_directory + '/' + inner_directory + '/' + inner_file),
        ]
        self.assertEqual(dir_node.content[0], content_of_directory[0])

    def test_directory_with_multiple_files_and_single_directory_node(self):
        dir_node = MerkleDAGNode(outer_directory)
        self.assertEqual(dir_node.filename, outer_directory)
        self.assertEqual(dir_node.hash, 'ec618189b9de0dae250ab5fa0fd9bf1abc158935c66ff8595446f5f9b929e037')
        content_of_directory = [
            MerkleDAGNode(outer_directory + '/' + file1),
            MerkleDAGNode(outer_directory + '/' + file2),
            MerkleDAGNode(outer_directory + '/' + file3),
            MerkleDAGNode(outer_directory + '/' + inner_directory)
        ]
        self.assertEqual(dir_node.pointers[file1], content_of_directory[0])
        self.assertEqual(dir_node.pointers[file2], content_of_directory[1])
        self.assertEqual(dir_node.pointers[file3], content_of_directory[2])
        self.assertEqual(dir_node.pointers[inner_directory], content_of_directory[3])


if __name__ == '__main__':
    unittest.main()
