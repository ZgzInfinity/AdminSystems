#!/usr/bin/env python

import os
import pexpect
import random
import re
from stat import S_ISREG, ST_MODE, S_IXUSR
import string
import sys
from tempfile import mkstemp, mkdtemp
import unittest

class TestPractica2_3(unittest.TestCase):

    def setUp(self):

        # create temporal files and directories
        self.tmp_handle, self.tmp_name = mkstemp(prefix='with_space ')

    def tearDown(self):
        os.close(self.tmp_handle)
        os.unlink(self.tmp_name)

    def test_shebang(self):
        with open('./practica2_3.sh') as f:
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
            self.child = pexpect.spawn('/bin/bash ./practica2_3.sh "{}"'.format(self.tmp_name))
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)
    
    def test_invalid_name(self):
        fname=''.join(random.choice(string.ascii_letters + string.digits + ' ') for _ in range(16))
        while os.path.isfile(fname):
            fname=''.join(random.choice(string.ascii_letters + string.digits + ' ') for _ in range(16))

        try:
            self.child = pexpect.spawn('/bin/bash ./practica2_3.sh "{}"'.format(fname))
            self.child.expect('{} no existe'.format(fname))
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)

    def test_no_arguments(self):
        try: 
            self.child = pexpect.spawn('/bin/bash ./practica2_3.sh')
            self.child.expect('Sintaxis: practica2_3.sh <nombre_archivo>\r\n')
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)
    
    def test_three_arguments(self):
        try: 
            self.child = pexpect.spawn('/bin/bash ./practica2_3.sh one two three')
            self.child.expect('Sintaxis: practica2_3.sh <nombre_archivo>\r\n')
        except:
            self.assertTrue(False)
        self.assertTrue(True)
        
        self.child.terminate(force=True)

    def test_valid_file(self):
        try: 
            self.child = pexpect.spawn('/bin/bash ./practica2_3.sh "{}"'.format(self.tmp_name))
            self.child.expect('-[r|-][w|-]x[r|-][w|-][x|-][r|-][w|-][x|-]\r\n')
        except:
            self.assertTrue(False)
        
        # read the file permissions to verify their correctness
        fstats=os.stat(self.tmp_name)
        self.assertTrue(S_ISREG(fstats.st_mode))
        self.assertTrue(fstats.st_mode & S_IXUSR)
        
        self.child.terminate(force=True)

if __name__ == "__main__":
    unittest.main()
