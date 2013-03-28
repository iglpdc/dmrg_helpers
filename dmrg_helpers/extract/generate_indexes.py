'''A generator to create all possible indexes from a pattern.
'''
import re
from dmrg_helpers.core.dmrg_exceptions import DMRGException

class SiteFilter(object):
    """A class to filter out integers according to a pattern.

    You construct this class using a string with some index specification,
    such as `2*i+1` to filter out even numbers, or `1` to get out only index
    labeled by 1.

    You use this class in the generator.

    Attributes
    ----------
    pattern: a regex with the pattern accepted filters should have.
        Basically, filters can have a mute index, 'i', which may be multiplied
        by an integer and can have a positive or negative constant added.

    Example
    -------
    >>> from dmrg_helpers.extract.generate_indexes import SiteFilter
    >>> site_filter = SiteFilter('2*i+1')
    >>> print [site_filter.a, site_filter.i, site_filter.pm, site_filter.b]
    ['2', 'i', '+', '1']
    >>> site_filter = SiteFilter('i-1')
    >>> print [site_filter.a, site_filter.i, site_filter.pm, site_filter.b]
    [None, 'i', '-', '1']
    """

    pattern = r"([0-9]+)?\*?([a-z])?([\+|\-])?([0-9]+)?"

    def __init__(self, string):
        """
        Parameters
        ----------
        string: a string.
            The filter you want to apply to the sites of the chain.
        """
        super(SiteFilter, self).__init__()
        match = re.search(SiteFilter.pattern, string)
        if not match:
            raise DMRGException('Not match in site filter')

        self.a = match.group(1)
        self.i = match.group(2)
        self.pm = match.group(3)
        self.b = match.group(4)

        if self.is_index_not_ok():
            raise DMRGException('Bad expression for site indexes')

    def is_index_not_ok(self):
        """Checks whether an index is right.
        """
        not_ok = (self.pm is None and self.b is not None) or (self.i is None
                and self.pm is not None)
        return not_ok

    def is_constant(self):
        '''Checks whether the expression is just a constant.
        '''
        return self.i is None
        
    def build_index(self, i):
        '''Evaluates the (possible) mute indexes in the filter to 'i'.

        You use this function to generate the integer, which correspond to site
        in the chain, by evaluating the expression for the filter. Evaluating
        the expression for the filter means making the value of the `self.i`,
        if is not None, equal to the argument `i` of this function.

        Parameters
        ----------
        i : an int.
            The value of a mute index.
        Returns
        -------
        result : an int.
            The value of the expression at the mute index.
        '''
        result = None

        if self.is_constant():
            result = int(self.a)
        else:
            result = i
            
            if self.a is not None:
                result *= int(self.a)
            if self.pm == '+':
                result += int(self.b)
            elif self.pm == '-':
                result -= int(self.b)
                
        return result 

def sites_are_ok(sites, number_of_sites):
    '''Checks whether a list of sites can index an estimator.

    The conditions for this is that it fits in the chain, i.e. the largest
    site is smaller than the length of the chain, and that the indexes in the
    list appear ordered in increasing order.

    Parameters
    ----------
    sites: a list of ints.
        The indexes for eah of the single-site operators in the estimator.
    number_of_sites: an int.
        The length of the chain in the main DMRG code.

    Returns
    -------
    a bool with the result.
    '''
    are_sorted = all(sites[i] < sites[i+1] for i in xrange(len(sites)-1))
    return sites[-1] < number_of_sites and are_sorted

def generate_indexes(site_expressions, number_of_sites):
    '''Generates all the possible indexes that can be obtained evaluating the
    `site_expressions`.

    Parameters
    ----------
    site_expressions: a list of strings.
        The expressions that specify the values for each single-site operator
        index in an estimator. E.g. `1`, `2*i+1`.
    number_of_sites: an int.
        The length of the chain in the main DMRG code.

    Example
    -------
    >>> from dmrg_helpers.extract.generate_indexes import generate_indexes
    >>> print generate_indexes('2*i+1', 10)
    [1, 3, 5, 7, 9]
    >>> print generate_indexes('1', 10)
    [1]
    '''
    site_filters = map(SiteFilter, site_expressions)
    are_all_filters_constant = map(SiteFilter.is_constant, site_filters)
    i = 0

    if are_all_filters_constant:
        yield map(SiteFilter.build_index(0), site_filters)
    else:
        sites = map(SiteFilter.build_index(i), site_filters)
        while sites_are_ok(sites, number_of_sites):
            yield sites
            i += 1
