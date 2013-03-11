#
# File: reader.py
# Author: Ivan Gonzalez
#
""" A module to read estimator files.
"""
import os
from dmrg_helpers.core.dmrg_exceptions import DMRGException


def is_empty_line(line):
    """Checks whether a line is empty.
    
    A line is empty is has only whitespace or consists only of a carriage
    return.

    """
    return (line.split == '') or (line in ['\n', '\n\r'])

class FileReader(object):
    """A file reader.

    Reads an estimators.dat file and extracts the data from the estimators
    stored there.

    """
    def __init__(self):
        super(FileReader, self).__init__()
        self.comments = []
        self.data = []
        self.meta = {}

    def read(self, filename):
        """Reads a file and extracts the data.

        Parameters
        ----------
        filename: a string.
            The filename of the estimators file. The file must exist. If you
            pass a relative path it will be made absolute.

        Raises
        ------
        DMRGException: if the file does not exist.
        """
        if os.path.exists(filename):
            filename = os.path.abspath(filename)
        else:
            raise DMRGException('File does not exist')

        self.filename = filename

        with  open(filename, 'r') as f:
            lines = f.readlines()
        for line in lines:
            self.validate_line(line)

    def validate_line(self, line):
        """Checks whether a line is OK, and if so gets its data.

        The estimators file is supposed to have a certain structure. Lines can 
        comments, and therefore its first char is "#", or they have a two-column
        format with the first column being a string with the estimator's name, 
        and the second a double with the estimator's value.

        Empty lines (i.e. having inly whitespaces) are skipped.

        If the line has not this structure this function raises. Otherwise the
        contents of the line are added to the proper field.

        Parameters
        ----------
        line: a string
            A line from the estimators file.
        """
        if self.is_comment(line):
            self.comments.append(line)
        elif is_empty_line(line):
            pass
        else:
            try:
                tmp = self.extract_data_from_line(line)
                self.data.append(tmp)
            except:
                raise DMRGException('Bad line in file')
        self.extract_meta_from_comments()

    def is_comment(self, line):
        """Checks whether a line is a comment

        Parameters
        ----------
        line: a string.
            The line you want to check.

        Returns
        -------
        a bool: whether is a comment or not.
        """
        return line[0] == '#'

    def extract_data_from_line(self, line):
        """Extracts the data from a valid line.
        
        Parameters
        ----------
        line: a string.
            The line you want to extract data from.

        Returns
        -------
        splitted_line: a 2-tuple with a string and a float
            The name of the correlator and its value stored in this line.
        """
        splitted_line = line.split()
        if len(splitted_line) != 2:
            raise DMRGException('Bad line in file')
        try:
            splitted_line[1] = float(splitted_line[1])
        except:
            raise DMRGException('Bad line in file')

        return splitted_line

    def extract_meta_from_comments(self):
        """Extracts metadata from the comments in the estimators file.

        Metadata are comment lines that start with '# META'. They are use to
        store in the file the values of the parameters of the run, for
        example. You use this function to are read and store in a dictionary
        the metadata.
        """
        for c in self.comments:
            splitted_line = c.split()
            if "META" in splitted_line:
                i = splitted_line.index('META')
                splitted_line = splitted_line[i+1:]
                if len(splitted_line) > 2:
                    raise DMRGException('Bad metadata')
                key = splitted_line[0]
                value = splitted_line[1]
                self.meta[key] = value
