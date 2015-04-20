#!/usr/bin/env python
# -*- coding: utf-8 -*-
# x2y: convert line ending between DOS, Mac and Unix
# https://github.com/bnomis/x2y
# (c) Simon Blanchard

import os
import os.path
import sys


from .logger import error, init_logging


def writerr(options, line, exception=None, set_exit_status=True):
    if set_exit_status:
        options.exit_status = 'error'
    options.stderr.write(line + '\n')
    if exception:
        error(line, exc_info=True)


def writerr_file_access(options, line, exception=None):
    if not options.suppress_file_access_errors:
        writerr(options, line, exception=exception, set_exit_status=False)


def check_file_access(options, path):
    # check file exists
    # will return true even for broken symlinks
    if not os.path.lexists(path):
        writerr_file_access(options, 'File does not exist: %s' % path)
        return False

    # double check for broken symlinks
    if os.path.islink(path):
        if not os.path.exists(path):
            writerr_file_access(options, 'Broken symlink: %s' % path)
            return False

    # check can open for read
    if os.path.isdir(path):
        if not os.access(path, os.R_OK):
            writerr_file_access(options, 'Directory is not readable: %s' % path)
            return False
    else:
        try:
            fp = open(path)
        except Exception as e:
            writerr_file_access(options, 'File is not readable: %s' % path)
            error('check_file_access: exception for %s: %s' % (path, e), exc_info=True)
            return False
        else:
            fp.close()

    return True


def make_outdir(options):
    if options.directory:
        if not os.path.exists(options.directory):
            path = ''
            for p in options.directory.split('/'):
                path = os.path.join(path, p)
                if not os.path.exists(path):
                    try:
                        os.mkdir(path)
                    except Exception as e:
                        writerr(options, 'Exception making directory: %s' % path, exception=e)


def output_filename(options, filename):
    if options.output:
        return options.output

    if options.directory:
        make_outdir(options)
        base = os.path.basename(filename)
        return os.path.join(options.directory, base)

    return filename


def backup(options, path):
    toname = path + '.' + options.backup
    os.rename(path, toname)


def x2y_bytes(options, in_bytes):
    start = pos = 0
    from_length = len(options.from_bytes)
    out_bytes = bytearray()
    in_length = len(in_bytes)
    while start < in_length:
        pos = in_bytes.find(options.from_bytes, start)
        
        if pos == -1:
            break
        out_bytes.extend(in_bytes[start:pos])
        out_bytes.extend(options.to_bytes)
        line_length = pos - start + from_length
        start += line_length
    if start < in_length - 1:
        out_bytes.extend(in_bytes[start:])
    return out_bytes


def x2y_file(options, path):
    if not check_file_access(options, path):
        return

    with open(path, 'rb') as fp:
        in_bytes = bytearray(fp.read())

    out_bytes = x2y_bytes(options, in_bytes)

    if in_bytes != out_bytes:
        options.did_convert = True

        outname = output_filename(options, path)
        if outname == path and options.backup:
            backup(options, path)

        with open(outname, 'wb') as fp:
            fp.write(out_bytes)


def x2y(options):
    for f in options.files:
        x2y_file(options, f)


def main(argv, stdin=None, stdout=None, stderr=None):
    from .options import parse_opts
    exit_statuses = {
        'converted': 0,
        'no-convert': 1,
        'error': 2,
        'not-set': -1
    }
    line_endings = {
        'dos': u'\r\n',
        'mac': u'\r',
        'unx': u'\n'
    }

    options = parse_opts(argv, stdin=stdin, stdout=stdout, stderr=stderr)
    if not options:
        return exit_statuses['error']

    # convert from/to same thing does nothing
    if options.from_end == options.to_end:
        return exit_statuses['no-convert']

    options.from_bytes = bytearray(line_endings[options.from_end], 'utf8')
    options.to_bytes = bytearray(line_endings[options.to_end], 'utf8')

    init_logging(options)

    # do the conversions
    try:
        x2y(options)
    except KeyboardInterrupt:
        writerr(options, '\nInterrupted')
    except Exception as e:
        writerr(options, 'x2y exception', exception=e)
        options.exit_status = 'error'

    if options.exit_status == 'not-set':
        if options.did_convert:
            options.exit_status = 'converted'
        else:
            options.exit_status = 'no-convert'

    return exit_statuses[options.exit_status]


def run():
    sys.exit(main(sys.argv[1:]))


if __name__ == '__main__':
    run()


