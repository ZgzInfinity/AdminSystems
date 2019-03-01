#!/usr/bin/env python

import os
import pexpect
import random
import re
import string
import sys
from tempfile import mkstemp
import unittest

class TestPractica2_1(unittest.TestCase):

    def setUp(self):
        self.child = pexpect.spawn('/bin/bash ./practica2_1.sh')
        # self.child.logfile = sys.stdout

        # create a temporal file 
        self.tmp_handle, self.tmp_name = mkstemp(prefix='with_space ')

    def tearDown(self):
        self.child.terminate(force=True)
        # delete file
        os.close(self.tmp_handle)
        os.unlink(self.tmp_name)

    def test_shebang(self):
        with open('./practica2_1.sh') as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or 
                    (pattern.match(first_line) != None), msg='Invalid shebang')

    def test_no_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ')
        os.chmod(self.tmp_name, 0000)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: ---\r\n'.format(self.tmp_name))
        except:
            self.assertTrue(False, msg='Incorrect permit. Expected value: ---')
        self.assertTrue(True)
    
    def test_exec_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ')
        os.chmod(self.tmp_name, 0100)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: --x\r\n'.format(self.tmp_name))
        except:
            self.assertTrue(False, msg='Incorrect permit. Expected value: --x')
        self.assertTrue(True)

    def test_read_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ')
        os.chmod(self.tmp_name, 0400)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: r--\r\n'.format(self.tmp_name))
        except:
            self.assertTrue(False, msg='Incorrect permit. Expected value: r--')
        self.assertTrue(True)
    
    def test_read_write_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ')
        os.chmod(self.tmp_name, 0600)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: rw-'.format(self.tmp_name))
        except:
            self.assertTrue(False, msg='Incorrect permit. Expected value: rw-')
        self.assertTrue(True)
    
    def test_read_write_exec_permit(self):
        self.child.expect('Introduzca el nombre del fichero: ')
        os.chmod(self.tmp_name, 0700)
        self.child.sendline(self.tmp_name)
        try:
            self.child.expect('Los permisos del archivo {} son: rwx'.format(self.tmp_name))
        except:
            self.assertTrue(False, msg='Incorrect permit. Expected value: rwx')
        self.assertTrue(True)

    def test_read_invalid_filename(self):
        fname=''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16))
        while os.path.isfile(fname):
            fname=''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16))

        try:
            self.child.expect('Introduzca el nombre del fichero: ')
            self.child.sendline(fname)
            self.child.expect('{} no existe'.format(fname))
        except:
            self.assertTrue(False, msg='Invalid output. Expected output: {} no existe'.format(fname))
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
