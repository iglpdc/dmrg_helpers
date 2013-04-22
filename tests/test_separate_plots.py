"""
Test for the functions to separate plots.
"""
import dmrg_helpers.view.separate_plots as sp
from dmrg_helpers.core.dmrg_exceptions import DMRGException
from nose.tools import assert_almost_equal, raises
from itertools import izip

def test_get_scaled_up_separations_fine():
    labels = ['a', 'b', 'c', 'd']
    values = [1.0, 3.3, 2.5, 4.0]
    vertical_axis = dict(izip(labels, values))
    height = 10.0 # assume the plot has this height
    sep = sp.get_scaled_up_separations(vertical_axis, height)
    assert_almost_equal( sep[('a', 'c')], 0.15)
    assert_almost_equal( sep[('c', 'b')], 0.08)
    assert_almost_equal( sep[('b', 'd')], 0.07)

def test_get_scaled_up_separations_empty():
    empty = {}
    sep = sp.get_scaled_up_separations(empty, 10)
    assert sep == empty

def test_get_key_to_pop_fine():
    labels = ['a', 'b', 'c', 'd']
    values = [1.0, 3.3, 2.5, 4.0]
    vertical_axis = dict(izip(labels, values))
    height = 10.0 # assume the plot has this height
    sep = sp.get_scaled_up_separations(vertical_axis, height)
    assert sp.get_key_to_pop([sep], []) == 'd'

def test_get_key_to_pop_banned():
    labels = ['a', 'b', 'c', 'd']
    values = [1.0, 3.3, 2.5, 6.0]
    vertical_axis = dict(izip(labels, values))
    height = 10.0 # assume the plot has this height
    sep = sp.get_scaled_up_separations(vertical_axis, height)
    banned = ['b']
    assert sp.get_key_to_pop([sep], banned) == 'c'

@raises(DMRGException)
def test_get_key_to_pop_raise():
    labels = ['a', 'b', 'c', 'd']
    values = [1.0, 3.3, 2.5, 4.0]
    vertical_axis = dict(izip(labels, values))
    height = 10.0 # assume the plot has this height
    sep = sp.get_scaled_up_separations(vertical_axis, height)
    banned = ['b', 'd']
    sp.get_key_to_pop([sep], banned)

def test_get_smallest_distance():
    sep_1 = {('a', 'c'): 0.15, ('c', 'b'): 0.08, ('b', 'd'): 0.15}
    sep_2 = {('a', 'b'): 0.05, ('b', 'c'): 0.18, ('c', 'd'): 0.15}
    sep_list = [sep_1, sep_2]
    assert_almost_equal(sp.get_smallest_distance(sep_list), 0.05)

def test_get_smallest_distance_equal_keys():
    sep_1 = {('a', 'c'): 0.05, ('c', 'b'): 0.08, ('b', 'd'): 0.15}
    sep_2 = {('a', 'c'): 0.05, ('c', 'b'): 0.18, ('b', 'd'): 0.15}
    sep_list = [sep_2, sep_1]
    assert_almost_equal(sp.get_smallest_distance(sep_list), 0.05)

def test_get_candidate_keys():
    sep_1 = {('a', 'c'): 0.15, ('c', 'b'): 0.08, ('b', 'd'): 0.15}
    sep_2 = {('a', 'b'): 0.05, ('b', 'c'): 0.18, ('c', 'd'): 0.15}
    sep_list = [sep_1, sep_2]
    assert sp.get_candidate_keys(sep_list) == ('a', 'b')

def test_select_keys():
    vertical_axis_and_heights = []
    labels = ['a', 'b', 'c', 'd']
    values = [1.0, 3.3, 2.5, 3.9]
    vertical_axis = dict(izip(labels, values))
    height = 10.0 # assume the plot has this height
    vertical_axis_and_heights.append((vertical_axis, height))
    labels = ['d', 'b', 'c', 'a']
    values = [1.0, 3.3, 2.5, 4.0]
    vertical_axis = dict(izip(labels, values))
    height = 5.0 # assume the plot has this height
    # The values of the separations are: 
    # {(a, c): 0.15, (c, b): 0.08, (b, d): 0.06}
    # {(d, c): 0.3, (c, b): 0.16, (b, a): 0.14}
    vertical_axis_and_heights.append((vertical_axis, height))
    selected = sp.select_keys(vertical_axis_and_heights, 0.1, ['a', 'd'])
    assert set(['a', 'c', 'd']) == set(selected)

def test_select_keys_two():
    vertical_axis_and_heights = []
    labels = ['a', 'b', 'c', 'd']
    values = [1.0, 3.3, 2.5, 3.9]
    vertical_axis = dict(izip(labels, values))
    height = 10.0 # assume the plot has this height
    vertical_axis_and_heights.append((vertical_axis, height))
    labels = ['d', 'b', 'c', 'a']
    values = [1.0, 3.3, 2.5, 4.0]
    vertical_axis = dict(izip(labels, values))
    height = 5.0 # assume the plot has this height
    # The values of the separations are: 
    # {(a, c): 0.15, (c, b): 0.08, (b, d): 0.06}
    # {(d, c): 0.3, (c, b): 0.16, (b, a): 0.14}
    vertical_axis_and_heights.append((vertical_axis, height))
    selected = sp.select_keys(vertical_axis_and_heights, 0.145, ['a', 'd'])
    assert set(['a', 'd']) == set(selected)

def test_select_keys_all():
    vertical_axis_and_heights = []
    labels = ['a', 'b', 'c', 'd']
    values = [1.0, 3.3, 2.5, 3.9]
    vertical_axis = dict(izip(labels, values))
    height = 10.0 # assume the plot has this height
    vertical_axis_and_heights.append((vertical_axis, height))
    labels = ['d', 'b', 'c', 'a']
    values = [1.0, 3.3, 2.5, 4.0]
    vertical_axis = dict(izip(labels, values))
    height = 5.0 # assume the plot has this height
    # The values of the separations are: 
    # {(a, c): 0.15, (c, b): 0.08, (b, d): 0.06}
    # {(d, c): 0.3, (c, b): 0.16, (b, a): 0.14}
    vertical_axis_and_heights.append((vertical_axis, height))
    selected = sp.select_keys(vertical_axis_and_heights, 0.5, ['a', 'd'])
    assert set(['a', 'd']) == set(selected)
