"""Functions to remove some of the plots.

Usually you have a bunch of plots and you may want to remove some to them to
keep only those separated by a certain distance, so the graph is not
cluttered with tens of lines.
"""
from dmrg_helpers.core.dmrg_logging import logger
import numpy as np
import operator
from itertools import izip, chain
from dmrg_helpers.core.dmrg_exceptions import DMRGException

def get_scaled_up_separations(vert_axis, height):
    """Returns the scaled-up difference between plots across a vertical axis.

    Parameters
    ----------
    vert_axis: dict of strings on floats.
        The keys are strings with the labels of the plot. The values are the y
        value of the plot with this label at the vertical axis, i.e. at a
        particular value of the x coordinate.

    height: a float.
        The height of the plot, i.e. the max minus the min values of y plotted.
        You use this to scale upthe separations such as they are in fractions
        of the height of the plot.

    Returns
    -------
    A dictionary of two-tuples of strings and floats. The key is a two-tuple of
    strings, each element in the tuple corresponds to the labels of two
    consecutive plots in the y-axis. The tuples are ordered in such a way that
    the first element of the tuple is the plot with the smallest value of y
    along this vertical axis. The value is the distance between the two plots
    along the vertical axis. This distance is scaled up such as a value of 1.0
    corresponds to the full height of the plot.

    """
    def get_two_consecutive_iterators(iterable):
        """Returns two iterators from the iterable, one and the next one.

        Example
        -------
        >>> a = [1, 2, 3, 4]
        >>> [i for i in get_two_consecutive_iterators(a)]
        [(1, 2), (2, 3), (3, 4)]

        """
        from itertools import tee
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)

    sorted_keys = [k for (k, v) in 
                   sorted(vert_axis.iteritems(), key = operator.itemgetter(1))]
    key_pairs = get_two_consecutive_iterators(sorted_keys)
    y_vals = np.sort(np.array([v for v in vert_axis.itervalues()]))
    return dict(izip(key_pairs, np.diff(y_vals) / height))

def get_smallest_distance(separation_list):
    """Returns the smallest distance between two plots for all the graphs.
    """
    if not isinstance(separation_list, list):
        raise DMRGException('Need a list')

    return min([min(s.itervalues()) for s in separation_list])

def get_key_to_pop(separation_list, banned):
    """Returns the key for the plot with the smallest separation in the graphs.

    You use this function to pick up the key you want to remove. The key to
    remove is choosen between the two whose plots have the smallest separation
    among all graphs. To choose which of the two, you select the one that is
    closer to any of its neighbors in any plot.

    If the key is among the `banned_keys` is never popped. If the two keys can
    popped (all coincides) the one you passes second is popped (for no reason),
    If the two keys can popped (all coincides) the one you passes second is
    popped (for no reason).

    """
    def get_smallest_separation(d, key):
        """Returns the smallest separation for a key in a given graph.
        """
        if key not in list(chain.from_iterable(d.iterkeys())):
            raise DMRGException('Mising key')

        a = b = None
        for k in d.iterkeys():
            k_1, k_2 = k
            if k_2 == key:
                a = d[k]
            elif k_1 == key:
                b = d[k]

        assert a is not None or b is not None
        
        if a is None:
            return b
        elif b is None:
            return a
        else:
            return a if (a < b) else b

    if not isinstance(separation_list, list):
        raise DMRGException('Need a list')

    key_1, key_2 = get_candidate_keys(separation_list) 

    # Check if the keys are banned.
    intersect = list(set([key_1, key_2]) & set(banned))
    if intersect:
        if len(intersect) == 2:
            raise DMRGException('Two banned keys to choose to pop')
        else: 
            return key_1 if key_2 in intersect else key_2

    key_1_separations = sorted([get_smallest_separation(d, key_1) for d in
                                separation_list])
    key_2_separations = sorted([get_smallest_separation(d, key_2) for d in
                                separation_list])
    return key_1 if key_1_separations < key_2_separations else key_2

def get_candidate_keys(separation_list):
    """Gives the two keys with the smallest separation among all plots.
    """
    if not isinstance(separation_list, list):
        raise DMRGException('Need a list')

    tmp = [min(s.iteritems(), key = lambda (k, v): v) for s in separation_list]
    return min(tmp, key = lambda (k, v): v)[0]

