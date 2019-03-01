#!/usr/bin/env python

# WARNING!!!
# this script should be run in a chrooted environment

import os
from pexpect import pxssh
import random
import re
from subprocess import check_call
import string
import sys
from tempfile import mkstemp
import unittest

class TestPractica4(unittest.TestCase):


    # clean before every test, just in case something goes wrong
    def setUp(self):
        self.IPs = ['192.168.56.2', '192.168.56.3']

    def tearDown(self):
        pass

    def test_shebang(self):
        with open('./practica_4.sh') as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or 
                    (pattern.match(first_line) != None))

    def test_connectivity(self):
        """ Check whether the expected nodes are alive
        """
        
        for ip in self.IPs:
            try:
                s=pxssh.pxssh(options={"PasswordAuthentication" : "no"})
                s.login(ip, "as", ssh_key="~/.ssh/id_as_ed25519")
                # send inocuous command
                s.sendline('true')
                self.assertTrue(s.prompt())
                s.logout()
            except pxssh.ExceptionPxssh as e:
                print 'Login to {} failed!, error: {}'.format(ip, e)
                self.assertTrue(False)
        self.assertTrue(True)

    def test_correct_sudo_config(self):
        """ Read sudo config file and check if root login is disabled
        """

        pattern = re.compile('^\s*PermitRootLogin\s+no')
        # remove escaped characters in case the string supports color
        rem_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        
        for ip in self.IPs:
            try:
                s=pxssh.pxssh(options={"PasswordAuthentication" : "no"})
                s.login(ip, "as", ssh_key="~/.ssh/id_as_ed25519")
                s.sendline('grep -E "^\s*PermitRootLogin\s+no" /etc/ssh/sshd_config')
                self.assertTrue(s.prompt())
                line_to_match=rem_escape.sub('', s.before.splitlines()[-1])
                self.assertTrue(pattern.match(line_to_match) != None, "Error in machine {}".format(ip))
                s.logout()
            except pxssh.ExceptionPxssh as e:
                self.assertTrue(False)
                print s.before
                print 'Sudo verification or login to {} failed!, error: {}'.format(ip, e)

        self.assertTrue(True)


    # def test_no_root
    # find PermitRootLogin no in /etc/sshd_config

    # def test_try_root_ssh

if __name__ == "__main__":
    unittest.main()
