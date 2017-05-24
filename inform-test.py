#!/usr/bin/python
import base64
import difflib
import docopt
import hashlib
import humanize
import logging
import os
import re
import sys
import tempfile
import time
import subprocess

version = '0.1'

__doc__ = """inform-test.py {version} --- Testing of Inform and Z-code stories
Usage:
  {filename} [-s <storyfile>] [-r <replayfile>] [-t <transcriptfile>]
             [-T <testfile>] [-R] [-p] [-c] [-l <numlines>] [-u] [-n] [-H]
             [-f | -F <width>] [-v ...]
  {filename} (-h | --help)
  {filename} --version

Options:
  -s <storyfile>            Story file.
  -r <replayfile>           Replay file (file of commands).
  -t <transcriptfile>       Transcript file (file to save output in).
  -T <testfile>             Test file (transcript to test output against).
  -R                        Random seed (else use fixed seed).
  -p                        Print test results.
  -u                        Produce a unified format diff (default).
  -n                        Produce a ndiff format diff.
  -c                        Produce a context format diff.
  -l <numlines>             Set number of context lines [default: 0].
  -H                        Produce HTML diff (use -c and -l in conjunction).
  -f                        Do not fold text.
  -F <width>                Fold text at width (default) [default: 80].
  --version                 Show version.
  -v                        Print info (-vv for printing lots of info (debug)).

Copyright (C) 2017 Thomas Boevith

License: GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it. There is NO
WARRANTY, to the extent permitted by law.
""".format(filename=os.path.basename(__file__), version=version)


def run_command(command):
    log.info('Running command: %s' % ' '.join(command))
    try:
        returncode = subprocess.call(' '.join(command), shell=True)
    except Exception as ex:
        log.exception('Exception: %s' % ex)
        sys.exit(1)

    if returncode != 0:
        log.error('Running command unsuccessful: %s' % command)
        sys.exit(1)
    else:
        log.info('Running command successful: %s' % command)
        command.append(args['-t'])

    return returncode


if __name__ == '__main__':
    start_time = time.time()
    args = docopt.docopt(__doc__, version=str(version))

    log = logging.getLogger(os.path.basename(__file__))
    formatstr = '%(asctime)-15s %(name)-17s %(levelname)-5s %(message)s'
    if args['-v'] >= 2:
        logging.basicConfig(level=logging.DEBUG, format=formatstr)
    elif args['-v'] == 1:
        logging.basicConfig(level=logging.INFO, format=formatstr)
    else:
        logging.basicConfig(level=logging.WARNING, format=formatstr)

    log.debug('%s started' % os.path.basename(__file__))
    log.debug('docopt args=%s' % args)

    if args['-s'] is None or args['-r'] is None:
        log.error('Please specify story, replay (and optionally a transcript' +
                  'and test file).')
        sys.exit(1)

    if not args['-p'] and not args['-t']:
        log.error('Please choose print or transcript file.')
        sys.exit(1)

    if args['-p'] and not args['-t']:
        args['-t'] = 'tmpfile.inform-test.tmp'

    interpreter = '~/bin/bocfel'
    command = [interpreter]
    if args['-r']:
        command.append('-r -R %s' % args['-r'])
    if not args['-R']:
        command.append('-z 123')
    if args['-t']:
        if args['-f']:
            command.append('-t -l -y -T %s' % args['-t'])
        else:
            command.append('-t -l -y -T %s' % args['-t']+'.unfold')
    if args['-s']:
        command.append(args['-s'])

    command.append('> /dev/null 2>&1')

    run_command(command)

    if args['-F'] and not args['-f']:
        command = ['fold']
        command.append('-s')
        command.append('-w%s' % args['-F'])
        command.append(args['-t']+'.unfold')
        command.append('>|')
        command.append(args['-t'])
        run_command(command)

    if args['-p'] and (not args['-t'] or not args['-T']):
        with open(args['-t']) as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == '>':
                    print("\033[0;31;48m%s" % line),
                else:
                    print("\033[0;38;48m%s" % line),

    if args['-T']:
        with open(args['-T']) as file:
            test = file.readlines()
        with open(args['-t']) as file:
            transcript = file.readlines()

        d = difflib.Differ()
        result = list(d.compare(test, transcript))

        fromfile = args['-T']
        tofile = args['-t']
        fromdate = time.ctime(os.stat(fromfile).st_mtime)
        todate = time.ctime(os.stat(tofile).st_mtime)
        n = int(args['-l'])

        if args['-H']:
            diff = difflib.HtmlDiff().make_file(test, transcript, fromfile,
                                                tofile, context=args['-c'],
                                                numlines=n)
        elif args['-n']:
            diff = difflib.ndiff(test, transcript)
        elif args['-c']:
            diff = difflib.context_diff(test, transcript, fromfile, tofile,
                                        fromdate, todate, n=n)
        else:
            # Default diff method
            diff = difflib.unified_diff(test, transcript, fromfile, tofile,
                                        fromdate, todate, n=n)

        if args['-p']:
            for line in diff:
                if line[0] == '+':
                    print("\033[0;33;48m%s" % line),
                elif line[0] == '-':
                    print("\033[0;34;48m%s" % line),
                elif line[0] == '?':
                    print("\033[0;31;48m%s" % line),
                else:
                    print("\033[0;38;48m%s" % line),

    log.debug('Processing time={0:.2f} s'.format(time.time() - start_time))
    log.debug('%s ended' % os.path.basename(__file__))
