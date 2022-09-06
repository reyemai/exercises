#!/usr/bin/env python
""" Simple examples of calling C functions through ctypes module. """
import ctypes
import sys,os
import pathlib

if __name__ == "__main__":
    libname = pathlib.Path().absolute()
    print("libname: ", libname)
    dll = os.path.join(libname,"TradingFW.dll")
    print("DLL: "+dll)
    if not os.path.isfile(dll):
        print("ERROR: cppmult.dll is missing!")
        raise Exception("cppmult.dll is missing")


    # Load the shared library into c types.
    if sys.platform.startswith("win"):
        c_lib = ctypes.CDLL(dll)

    c_lib.get.restype = ctypes.c_int
    c_lib.NewTradingFW.restype = ctypes.c_void_p
    myobj = ctypes.c_void_p(c_lib.NewTradingFW())
    c_lib.set(myobj, 20)
    value = c_lib.get(myobj)
    print("Value must be 20: "+str(value))
    #
    # # Sample data for our call:
    # x, y = 6, 2.3
    #
    # # You need tell ctypes that the function returns a float
    # c_lib.cppmult.restype = ctypes.c_float
    # answer = c_lib.cppmult(x, ctypes.c_float(y))
    # print(f"    In Python: int: {x} float {y:.1f} return val {answer:.1f}")
