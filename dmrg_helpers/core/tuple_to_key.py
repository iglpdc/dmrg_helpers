'''
File: tuple_to_key.py
Author: Ivan Gonzalez
Description: A function to build keys for the database.
'''
def tuple_to_key(t, delimiter=u':'):
    '''Joins the elements of a tuple into a string using delimiter.

    Parameters
    ----------
    t: a tuple 
        You want to join this.
    delimiter: a string
        You want to join usig this as a delimiter.

    Returns
    -------
    a string with the result.

    Example
    -------
    >>> from dmrg_helpers.core.tuple_to_key import tuple_to_key
    >>> tuple = ['a', 'b', 'c']
    >>> print tuple_to_key(tuple)
    'a:b:c'
    '''
    return delimiter.join(t)
