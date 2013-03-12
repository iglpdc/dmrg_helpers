#
# File: test_reader.py
# Author: Ivan Gonzalez
#
""" A tests for the reader class
"""
from dmrg_helpers.core.reader import FileReader
    
class TestFileReader(object):

    def setUp(self):
        self.reader = FileReader()

    def test_empty_file(self):
        self.reader.read('tests/empty.dat')
        assert self.reader.data == []
        assert self.reader.meta == {}
        assert self.reader.comments == []

    def test_only_comments_file(self):
        self.reader.read('tests/only_comments.dat')
        assert self.reader.data == []
        assert self.reader.meta == {}
        assert self.reader.comments == ['# This is a file with comments\n', 
            '#\n', '#\n']

    def test_only_whitespace_file(self):
        self.reader.read('tests/only_whitespace.dat')
        assert self.reader.data == []
        assert self.reader.meta == {}
        assert self.reader.comments == []

    def test_file_ok(self):
        self.reader.read('tests/file_ok.dat')
        assert self.reader.data == [['n_up_0', 1.0], ['n_up_1', 2.0]]
        assert self.reader.meta['parameter_1'] == '1.0'
        assert self.reader.meta['parameter_2'] == 'a_string'
        assert self.reader.comments == ['#\n',  '# Some comments\n', '# META parameter_1 1.0\n', '# META parameter_2 a_string\n', '#\n']
