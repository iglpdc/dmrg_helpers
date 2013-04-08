"""A module to read input files.
"""
from dmrg_helpers.core.dmrg_exceptions import DMRGException

class InputFileReader(object):
    """A class to read input file data and extract parameter info.
    
    Parameters
    ----------
    watched_keywords: a list of strings (default to None).
        The list of keywords (i.e. parameter names) you want to extract from
        the file.
    data: a dictionary of strings to strings or string lists.
        The name of the parameters as key and its value as value.
    open_keywords: a stack with the keywords whose value has not been read yet.

    Examples
    --------
    >>> from dmrg_helpers.extract.input_file_reader import InputFileReader
    >>> from tempfile import NamedTemporaryFile
    >>> f = NamedTemporaryFile()
    >>> f.writelines(['<param>', '1.0', '</param>'])
    >>> reader = InputFileReader('param')
    >>> xml_data = reader.read(f.name)
    >>> xml_data['param']
    '1.0'
    >>> f.close()
    """
    def __init__(self, watched_keywords):
        super(InputFileReader, self).__init__()
        self.watched_keywords = watched_keywords
        self.data = {}
        self.open_keywords = []

    @classmethod
    def get_keyword(cls, line):
        """Strips the XML stuff for the line and gets the parameter name.
        """
        word = line.strip()[1:-2]
        if word.startswith("/"):
            word = word[1:]
        return word

    def close_keyword(self, line):
        """Closes a keyword.
        """
        keyword = self.open_keywords.pop()
        if keyword != InputFileReader.get_keyword(line):
            raise DMRGException("Bad input file")

    def open_keyword(self, line):
        """Opens a keyword.
        """
        return self.open_keyword[-1]

    def set_value(self, keyword, value):
        """Sets a value for an open keyword.
        """
        value = value.split()
        if len(value) == 1:
            value = value[0]
        self.data[keyword] = value

    def read(self, filename):
        """Reads an input file and extracts the parameters you're watching.
        """
        opened_keyword = ''
        with open(filename, 'r') as f:
            lines = f.read()
        for line in lines:
            line = line.strip() # get blanks off
            if line.startswith("<"):
                if line.startswith("/", 1):
                    self.close_keyword(InputFileReader.get_keyword(line))
                else:
                    opened_keyword = self.open_keyword(
                                         InputFileReader.get_keyword(line))
            else:
                if opened_keyword in self.watched_keywords:
                    self.set_value(opened_keyword, line)

        if self.watched_keywords != self.data.keys():
            raise DMRGException("Missing keyword")
        return self.data
