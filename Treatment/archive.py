import itertools

import numpy
import pylab

from StringIO import StringIO

from lxml import etree, objectify
from scipy import ndimage

from _helpers import tt_tuple, tt_str, tt_int


data_types = {
    "com.tomotherapy.tomo.auto.tcorba.TFloatPair" : tt_tuple,
    "com.tomotherapy.tomo.auto.tcorba.TFloatTriplet" : tt_tuple,
    "[I" : tt_tuple,
    "java.lang.String" : tt_str,
    "java.lang.Integer" : tt_int,
    "com.tomotherapy.tomo.auto.tcorba.TImageType" : tt_str,
    "com.tomotherapy.tomo.auto.tcorba.TArrayDataType" : tt_str,
    "com.tomotherapy.tomo.auto.tcorba.TPersonGender" : tt_str,
    "com.tomotherapy.tomo.auto.tcorba.TCurrency" : tt_str,
    "com.tomotherapy.tomo.auto.tcorba.TPatientDataPackage.TROIInterpretedType" : tt_str,
    'Float_Data' : '>f',
    'Short_Data' : '>i2',          
}


class Target(object):
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.unique = True
        self.obj = None
        self.attrs = {}
        self.length = None
        self.typ = None
    
        for k, v in kwargs.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                # logging or raise?
                pass


class Record(object):
    """
    Everything is a Record.

    This is where the logic of Record creation is held given a mapping
    from a Tomotherapy XML to Python objects.
    """
    def __init__(self, tree, **kwargs):
        self.tree = tree  
        for name, target in kwargs.iteritems():
            target = Target(**target)

            targets = []
            for t in self.tree.iter(target.tag):
                if target.typ is not None:
                    if target.typ != t.attrib["Type"]:
                        continue
                if target.obj is None:
                    obj = data_types[t.attrib["Type"]]
                else:
                    obj = target.obj
                
                if len(t) == target.length or target.length is None:
                    targets.append(obj(t, **target.attrs))
 
            #assert len(targets) > 0, "<%s not found in tree." % target.tag
            if target.unique is True:
                assert len(targets) == 1, \
                    "%s possible entries found for <%s> when asserted as unique." \
                    % (len(targets), target.tag)
                setattr(self, name, targets[0])
            else:
                setattr(self, name, targets)        


class Archive(Record):
    def __init__(self, filename, **kwargs):
        self.filename = filename
        tree = etree.parse(file(self.filename))
        
        super(Archive, self).__init__(tree, **kwargs)
        
    @property
    def mvct(self):
        return [i for i in self.images if i.image_type == "MVCT"]
        
    @property
    def kvct(self):
        return [i for i in self.images if i.image_type == "KVCT"]

    @property
    def qa_dose(self):
        return [i for i in self.images if i.image_type == "Delivery_QA_Dose"]
        
        
class Patient(Record):
    pass        


class Contour(Record):
    def __init__(self, tree, **kwargs):
        super(Contour, self).__init__(tree, **kwargs)
#        self.load()

    def load(self):
        self.rois = etree.parse(file(self.filename)).iter("pointData")
        self.points = [[map(float, r.strip().split(',')) for r in
                        roi.text.split(';') if r.strip() != ''] for roi in self.rois] 


class VolumeImage(Record):
    def __init__(self, tree, **kwargs):
        super(VolumeImage, self).__init__(tree, **kwargs)
#        self.load()
        
    def load(self):
        #logger.info("Reading image: %s" % self.filename)
        self.data = numpy.fromstring(file(self.filename).read(), dtype=data_types[self.dtype])
        self.data.resize(self.shape)

    @property
    def extent(self):
        return self.x_extent + self.y_extent + self.z_extent
        
    @property
    def z_extent(self):
        return (0, self.shape[0]*self.resolution[0])
        
    @property
    def y_extent(self):
        return (0, self.shape[1]*self.resolution[1])
        
    @property
    def x_extent(self):
        return (0, self.shape[2]*self.resolution[2])
    
        
class Film(Record):
    def __init__(self, tree, **kwargs):
        super(Film, self).__init__(tree, **kwargs)
#        self.load()
        
    def load(self):
        #logger.info("Reading film: %s" % self.filename)
        #logger.info("\tshape:\t\t%s\n\tresolution:\t%s" % (str(self.shape), str(self.resolution)))
        
        self.raw = 2**16 - numpy.fromstring(file(self.filename).read(), dtype='>u2')
        self.raw.resize(self.shape)

        self.calibration_factors = [tt_tuple(c) for c in \
                                    self.tree.find("scanValueDoseCalibration").getchildren()]
        self.calibration_factors = [numpy.array([0., 0.]), ] + self.calibration_factors
        
        self.calibration_offset = self.calibration_factors[0][1]
        
        #logger.info("Calibrating film.")
        self.calibration_grid = numpy.zeros(self.raw.shape, dtype=float)
        for i, c in enumerate(self.calibration_factors[1:]):
             index = numpy.where((self.raw > self.calibration_factors[i-1][1]) \
                                 * (self.raw < c[1]))
             self.calibration_grid[index] = (c[0] - self.calibration_factors[i-1][0]) \
                                            / (c[1] - self.calibration_factors[i-1][1])
        
        self.data = (self.raw.astype(float) - self.calibration_offset) \
                    * self.calibration_grid
    
    @property
    def y_extent(self):
        return (0, self.shape[0]*self.resolution[0])
        
    @property
    def x_extent(self):
        return (0, self.shape[1]*self.resolution[1])      
          
