#!/usr/bin/env python

import os
import pexpect
import random
import re
import string
import sys
from tempfile import mkstemp, mkdtemp
import unittest

class TestPractica2_2(unittest.TestCase):

    def setUp(self):

        # create temporal files and directories
        self.n_files=2
        # [0] handle, [1] file name
        self.tmp_files = [ mkstemp(prefix='with_space ')[1] for _ in range(self.n_files) ]

        self.n_dirs=1
        self.tmp_dirs = [mkdtemp() for _ in range(self.n_dirs)]

    def tearDown(self):
        for fname in self.tmp_files:
            os.unlink(fname)

        for dname in self.tmp_dirs:
            os.rmdir(dname)

    def test_shebang(self):
        with open('./practica2_2.sh') as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or 
                    (pattern.match(first_line) != None))

    def test_spaces_in_name(self):
        """ Check whether the script supports filenames with spaces
        """
        # creation of the process every time because we have to change the 
        # argument list
        try: 
            self.child = pexpect.spawn('/bin/bash ./practica2_2.sh "{}"'.format(self.tmp_files[0]))
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)
    
    def test_directory(self):
        try:
            self.child = pexpect.spawn('/bin/bash ./practica2_2.sh "{}"'.format(self.tmp_dirs[0]))
        except:
            self.assertTrue(False)
        try:
            self.child.expect('{} no es un fichero'.format(self.tmp_dirs[0]))
        except:
            print str(self.child)
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)

    def test_invalid_name(self):
        fname=''.join(random.choice(string.ascii_letters + string.digits + ' ') for _ in range(16))
        while os.path.isfile(fname):
            fname=''.join(random.choice(string.ascii_letters + string.digits + ' ') for _ in range(16))

        try:
            self.child = pexpect.spawn('/bin/bash ./practica2_2.sh "{}"'.format(fname))
            self.child.expect('{} no es un fichero'.format(fname))
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)

    def test_list_files(self):
        """ Run the program with 3 arguments, two valid files with a 
            directory in between.

            Note that this test do not handle the case when more requests 
            to hit a key to continue
        """

        lines=[ ''.join(random.choice(string.ascii_letters) for _ in range(6)) ]

        # fill the files with random content
        for fname in self.tmp_files:
            with open(fname, 'w') as f:
                for l in lines:
                    f.write(l)

        try:
            self.child = pexpect.spawn('/bin/bash ./practica2_2.sh "{}" "{}" "{}"'.format(self.tmp_files[0], self.tmp_dirs[0], self.tmp_files[1]))
        except:
            self.assertTrue(False)

        try:
            # first file
            for l in lines:
                self.child.expect(l+'\r\n')
            # directory
            self.child.expect('{} no es un fichero'.format(self.tmp_dirs[0]))
            # second file
            for l in lines:
                self.child.expect(l+'\r\n')
        except:
            self.assertTrue(False)
        self.assertTrue(True)

        self.child.terminate(force=True)


if __name__ == "__main__":
    unittest.main()
