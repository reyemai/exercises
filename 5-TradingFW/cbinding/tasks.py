""" Task definitions for invoke command line utility for python bindings
    overview article.
    Credits: https://github.com/realpython/materials/tree/master/python-bindings
"""
import invoke
import pathlib
import sys
import os
import shutil
import re
import glob

on_win = sys.platform.startswith("win")


@invoke.task
def clean(c):
    """Remove any built objects"""
    for file_pattern in (
        "*.o",
        "*.so",
        "*.obj",
        "*.dll",
        "*.exp",
        "*.lib",
        "*.pyd",
        "cython_wrapper.cpp",
    ):
        for file in glob.glob(file_pattern):
            os.remove(file)
    for dir_pattern in "Release":
        for dir in glob.glob(dir_pattern):
            shutil.rmtree(dir)


def print_banner(msg):
    print("==================================================")
    print("= {} ".format(msg))

@invoke.task()
def test_ctypes_cpp(c):
    """Run the script to test ctypes"""
    print_banner("Testing ctypes Module for C++")
    # pty and python3 didn't work for me (win).
    if on_win:
        invoke.run("python ctypes_cpp_test.py")
    else:
        invoke.run("python3 ctypes_cpp_test.py", pty=True)

@invoke.task()
def build_TradingFW(c):
    """Build the shared library for the sample C++ code"""
    print_banner("Building C++ Library TradingFW.cpp")
    command = ("g++ -O3 -Wall  -shared -std=c++11 TradingFW.cpp " # -fPIC -Werror
        "-o TradingFW.dll -fPIC "
        " -static "
        )
    print(command)
    invoke.run(command)
    sofile = os.path.abspath("TradingFW.dll")
    if not os.path.isfile(sofile):
        print("ERROR: Output "+sofile+" not found!")

    print("* Complete")


@invoke.task(
    clean,
    build_TradingFW,
    test_ctypes_cpp,
)
def all(c):
    """Build and run all tests"""
    pass
