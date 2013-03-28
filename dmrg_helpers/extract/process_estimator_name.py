'''A few functions to check whether the data in the estimator file is fine.
'''

from dmrg_helpers.core.dmrg_exceptions import DMRGException

def process_estimator_name(estimator_name):
    '''Process the name of the estimator and tries to extract the operators and
    sites involved.
    
    Parameters
    ----------
    name: a string
        This is one of the elements of the first columns of the estimators file
        produced by the DMRG code. 

    Returns
    -------
    operators: a n-tuple of strings.
        The single-site operators that form the estimator.
    sites: a n-tuple of ints.
        The sites at which each of the operators above act.
    '''
    operators = estimator_name.split('*')
    operator_names = []
    sites = []

    for operator in operators:
        name, site = split_into_name_and_site(operator)
        operator_names.append(name)
        sites.append(site)
    return (operator_names, sites)

def split_into_name_and_site(operator):
    """Splits an operator into a single-site operator name and site.

    A single site operator is a string with the following format: chars_ints,
    where chars are characters (incl. '_') but no numbers, and ints are [0-9].
    There must be at least a char in chars and number in ints.

    You use this function to separate the chars from the ints.

    Parameters
    ----------
    operator: a string.
        The name of a single site operator.
    
    Returns
    -------
    name: a string 
        The name of the single-site operator.
    site: an int.
        The site where this operator acts.
    """
    splitted = operator.split('_')
    if len(splitted)<2:
        raise DMRGException('Bad operator name')

    site = splitted[-1]
    # the operator name is the whole thing but the site part and the '_' that
    # separates them
    name = operator[:-(len(site)+1)]

    try:
        site = int(site)
    except:
        raise DMRGException('Bad site number')
    
    return name, site
