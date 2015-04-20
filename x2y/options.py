# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import sys

from . import __version__


# put these string here so we can import them for testing
program_name = 'x2y'
usage_string = '%(prog)s [options] --from line-ending --to line-ending File [File ...]'
version_string = '%(prog)s %(version)s' % {'prog': program_name, 'version': __version__}
description_string = '''x2y: convert line ending between DOS, Mac (pre OS X) and Unix'''


def parse_opts(argv, stdin=None, stdout=None, stderr=None):
    choices = [u'dos', u'mac', u'unx']

    parser = argparse.ArgumentParser(
        prog=program_name,
        usage=usage_string,
        description=description_string,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--version',
        action='version',
        version=version_string
    )

    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='Turn on debug logging.'
    )

    parser.add_argument(
        '--debug-log',
        dest='debug_log',
        metavar='FILE',
        help='Save debug logging to FILE.'
    )

    parser.add_argument(
        '-b',
        '--backup',
        metavar='BACKUP EXTENTSION',
        help='Save a backup of the input file by renaming with BACKUP EXTENTSION. Ignored if the -o option is given. Default: %(default)s.'
    )

    parser.add_argument(
        '-d',
        '--directory',
        metavar='DIRECTORY',
        help='Save extracted text to DIRECTORY. Ignored if the -o option is given.'
    )

    parser.add_argument(
        '-f',
        '--from',
        dest='from_end',
        choices=choices,
        required=True,
        help='Line ending to convert from.'
    )

    parser.add_argument(
        '-o',
        '--output',
        metavar='FILE',
        help='Save extracted text to FILE. If not given, the output file is named the same as the input file but with a txt extension. The extension can be changed with the -e option. Files are opened in append mode unless the -X option is given.'
    )

    parser.add_argument(
        '-t',
        '--to',
        dest='to_end',
        choices=choices,
        required=True,
        help='Line ending to convert to.'
    )

    parser.add_argument(
        '-A',
        '--suppress-file-access-errors',
        default=False,
        action='store_true',
        help='Do not print file/directory access errors.'
    )

    parser.add_argument(
        'files',
        metavar='File',
        nargs='+',
        help='Files to convert'
    )

    # print('argv = %s' % argv)
    options = parser.parse_args(argv)

    # set up i/o options
    options.stdin = stdin or sys.stdin
    options.stdout = stdout or sys.stdout
    options.stderr = stderr or sys.stderr

    options.did_convert = False
    options.exit_status = 'not-set'

    return options

