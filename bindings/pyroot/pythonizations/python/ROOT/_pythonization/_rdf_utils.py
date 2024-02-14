# Author: Stefan Wunsch CERN, Vincenzo Eduardo Padulano (UniMiB, CERN) 07/2019

################################################################################
# Copyright (C) 1995-2018, Rene Brun and Fons Rademakers.                      #
# All rights reserved.                                                         #
#                                                                              #
# For the licensing terms see $ROOTSYS/LICENSE.                                #
# For the list of contributors see $ROOTSYS/README/CREDITS.                    #
################################################################################

from __future__ import annotations
from typing import Iterable
import numpy


class ndarray(numpy.ndarray):
    """
    A wrapper class that inherits from `numpy.ndarray` and allows to attach the
    result pointer of the `Take` action in an `RDataFrame` event loop to the
    collection of values returned by that action. See
    https://docs.scipy.org/doc/numpy/user/basics.subclassing.html for more
    information on subclassing numpy arrays.
    """

    def __new__(cls, numpy_array, result_ptr):
        """
        Dunder method invoked at the creation of an instance of this class. It
        creates a numpy array with an `RResultPtr` as an additional
        attribute.
        """
        obj = numpy.asarray(numpy_array).view(cls)
        obj.result_ptr = result_ptr
        return obj

    def __array_finalize__(self, obj):
        """
        Dunder method that fills in the instance default `result_ptr` value.
        """
        if obj is None:
            return
        self.result_ptr = getattr(obj, "result_ptr", None)


def _is_ragged(iterable: Iterable) -> bool:
    """
    Check if the given iterable is ragged.
    """
    # TODO: Handle array of arrays... etc.
    try:
        iterable_length = len(iterable)
    except TypeError:
        return True

    if iterable_length == 0:
        return False

    first_length = None
    for item in iterable:
        # iterable may not support indexing
        first_length = len(item)
        break

    if all(len(item) == first_length for item in iterable):
        return False

    return True
