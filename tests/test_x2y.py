#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import codecs
import os
import os.path
import pytest
import stat
import subprocess
import sys

if sys.version_info.major == 2:
    from StringIO import StringIO
else:
    from io import StringIO

import x2y.options
import x2y.x2y

class Cmd(object):
    def __init__(self, cmd, chdir='', indir='', stdin=None, stdout=None, stderr=None, exitcode=0, reference=None):
        self.cmd = cmd
        self.chdir = chdir
        self.indir = indir
        self.reference = reference
        # set and rewind stdin
        self.stdin = stdin
        if stdin:
            self.stdin = StringIO()
            for f in stdin:
                self.stdin.write(f + '\n')
            self.stdin.seek(0)
        self.stdout = stdout
        if stdout:
            if chdir:
                self.stdout = []
                for o in stdout:
                    self.stdout.append(os.path.join(chdir, o))
            elif indir:
                self.stdout = []
                for o in stdout:
                    self.stdout.append(os.path.join(indir, o))
        self.stderr = stderr
        self.exitcode = exitcode

    def __str__(self):
        return self.cmd

    def argv(self):
        args = []
        if self.chdir:
            args.extend(['-d', self.chdir])
        args.extend(self.cmd.split())
        return args

    def cmdline(self):
        args = ['x2y']
        args.extend(self.argv())
        return args

    def run(self):
        rval = Cmd(self.cmd)
        argv = self.argv()
        stdout = StringIO()
        stderr = StringIO()
        rval.exitcode = x2y.x2y.main(argv, stdin=self.stdin, stdout=stdout, stderr=stderr)
        stdout_value = stdout.getvalue()
        stderr_value = stderr.getvalue()
        if stdout_value:
            rval.stdout = stdout_value.strip().split('\n')
        if stderr_value:
            rval.stderr = stderr_value.strip().split('\n')
        stdout.close()
        stderr.close()
        if self.stdin:
            self.stdin.close()
        return rval

    def run_as_process(self):
        rval = Cmd(self.cmd)
        try:
            cmd = self.cmdline()
            os.environ['COVERAGE_PROCESS_START'] = '1'
            env = os.environ.copy()
            env['COVERAGE_FILE'] = '.coverage.%s' % (self.cmd.replace('/', '-').replace(' ', '-'))
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        except Exception as e:
            pytest.fail(msg='Cmd: run: exception running %s: %s' % (cmd, e))
        else:
            stdout, stderr = p.communicate()
            if stdout:
                rval.stdout = stdout.decode().strip().split('\n')
            if stderr:
                rval.stderr = stderr.decode().strip().split('\n')
            rval.exitcode = p.wait()
        return rval

    def outfile(self):
        argv = self.argv()
        i = 0
        while i < len(argv):
            if argv[i] == '-o':
                return argv[i + 1]
        return None
    
    def files_match(self):
        outfile = self.outfile()
        with open(outfile, 'rb') as fp:
            out_bytes = bytearray(fp.read())

        with open(self.reference, 'rb') as fp:
            ref_bytes = bytearray(fp.read())
        
        if out_bytes == ref_bytes:
            return True
        pyf.fail(msg='Files differ: %s %s' % (self.reference, outfile))
        return False


some_bad_option = '--some-bad-option'
usage_string_expanded = 'usage: %s' % (x2y.options.usage_string % {'prog': x2y.options.program_name})
some_bad_option_error_msg = '%(prog)s: error: unrecognized arguments: %(option)s' % {'prog': x2y.options.program_name, 'option': some_bad_option}


cmds = [
    # DOS
    Cmd('-o tests-out/mac.txt -f dos -t mac tests/in/dos.txt', reference='tests/in/mac.txt'),
    Cmd('-o tests-out/unx.txt -f dos -t unx tests/in/dos.txt', reference='tests/in/unx.txt'),
    
    # Mac
    Cmd('-o tests-out/mac.txt -f mac -t dos tests/in/mac.txt', reference='tests/in/dos.txt'),
    Cmd('-o tests-out/dos.txt -f mac -t unx tests/in/mac.txt', reference='tests/in/unx.txt'),
    
    # Unix
    Cmd('-o tests-out/dos.txt -f unx -t dos tests/in/unx.txt', reference='tests/in/dos.txt'),
    Cmd('-o tests-out/mac.txt -f unx -t mac tests/in/unx.txt', reference='tests/in/mac.txt'),
]

class TestCmd(object):
    @pytest.mark.parametrize('cmd', cmds)
    def test_cmd(self, cmd):
        r = cmd.run()
        assert r.stderr == cmd.stderr
        assert r.stdout == cmd.stdout
        assert r.exitcode == cmd.exitcode
        assert cmd.files_match()


if __name__ == '__main__':
    pytest.main()


