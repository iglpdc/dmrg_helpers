"""Functions to remove some of the plots.

Usually you have a bunch of plots and you may want to remove some to them to
keep only those separated by a certain distance, so the graph is not
cluttered with tens of lines.
"""
import numpy as np
import operator
from itertools import izip
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

    Example
    -------
    >>> labels = ['a', 'b', 'c', 'd']
    >>> values = [1.0, 3.3, 2.5, 4.0]
    >>> vertical_axis = dict(izip(labels, values))
    >>> height = 10.0 # assume the plot has this height
    >>> get_scale_up_separations(vertical_axis, height)
    {(a, c): 0.15, (c, b): 0.08, (b, d): 0.15}

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

    sorted_axis = sorted(vert_axis.iteritems(), key = operator.itemgetter(1))
    key_pairs = get_two_consecutive_iterators(sorted_axis.iterkeys())
    y_vals = np.array([v for v in sorted_axis.itervalues()])
    return dict(izip(key_pairs, np.diff(y_vals) / height))

def get_smallest_distance(separation_list):
    """Returns the smallest distance between two plots for all the graphs.

    Example
    -------
    >>> sep_1 = {(a, c): 0.15, (c, b): 0.08, (b, d): 0.15}
    >>> sep_2 = {(a, b): 0.05, (d, c): 0.18, (b, d): 0.15}
    >>> sep_list = [sep_1, sep_2]
    >>> get_smallest_distance(sep_list)
    0.05

    """
    return min([s[min(s, key = operator.itemgetter(1))] 
                for s in separation_list])

def get_key_to_pop(separation_list, banned_keys=[]):
    """Returns the key for the plot with the smallest separation in the graphs.

    You use this function to pick up the key you want to remove. The key to
    remove is choosen between the two whose plots have the smallest separation
    among all graphs. To choose which of the two, you select the one that is
    closer to any of its neighbors in any plot.

    If the key is among the `banned_keys` is never popped.

    """
    def get_smallest_separation(d, key):
        """Returns the smallest separation for a key in a given graph.
        >>> labels = ['a', 'b', 'c', 'd']
        >>> values = [1.0, 3.3, 2.5, 4.0]
        >>> vertical_axis = dict(izip(labels, values))
        >>> height = 10.0 # assume the plot has this height
        >>> separations = get_scale_up_separations(vertical_axis, height)
        >>> get_smallest_separation('c')
        0.08
        >>> get_smallest_separation('a')
        0.15
        """
        a = b = None
        for k in d.iterkeys():
            k_1, k_2 = k
            if k_2 == key:
                a = d[k]
            elif k_1 == key:
                b = d[k]
        return a if (a < b and a is not None) else b

    key_1, key_2 = get_candidate_keys(separation_list) 

    # Check if the keys are banned.
    intersect = [key_1, key_2] & banned_keys
    if intersect:
        if len(intersect) == 2:
            raise DMRGException('Two banned keys to choose to pop')
        else: 
            return intersect[0]

    key_1_separations = sorted([get_smallest_separation(d, key_1) for d in
                                separation_list])
    key_2_separations = sorted([get_smallest_separation(d, key_2) for d in
                                separation_list])
    return key_1 if key_1_separations[1] < key_2_separations[1] else key_2

def get_candidate_keys(separation_list):
    tmp = [s[min(s, key = operator.itemgetter(1))] for s in separation_list]
    index = min([s for s in enumerate(tmp)], key = operator.itemgetter(1))[0]
    return min([s for s in separation_list[index]], 
               key = operator.itemgetter(1))

def pop_closest(separation_list):
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
    key = get_key_to_pop(separation_list)
    new_key = (None, None)
    new_value = 0.0
    for sep in separation_list:
        for k in sep.iterkeys():
            k_1, k_2 = k
            if k_2 == key:
                new_key[0] = k_1
                new_value += sep[k]
                sep.pop(k)
            elif k_1 == key:
                new_key[1] = k_2
                new_value += sep[k]
                sep.pop(k)
        sep[new_key] = new_value
    return separation_list

def pop_until_separated(separation_list, min_separation):
    """Removes one plot from each graph until there's certain separation.

    The plot removed is the same in all the graphs. 
    """
    while min_separation > get_smallest_distance(separation_list):
        separation_list = pop_closest(separation_list)
    return separation_list

def select_keys(vertical_axis_and_heights, min_separation):
    """Selects the plots so their separation in the graph is `min_separation`.

    Example
    -------
    >>> vertical_axis_and_heights = []
    >>> labels = ['a', 'b', 'c', 'd']
    >>> values = [1.0, 3.3, 2.5, 3.9]
    >>> vertical_axis = dict(izip(labels, values))
    >>> height = 10.0 # assume the plot has this height
    >>> vertical_axis_and_heights.append((vertical_axis, height))
    >>> labels = ['a', 'b', 'c', 'd']
    >>> values = [1.0, 3.3, 2.5, 4.0]
    >>> vertical_axis = dict(izip(labels, values))
    >>> height = 5.0 # assume the plot has this height
    >>> # The values of the separations are: 
    >>> # {(a, c): 0.15, (c, b): 0.08, (b, d): 0.14}
    >>> # {(a, c): 0.3, (c, b): 0.16, (b, d): 0.3}
    >>> vertical_axis_and_heights.append((vertical_axis, height))
    >>> selected = select_keys(vertical_axis_and_heights, 0.1)
    >>> assert set('a', 'c', 'd') == selected

    """
    separation_list = [get_scaled_up_separations(v, h) 
                       for (v, h) in vertical_axis_and_heights]
    separation_list = pop_until_separated(separation_list, min_separation)
    selected = separation_list[0].viewkeys()
    for s in separation_list:
        assert s.viewkeys() == selected
    return selected
