'''
Test for generate_indexes module.
'''
from dmrg_helpers.extract.generate_indexes import SiteFilter

def test_constant():
    f = SiteFilter('1')
    assert f.a == '1'
    assert f.i == None
    assert f.pm == None
    assert f.b == None
    assert f.is_constant() == True
    assert f.build_index(5) == 1

def test_odd():
    f = SiteFilter('2*i+1')
    assert f.a == '2'
    assert f.i == 'i'
    assert f.pm == '+'
    assert f.b == '1'
    assert f.is_constant() == False
    assert f.build_index(5) == 11

def test_even():
    f = SiteFilter('2*i')
    assert f.a == '2'
    assert f.i == 'i'
    assert f.pm == None
    assert f.b == None
    assert f.is_constant() == False
    assert f.build_index(5) == 10

def test_identity():
    f = SiteFilter('i')
    assert f.a == None
    assert f.i == 'i'
    assert f.pm == None
    assert f.b == None
    assert f.is_constant() == False
    assert f.build_index(5) == 5

