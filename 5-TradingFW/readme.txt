Author: Marco Bettoni
Data: 2021/11/21

Title:
    Code for "Programming project for quantitative researcher"

Summary:
    Basic demostration predictive signal generation.
    The basic Framework has been inspired by Pandas well know structure.
    Once all Pandas function have been removed, the basic function have
    beed replaced with faster C instruction.
    The basic Python environment intefaces the C++ framework by means
    of a .DLL.

Content:
    .\cbinding\            - C++ Framework
        compile_cpp.bat    - compilation script in virtualenv 
        ctypes_cpp_test.py - test for the C++ Framework
        tasks.py           - "invoke" make file
        TradingFW.cpp      - main file for C++ Framework
        TradingFW.dll      - [to be compiled]
        TradingFW.hpp      - header for C++ Framework
    .\MarketDataFiles\     - input .csv data
    .\venv\                - python3 virtual env
    .\main.py              - main code
    .\readme.txt           - this file
    .\requirements.txt     - virtualenv requirements
    .\TradingFW.py         - python Framework
    .\main.cpp             - Main + test

How to BUILD:
    > cd %this_folder%
    > python3 -m virtualenv venv
    > call venv\Scripts\activate
    > pip install requirements.txt
    > deactivate
    > cd cbinding
    > call compile_cpp.bat

How to RUN:
    > call venv\Scripts\activate
    > python main.py

Testing Environment:
    - gcc version 9.3.0
    - Windows 10 build 1910a November 2019