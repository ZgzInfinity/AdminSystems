#!/usr/bin/env python

# WARNING!!!
# this script should be run in a chrooted environment

import os
import pexpect
import random
import re
from subprocess import check_call
import string
import sys
from tempfile import mkstemp
import unittest

class TestPractica3(unittest.TestCase):

    # clean before every test, just in case something goes wrong
    def setUp(self):
        check_call(["./remove_possible_users.sh"])

    def tearDown(self):
        try:
            self.child.terminate(force=True)
        except:
            None

    def test_shebang(self):
        with open('./practica_3.sh') as f:
            first_line = f.readline().rstrip('\r\n')

            pattern=re.compile('#!/usr/bin/env\s+bash')
            # two options: #!/bin/bash or #!/usr/bin/env bash
            self.assertTrue((first_line == '#!/bin/bash') or
                    (pattern.match(first_line) != None))

    def test_required_commands(self):
        """ This test checks for required commands and options for useradd
        """

        def ensure_useradd_options(word_list):
            """ Given a list of words, this functions returns true if useradd includes
                options:
                -U
                -k /etc/skel
                -K UID_MIN=1000
             """

            idx=words_in_line.index('useradd')

            self.assertTrue('-U' in words_in_line[idx:],
                            msg={'useradd does not contain option -U'})

            if '-k' in words_in_line[idx:-1]:
                idx_k=words_in_line.index('-k')
                self.assertTrue(words_in_line[idx_k+1]=='/etc/skel',
                        msg={'useradd does not contain -k /etc/skel'})

            if '-K' in words_in_line[idx:-1]:
                idx_k=words_in_line.index('-K')
                self.assertTrue(words_in_line[idx_k+1]=='UID_MIN=1000',
                        msg={'useradd does not contain -K UID_MIN=1000'})

            return

        required_commands=frozenset(['useradd', 'userdel', 'usermod', 'chpasswd'])

        with open('./practica_3.sh') as f:
            script_words=set()
            for l in f:
                # skip commented lines
                if l[0] == '#':
                    continue
                words_in_line=l.split()
                script_words.update(w.rstrip('\n') for w in words_in_line)
                if 'useradd' in words_in_line:
                    ensure_useradd_options(words_in_line)

            self.assertTrue(script_words.issuperset(required_commands),
                    msg='The script does not contain all required commands')

    def test_number_arguments(self):
        self.child = pexpect.spawn('sudo /bin/bash ./practica_3.sh -a correct_user_list.txt extra_arg')
        try:
            self.child.expect_exact('Numero incorrecto de parametros\r\n')
        except:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_sudo(self):
        self.child = pexpect.spawn('/bin/bash ./practica_3.sh -a correct_user_list.txt')
        try:
            self.child.expect_exact('Este script necesita privilegios de administracion')
        except:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_invalid_argument(self):
        self.child = pexpect.spawn('sudo -- /bin/bash ./practica_3.sh -I correct_user_list.txt')
        try:
            self.child.expect_exact('Opcion invalida')
        except:
            self.assertTrue(False)

        try:
            self.assertFalse(self.child.expect(pexpect.EOF))
        except:
            self.assertTrue(False)

    def test_create_extra_backup(self):
        # risky test, it deletes a directory
        backup_dir='/extra/backup'

        if os.path.isdir(backup_dir):
            check_call(["sudo", "rm", "-rf", '{}'.format(backup_dir)])

        self.child = pexpect.spawn('sudo', ['--', '/bin/bash', './practica_3.sh', '-s', '/dev/null'])
        try:
            self.child.expect(pexpect.EOF)
        except:
            self.assertTrue(False)

        self.child.close()
        self.assertEqual(self.child.exitstatus, 0)
        self.assertTrue(os.path.isdir(backup_dir))


    def test_correct_user_list(self):
        self.child = pexpect.spawn('sudo -- /bin/bash ./practica_3.sh -a ./correct_user_list.txt')

        with open('./correct_user_list.txt', 'r') as f:
            for line in f:
                user, pwd, name = [ w.rstrip(' \n').lstrip(' ') for w in line.split(',') ]
                try:
                    expected_string="{} ha sido creado".format(name)
                    self.child.expect_exact(expected_string)
                except:
                    self.assertTrue(False)

                # read /etc/passwd
        try:
            self.assertFalse(self.child.expect(pexpect.EOF))
        except:
            self.assertTrue(False)

    def test_root_user(self):
        self.child = pexpect.spawn('sudo -- /bin/bash ./practica_3.sh -a incorrect_user_list_existing_root.txt')

        try:
            self.child.expect_exact('El usuario root ya existe')
        except:
            self.assertTrue(False)

        try:
            self.assertFalse(self.child.expect(pexpect.EOF))
        except:
            self.assertTrue(False)

    def get_new_user(self):
        """ This helper function returns a valid name for a new user
        """
        users=set()
        with open('/etc/passwd', 'r') as f:
            for line in f:
                users.add(line.split(':')[0])

        random_user_name=''.join(random.choice(string.ascii_letters+string.digits) for _ in range(8))
        while random_user_name in users:
            random_user_name=''.join(random.choice(string.ascii_letters+string.digits) for _ in range(8))
        return random_user_name

    def create_fake_user_file(self, user_name, fake_home=False):
        """ this function returns the name of a temporary file with a new user named user_name.
            The file has been closed and it is the caller responsability to remove the generated file.
        """

        tmp_handle, tmp_name = mkstemp()

        command_list = [ "sudo", "useradd", "-m" ]

        if fake_home:
            command_list += ["-d", "/tmp/{}".format(user_name)]

        command_list += ["{}".format(user_name)]
        check_call(command_list)

        os.write(tmp_handle, '{}, {}, {}\n'.format(user_name,
            'pwd' + user_name, 'name' + user_name))
        os.close(tmp_handle)

        return tmp_name

    def test_remove_user_uncommon_home(self):
        """ Remove a user whom $HOME is not in /home
        """
        random_user_name=self.get_new_user()
        tmp_name = self.create_fake_user_file(random_user_name, fake_home=True)

        # run the script
        self.child = pexpect.spawn('sudo', ['--', '/bin/bash', './practica_3.sh', '-s', tmp_name])
        try:
            self.child.expect(pexpect.EOF)
        except:
            os.unlink(tmp_name)
            self.assertTrue(False)

        # verify the user is not in the system and the backup has been created
        users=set()
        with open('/etc/passwd', 'r') as f:
            for line in f:
                users.add(line.split(':')[0])

        self.assertFalse(random_user_name in users)
        self.assertTrue(os.path.isfile('/extra/backup/' + random_user_name + ".tar"))
        os.unlink(tmp_name)

    def test_remove_existing_user(self):

        random_user_name=self.get_new_user()
        tmp_name = self.create_fake_user_file(random_user_name)

        # run the script
        self.child = pexpect.spawn('sudo', ['--', '/bin/bash', './practica_3.sh', '-s', tmp_name])
        self.child.logfile = sys.stdout
        try:
            self.assertFalse(self.child.expect(pexpect.EOF))
        except:
            os.unlink(tmp_name)
            self.assertTrue(False)

        # verify the user is not in the system and the backup has been created
        users=set()
        with open('/etc/passwd', 'r') as f:
            for line in f:
                users.add(line.split(':')[0])

        self.assertFalse(random_user_name in users)
        self.assertTrue(os.path.isfile('/extra/backup/' + random_user_name + ".tar"))
        os.unlink(tmp_name)

    def test_existing_user(self):

        random_user_name=self.get_new_user()
        tmp_name = self.create_fake_user_file(random_user_name)

        null_file=open(os.devnull, 'w')

        self.child = pexpect.spawn('sudo', ['--', '/bin/bash', './practica_3.sh', '-a', tmp_name])

        try:
            expected_string='El usuario {} ya existe'.format(random_user_name)
            self.child.expect_exact(expected_string)
        except:
            # ensure the newly created user is deleted
            check_call(["sudo", "userdel", "-r", "-f", "{}".format(random_user_name)],
                    stdout=null_file, stderr=null_file)
            self.assertTrue(False, msg='Expected: {}\nFound: {}'.format(expected_string, self.child.before))
            os.unlink(tmp_name)
            null_file.close()

        try:
            self.assertFalse(self.child.expect(pexpect.EOF))
        except:
            self.assertTrue(False)

        check_call(["sudo", "userdel", "-r", "-f", "{}".format(random_user_name)],
                    stdout=null_file, stderr=null_file)
        os.unlink(tmp_name)
        null_file.close()

if __name__ == "__main__":
    unittest.main()