def pop_closest(separation_list, banned):
    """Pops the plot with smallest separation from each element in the list.

    You use this function to pop out a plot from each of the graph you're
    plotting. The plot removed is the same in each of the graphs. You select
    the plot to remove by choosing the plot that is closer to its neighboring
    plots among all the graphs. This means that the graphs have always the same
    plots, i.e. if a label is in one of them is in all. It also means that
    every time you pop a plot the smallest separation between neighboring plots
    increases.

    You actually remove two entries for each dictionary, i.e. the elements of
    the list, as you remove the two elements that involve the plot to be
    removed. But then you insert a new element involving the two unpaired keys
    and whose value is the sum of the values of the elements being removed.

    Parameters
    ----------
    separation_list: a list of dict of pairs of strings on floats.
        For each graph you're plotting, you calculate the separations between
        plots in the graph by using the `get_scaled_up_separations` function.
        The return value of this function has the same type as the elements of
        this list.

    Returns
    -------
    The same list but in which each of the elements, which is a dictionary, has
    one less item. 

    """
    if not isinstance(separation_list, list):
        raise DMRGException('Need a list')

    key = get_key_to_pop(separation_list, banned)
    for sep in separation_list:
        new_key = [None, None]
        new_value = 0.0
        to_pop = []
        for k in sep.iterkeys():
            k_1, k_2 = k
            if k_2 == key:
                new_key[0] = k_1
                new_value += sep[k]
                to_pop.append(k)
            elif k_1 == key:
                new_key[1] = k_2
                new_value += sep[k]
                to_pop.append(k)
        sep[(new_key[0], new_key[1])] = new_value
        for k in to_pop:
            sep.pop(k)
    logger.info('Removing plot with label {}'.format(key))
    return separation_list

def pop_until_separated(separation_list, min_separation, banned):
    """Removes one plot from each graph until there's certain separation.

    The plot removed is the same in all the graphs. 
    """
    if not isinstance(separation_list, list):
        raise DMRGException('Need a list')

    while min_separation > get_smallest_distance(separation_list):
        separation_list = pop_closest(separation_list, banned)
        remaining = [set(list(chain.from_iterable(s.keys())))
                    for s in separation_list]
        assert remaining.count(remaining[0]) == len(remaining)
        if set(banned) == set(remaining[0]):
            break
    return remaining[0], separation_list

def select_keys(vertical_axis_and_heights, min_separation, banned=[]):
    """Selects the plots so their separation in the graph is `min_separation`.

    The keys are popped, i.e. the corresponding plots are removed from the list
    to plot, until the separation between plots is larger than
    `min_separation`. `min_separation` is measured in fractions of the total
    heigth of the plot. 

    If you are using the two-column APS style, a good value for `min_separation
    is 1/25, which correspond to a font size of 6 points in the plot. It

    Parameters
    ----------

    vertical_axis_and_heights: a list of dictionaries of strings on floats.
        The list with the values of the plots, labelled by a string, along some
        vertical axis.
    min_separation: a float.  
        The minimum separation between plots required. It's measured in
        fractions of the total heigth of the plot.
    banned: a list of strings (defaulted to '[]').
        The list of keys that won't be popped.

    Example
    -------
    >>> from dmrg_helpers.view.separate_plots import select_keys
    >>> vertical_axis_and_heights = []
    >>> labels = ['a', 'b', 'c', 'd']
    >>> values = [1.0, 3.3, 2.5, 3.9]
    >>> vertical_axis = dict(izip(labels, values))
    >>> height = 10.0 # assume the plot has this height
    >>> vertical_axis_and_heights.append((vertical_axis, height))
    >>> labels = ['d', 'b', 'c', 'a']
    >>> values = [1.0, 3.3, 2.5, 4.0]
    >>> vertical_axis = dict(izip(labels, values))
    >>> height = 5.0 # assume the plot has this height
    >>> # The values of the separations are: 
    >>> # {(a, c): 0.15, (c, b): 0.08, (b, d): 0.06}
    >>> # {(d, c): 0.3, (c, b): 0.16, (b, a): 0.14}
    >>> vertical_axis_and_heights.append((vertical_axis, height))
    >>> select_keys(vertical_axis_and_heights, 0.5, ['a', 'd'])
    set(['a', 'd'])

    """
    separation_list = [get_scaled_up_separations(v, h) 
                      for (v, h) in vertical_axis_and_heights]
    selected, separation_list = pop_until_separated(separation_list,
                                                    min_separation,
                                                    banned)
    return selected
