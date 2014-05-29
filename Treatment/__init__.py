import logging


logger = logging.getLogger('Treatment')
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


from archive import Archive, Patient, VolumeImage, Contour, Film, Sinogram
from _helpers import tt_tuple, tt_str, tt_float, tt_int

def debug(debug_on=False):
    global logger, debugging
    if debug_on:
        logger.setLevel(logging.DEBUG)
        debugging = True
    else:
        logger.setLevel(logging.WARNING)
        debugging = False

default_mapping = {
    "patient_info" : {
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
    "treatment_info" : {
        "tag" : "FullPatient",
        "obj" : Patient,
        "attrs" : {
            "disease_name" : {"tag" : "diseaseName", "unique" : False},
            "prescribed_dose" : {"tag" : "prescribedDose", "obj" : tt_float, "unique" : False},
            "gantry_period" : {"tag" : "nominalGantryPeriod", "obj" : tt_float, "unique" : False},
            "couch_speed" : {"tag" : "desiredCouchSpeed", "obj" : tt_float, "unique" : False},
            "projections_per_rotation" : {"tag" : "numProjsPerRotation", "obj" : tt_int, "unique" : False},
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
    "contours" : {
        "tag" : "troiList",
        "typ" : "com.tomotherapy.tomo.auto.tcorba.TPatientDataPackage.TROI",
        "unique" : False,
        "obj" : Contour,
        "attrs" : {
            "filename" : {"tag" : "curveDataFile"},
            "name" : {"tag" : "name"},
            "number" : {
                "tag" : "structureNumber",
                "obj" : tt_str,
                "attrs" : {
                    "dtype" : int,
                }, 
            },
            "interpreted_type" : {"tag" : "interpretedType"},
            "user" : {"tag" : "userName"},
        },
    },
    "films" : {
        "tag" : "film",
        "unique" : False,
        "obj" : Film,
        "attrs" : {
            "filename" : {"tag" : "sinogramDataFile"},
            "origin" : {
                "tag" : "phantomOrigin",
                "obj" : tt_tuple,
                "attrs" : { "reverse" : True},
            },
            "position" : {"tag" : "filmOrigin"},
            "cosines_x" : {"tag" : "filmXDirectionCosines"},
            "cosines_y" : {"tag" : "filmYDirectionCosines"},
            "shape" : {
                "tag" : "dimensions",
                "obj" : tt_tuple,
                "length" : 2,
                "attrs" : {
                    "dtype" : int,
                },
            },
            "resolution" : {"tag" : "resolution"},
            "calibration_factors" : {
                "tag" : "scanValueDoseCalibration",
                "obj" : tt_tuple,
                "unique" : False,
                "length" : 2,
            },
        },
    },
    "sinograms" : {
        "tag" : "detectorSinogram",
        "unique" : False,
        "obj" : Sinogram,
        "attrs" : {
            "filename" : {"tag" : "sinogramDataFile"},
        },
    },
}

