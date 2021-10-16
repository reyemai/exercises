

import sys
import os
from subprocess import Popen, PIPE
from threading import Thread, Lock, Event
import argparse
import shutil

input_file_requirements = """\
Input file format:
Lines that start with are used as test stimuli/comparison: [stdout|stdin|stderr]:
All other lines are ignored (empty lines are ignored as well).
Script tested with: dc (GNU bc 1.07.1) 1.4.1, Python 3.8.5, Ubuntu 20.04.2 LTS
"""


class Test(object):
    FORMAT_STDIN = b"stdin:"
    FORMAT_STDOUT = b"stdout:"
    FORMAT_STDERR = b"stderr:"

    def __init__(self):
        object.__init__(self)
        self.input = None
        self.output = []
        self.errors = []

        self.result = None

    @staticmethod
    def check_dest(line,format):
        return line[:len(format)] == format
    @staticmethod
    def extract_str(line,format):
        return line[len(format)+1:]

    def set_input(self,line):
        self.input = Test.extract_str(line, Test.FORMAT_STDIN)

    def add_output(self,line,error=False):
        self.errors.append(error)
        if error:
            format = Test.FORMAT_STDERR
        else:
            format = Test.FORMAT_STDOUT
        self.output.append(Test.extract_str(line, format))

    @staticmethod
    def parse_test_from_file(test_path):

        if not os.path.isfile(test_path):
            raise Exception("File " + str(test_path) + " doesn't exists.")
        tests = []
        lines = []
        with open(test_path, "rb") as f:
            lines = f.readlines()

        test = None
        for line in lines:
            line = remove_binary_line_ending(line)
            if line != b"":
                if Test.check_dest(line, Test.FORMAT_STDIN):
                    if test != None:
                        tests.append(test)
                    test = Test()
                    test.set_input(line)
                else:
                    if test == None:
                        test = Test()
                    if Test.check_dest(line, Test.FORMAT_STDOUT):
                        test.add_output(line)
                    elif Test.check_dest(line, Test.FORMAT_STDERR):
                        test.add_output(line,error=True)

        if test != None:
            tests.append(test)

        return tests

class NonBlockingReader(object):
    def __init__(self,fp,max_lines=25):
        object.__init__(self)
        self.max_lines = max_lines
        self.fp = fp
        self.buffer = []
        self.mutex = Lock()
        self.data_ready = Event()
        self.data_ready.clear()
        self.stop_thread = False
        self.t = Thread(target=self._thread_read_line)
        self.t.daemon = True
        self.t.start()

    def _thread_read_line(self):
        while not self.stop_thread:
            output = self.fp.readline()
            self.mutex.acquire()
            if len(self.buffer) > self.max_lines:
                self.stop_thread = True
            self.buffer.append(output)
            self.data_ready.set()
            self.mutex.release()

    def has_data(self):
        return self.data_ready.isSet()

    def readline(self,timeout=0.5):
        line = None
        # Reading immediately may lead to a false empty buffer
        if self.data_ready.wait(timeout=timeout):
            self.mutex.acquire()
            line = remove_binary_line_ending(self.buffer.pop(0))
            if len(self.buffer) == 0:
                self.data_ready.clear()
            self.mutex.release()
        return line

    def empty_buffer(self):
        self.mutex.acquire()
        ret = self.buffer[:]
        self.buffer = []
        self.data_ready.clear()
        self.mutex.release()
        return ret

def remove_binary_line_ending(line):
    if line[-len(os.linesep):] == os.linesep.encode("ascii"):
        line = line[:-len(os.linesep)]
    return line

def main():

    # Parse the arguments
    parser = argparse.ArgumentParser("Testing an interactive console program", epilog=input_file_requirements)
    parser.add_argument("sw_under_test", help="Software name or path to be tested.")
    parser.add_argument("test_case_path", help="Test cases as text file path.")
    args = parser.parse_args()

    sw_under_test = args.sw_under_test
    test_case_path = args.test_case_path

    # Checking the sw to be tested actually exists:
    sw_under_test_full_path = shutil.which(sw_under_test)
    if sw_under_test_full_path == None:
        raise Exception("Cannot find software to be tested: " + str(sw_under_test))

    # Parse input files:
    # Tests will be some objects of input + [output]
    tests = Test.parse_test_from_file(test_case_path)

    # Subprocess running sw under test
    p = Popen(sw_under_test, stdin=PIPE,stdout=PIPE,stderr=PIPE, bufsize=0)

    # The readers of STDOUT and STDIN will be on a different thread
    #  The main reason is that subrocess PIPE reads are blocking.
    stdout_reader = NonBlockingReader(p.stdout)
    stderr_reader = NonBlockingReader(p.stderr)

    for t in tests:
        # Check the sw under test is still running:
        if p.poll() != None:
            break

        if t.input:
            # Clean the output from a previous test:
            stdout_reader.empty_buffer()
            stderr_reader.empty_buffer()

            # Send input to the sw under test
            p.stdin.write(t.input+b'\n')
            p.stdin.flush()

        for expected_output, error in zip(t.output, t.errors):
            # Check the sw under test is still running:
            if p.poll() != None:
                break

            # Read from the expected reader
            reader = stderr_reader if error else stdout_reader
            output = reader.readline()

            # Compare the output line:
            if expected_output != output:
                t.result = False
                break
        else:
            # Check for some unexpected output:
            if stdout_reader.has_data() or stderr_reader.has_data():
                t.result = False
            else:
                t.result = True


    if p.poll() == None:
        p.terminate()

    stdout_reader.stop_thread = True
    stderr_reader.stop_thread = True

    failed = 0
    passed = 0
    not_executed = 0
    for t in tests:
        if t.result == None:
            not_executed += 1
        elif t.result:
            passed += 1
        else:
            failed += 1

    print("Total number of tests: " +str(len(tests)))
    print("Test passed: " + str(passed))
    print("Test failed: " + str(failed))



if __name__ == "__main__":
    main()