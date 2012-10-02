Read Tomotherapy Patient Treatment Archives
===========================================

This Python module provides a simple API for accessing data contained within a standard Tomotherapy patient treatment archive. This includes MVCT and kVCT datasets, sinograms, planning volumes/contours, patient dose grids, and patient specific quality assurance data (DQA) such as irradiated films and phantom dose grids.

Installation
------------
    git clone https://github.com/christopherpoole/Treatment.git
    cd Treatment
    sudo python setup.py install

Usage
-----
The archive is generally made up of a primary XML file, usually called something like `patient_their_name.xml`, and a directory filled with binary blobs (images and sinograms) and more XML files which make up the patient contours.

    from Treatment import Archive, default_mapping

    archive = Archive("archive.xml", **default_mapping)
    
    # Or with optional custom mapping
    archive = Archive("archive.xml", **mapping)

    archive.films      # List of DQA films
    archive.kvct       # List of kVCT images
    archive.mvct       # List of MVCT images
    archive.qa_dose    # List of qa_dose images

Dependencies
------------
The patient archive is pretty ragged XML, so [lxml](http://lxml.de/) is used to parse it. [numpy](http://numpy.scipy.org/), [scipy](http://www.scipy.org/) and [pylab](http://www.scipy.org/PyLab) are used for manipulation of data arrays and display.


Custom Mappings
---------------

The mapping between the XML archive and Python objects can be customised by the user - this is mostly to cope with the possibility of different archive versions in the future. A part of the default mapping is shown below:

    from archive import Patient, VolumeImage
    from _helpers import tt_str, tt_tuple, tt_dict

    mapping = {
        "patient" : {
            "tag" : "briefPatient",
            "obj" : Patient,
            "attrs" : {
                "name" : {"tag" : "patientName"},
                "gender" : {"tag" : "patientGender"},
                "dob" : {"tag" : "patientBirthDate"},
                "unique_id" : {"tag" : "patientID"},
                "currency" : {"tag" : "currency"},
            },
        },
        "images" : {
            "tag" : "image",
            "unique" : False,
            "obj" : VolumeImage,
            "attrs" : {
                "filename" : {"tag" : "binaryFileName"},
                "image_type" : {"tag" : "imageType"},
                "shape" : {
                    "tag" : "dimensions",
                    "obj" : tt_tuple,
                    "attrs" : {
                        "reverse" : True,
                    },
                },
                "resolution" : {
                    "tag" : "elementSize",
                    "obj" : tt_tuple,
                    "attrs" : {
                        "reverse" : True,
                    },
                },
                "position" : {
                    "tag" : "start",
                    "obj" : tt_tuple,
                    "attrs" : {
                        "reverse" : True,
                    },
                },
                "dtype" : {"tag" : "dataType"},
                "user" : {"tag" : "userName"},
            },
        },
    }

TODO's
------

* The handling of the default mapping is a bit uncomfortable at the moment, instead of being parsed and kwargs to Archive, just the dict might be better.
* Reading of sinograms is not currently included in the default mapping
* Film calibration needs to be more throughly tested
