import re
import numpy
from lxml import etree


data_types = {
    'java.lang.String' : str,
    'java.lang.Integer' : int,
    'java.lang.Float' : float,
    'com.tomotherapy.tomo.auto.tcorba.TFloatPair' : float,
}


def uncamel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().replace('__', '_')


def tt_dict(tree, dtype=None):
    _dtype = tree[0].attrib['Type']
    if dtype is None:
        dtype = data_types[_dtype]

    return dict([(e.tag, dtype(e.text)) for e in tree if e.attrib["Type"][0] != '['])


def tt_tuple(tree, length=None, dtype=None, reverse=False):
    """
    Return a tuple from a tree of leaves with the option of asserting a
    length and a dtype. All data elements however must have the same dtype.
    """
    data = [element.text for element in tree]    
    if length is not None:
        assert len(data) == length, "Tree with %i elements provided, with length %i expected/asserted." % (len(data), length)

    _dtype = set(element.attrib['Type'] for element in tree)
    assert len(_dtype) == 1, "Elements must all be the same type."
    
    _dtype = tree[0].attrib['Type']
    if dtype is not None:
        assert data_types[_dtype] == dtype, "Tree with %s elements provided, %s expected/asserted." % (_dtype, dtype)
         
    if dtype is None:
        dtype = data_types[_dtype]
        
    if reverse is True:
        data.reverse() 

    return numpy.array(map(dtype, data))
   
   
def tt_str(tree, dtype=str):
    return dtype(tree.text)

def tt_int(tree, dtype=int):
    return dtype(tree.text)
 
def tt_float(tree, dtype=float):
    return dtype(tree.text)
    
def timestamp(tree):
    date = int(tree.find("data").text)
    time = int(tree.find("time").text)
    
    return (date, time)

