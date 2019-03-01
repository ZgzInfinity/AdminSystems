#!/usr/bin/env python

import os
import pexpect
import random
import re
from shutil import rmtree
from stat import S_IXUSR
import string
import sys
import unittest

class TestPractica2_6(unittest.TestCase):

    def setUp(self):
        self.home=os.getenv("HOME")

    def tearDown(self):
        """ Nothing to finish """

    def test_shebang(self):
        with open('./practica2_6.sh') as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or
                    (pattern.match(first_line) != None))

    # helper function
    def is_exe(self, fname):
        fstats=os.stat(fname)
        return fstats.st_mode & S_IXUSR

    def find_bin_dir(self):
        """ Find the directory bin\w\w\w that is the least frequency modified

            Returns a tuple with a boolean value and a directory name
        """

        home=self.home
        pattern=re.compile('bin\w\w\w')
        candidate_dirs=[ os.path.abspath(home + '/' + d) for d in os.listdir(home) if os.path.isdir(os.path.abspath(home + '/' + d)) and pattern.match(d) ]
        # return the least recently modified directory
        if len(candidate_dirs) == 0:
            return True, ""
        else:
            return False, sorted(candidate_dirs, key=lambda d: os.stat(d).st_mtime)[0]

    def test_existing_dir(self):
        """ This test creates the destination directory if it does not exist
        """

        # if there is no bin_dir, we create one
        bin_dir_required, bin_dir=self.find_bin_dir()

        home=self.home

        if bin_dir_required:
            bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            while os.path.isdir(bin_dir):
                bin_dir=os.path.abspath(home + '/bin' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(3)))
            # directory creation
            os.mkdir(bin_dir)

        # count the number of executables files in current directory
        exec_files= [ f for f in os.listdir('./') if self.is_exe(f) and not f.startswith('.') ]

        try:
            self.child = pexpect.spawn('/bin/bash ./practica2_6.sh')
        except:
            self.assertTrue(False, msg='Error spanwing process')

        try:
            self.child.expect(pexpect.EOF)
        except:
            self.assertTrue(False, msg='Error expecing EOF')

        # insert all non-empty lines in a list
        output_lines = [ line for line in self.child.before.splitlines() if line ]

        dstdir_line=output_lines[0]
        output_lines.pop(0)
        expected_dstdir_line = 'Directorio destino de copia: {}'.format(bin_dir)
        self.assertTrue(expected_dstdir_line == dstdir_line, msg='Expected {}, Found: {}'.format(expected_dstdir_line, dstdir_line))

        # Do all matches
        for fname in exec_files:
            self.assertTrue('./{} ha sido copiado a {}'.format(fname, bin_dir) in output_lines, msg='{} not found'.format(fname))

        self.assertTrue('Se han copiado {} archivos'.format(str(len(exec_files))))
        self.assertTrue(len(output_lines) == (len(exec_files)+1))

        self.child.terminate(force=True)

        if bin_dir_required:
            rmtree(bin_dir)


    def test_dir_creation(self):
        """ This test forces the creation of the destination directory
        """

        # if there is no bin_dir, the script should create one
        bin_dir_required, bin_dir=self.find_bin_dir()

        # remove the directory if it exists, to ensure the creation by the script
        if not bin_dir_required:
            rmtree(bin_dir)
            bin_dir_required=True

        # count the number of executables files in current directory
        exec_files= [ f for f in os.listdir('./') if self.is_exe(f) and not f.startswith('.') ]

        try:
            self.child = pexpect.spawn('/bin/bash ./practica2_6.sh')
        except:
            self.assertTrue(False, msg='Error spanwing process')

        try:
            self.child.expect(pexpect.EOF)
        except:
            self.assertTrue(False, msg='Error expecing EOF')

        # insert all non-empty lines in a list
        output_lines = [ line for line in self.child.before.splitlines() if line ]

        if bin_dir_required:
            fline=output_lines[0]
            output_lines.pop(0) # remove first element list
            self.assertTrue(fline.startswith('Se ha creado el directorio '), msg='Invalid directory creation message')
            bin_dir=os.path.abspath(fline.split(' ')[-1])

        dstdir_line=output_lines[0]
        output_lines.pop(0)
        expected_dstdir_line = 'Directorio destino de copia: {}'.format(bin_dir)
        self.assertTrue(expected_dstdir_line == dstdir_line, msg='Expected {}, Found: {}'.format(expected_dstdir_line, dstdir_line))

        # Do all matches
        for fname in exec_files:
            self.assertTrue('./{} ha sido copiado a {}'.format(fname, bin_dir) in output_lines, msg='{} not found'.format(fname))

        self.assertTrue('Se han copiado {} archivos'.format(str(len(exec_files))))
        self.assertTrue(len(output_lines) == (len(exec_files)+1))

        self.child.terminate(force=True)

        if bin_dir_required:
            rmtree(bin_dir)

if __name__ == "__main__":
    unittest.main()
