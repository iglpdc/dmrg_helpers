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
    #>>> from dmrg_helpers.extract.input_file_reader import InputFileReader
    #>>> # create a temporary input file
    #>>> with open('tmp.xml', 'w') as f:
    #...    f.writelines(['<param>\n', '1.0\n', '</param>'])
    #>>> reader = InputFileReader(['param'])
    #>>> reader.read(f.name)
    #>>> reader.append_data_to_file('estimators_with_data.dat')
    """
    def __init__(self, watched_keywords):
        self.watched_keywords = []
        self.watched_keywords.append(watched_keywords)
        self.data = {}
        self.open_keywords = []

    @classmethod
    def get_keyword(cls, line):
        """Strips the XML stuff for the line and gets the parameter name.
        """
        word = line.strip()[1:-1]
        if word.startswith("/"):
            word = word[1:]
        return word

    def close_keyword(self, keyword):
        """Closes a keyword.
        """
        tmp = self.open_keywords.pop()
        if keyword != tmp:
            raise DMRGException("Bad input file")

    def open_keyword(self, keyword):
        """Opens a keyword.
        """
        self.open_keywords.append(keyword)
        return self.open_keywords[-1]

    def set_value(self, keyword, value):
        """Sets a value for an open keyword.
        """
        value = value.split()
        if len(value) == 1:
            value = value[0]
        self.data[keyword] = value

    def read(self, filename):
        """Reads an input file and extracts the parameters you're watching.

        Examples
        --------
        #>>> from dmrg_helpers.extract.input_file_reader import InputFileReader
        #>>> # create a temporary input file
        #>>> with open('tmp.xml', 'w') as f:
        #...    f.writelines(['<param>\n', '1.0\n', '</param>'])
        #>>> reader = InputFileReader(['param'])
        #>>> reader.read(f.name)
        #>>> reader.data['param']
        #'1.0'
        #>>> import os
        #>>> os.remove('tmp.xml')
        """
        opened_keyword = ''
        with open(filename, 'r') as f:
            lines = f.readlines()
        import pdb; pdb.set_trace()
        for line in lines:
            line = line.strip() # get blanks off
            if line.startswith("<"):
                keyword = InputFileReader.get_keyword(line)
                if line.startswith("/", 1):
                    self.close_keyword(keyword)
                else:
                    opened_keyword = self.open_keyword(keyword)
            else:
                if opened_keyword in self.watched_keywords:
                    self.set_value(opened_keyword, line)

        for k in self.watched_keywords:
            if k not in self.data.keys():
                raise DMRGException("Missing keyword")

    def get_data_as_metadata(self):
        """Get the dictionary with parameters and values as a formatted string.

        The metadata has to follow some format to be read by the FileReader
        class. Specifically, metadata lines start with '# META ', followed by
        the parameter name and value, separated by a whitespace.
        """
        metadata = []
        for k, v in self.data.iteritems():
            metadata.append('# META ' + str(k) + ' ' + str(v))
        return metadata

    def append_data_to_file(self, filename):
        """Appends the data to the file using the proper format for metadata.
        """
        with open(filename, 'a') as f:
            f.write('\n'.join(self.get_data_as_metadata()))

    def prepend_data_to_file(self, filename):
        """Prepends the data to the file using the proper format for metadata.

        This is slower than appending, as you have to read the whole file,
        keep it in memory, rewrite it starting with the metadata and then
        append the old stuff you read.
        """
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        with open(filename, 'w') as f:
            f.write('\n'.join(self.get_data_as_metadata()))
            f.writelines(lines)
