'''
File: test_generate_indexes.py
Author: Ivan Gonzalez
Description: Test for generate_indexes module.
'''
from dmrg_helpers.extract.generate_indexes import SiteFilter

def test_constant():
    f = SiteFilter('1')
    assert f.is_constant() == True
    assert f.build_index(5) == 1

def test_odd():
    f = SiteFilter('2*i+1')
    assert f.is_constant() == False
    assert f.build_index(5) == 11

def test_even():
    f = SiteFilter('2*i')
    assert f.is_constant() == False
    assert f.build_index(5) == 10

def test_identity():
    f = SiteFilter('i')
    assert f.is_constant() == False
    assert f.build_index(5) == 5

