About estimators.dat files
==========================

In our DMRG code, all the correlation functions calculated in a run 
go to a file, whose name is defaulted to 'estimators.dat'. The format of this
file is important for all the scripts in this package to work. You only need to
read this if you what to use this code to process the output of other code
that spits correlators in a different way from our DMRG code 

The estimators file are text files. They can have two types of lines: comments
or data lines. Comments are lines starting by the `#` symbol. In general,
comments are disregarded by this package, so you can put there whatever you
want. Nevertheless, there is a special type of comment that contains some data
that may be used in the analysis, but is not actual correlator data, such as
the Hamiltonian parameters used to obtain the correlators in the file. These
special type of comments are called metadata lines. A comment is a metadata
line if the first non-blank characters after the `#` symbol are 'META',
followed by a blank space. Metadata lines are treated in the following way. The
next two words after the 'META' keyword are read into a dictionary: the first
one becomes the dictionary's entry key, the second one the dictionary's entry
value. Both words are treated like Python strings.

An example of metadata comment, which is used to specify the system length is:
::

    $ cat estimators.dat
    ...
    # A comment line
    # META L 24
    # More comments
    ...

All comment lines, including metadata lines, are optional, so a file without
them can be still processed. It may be, though, that some features are not
avaliable.

Data lines have two words separated by blank spaces. The first word is read as
a string and specifies the name of the correlator. The name of the correlator
is given by the name and site of each of the single-site operators that make it
up, separated by the `*` symbol. Single-site operator names and sites are
separated by underscores. Single-site operator names contain no numbers.
Single-site operator sites are integer numbers. The second word is read as a
string, but it has to be able to be transformed to a double; it's the value of
the correlator.
