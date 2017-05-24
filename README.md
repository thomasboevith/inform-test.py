# inform-test.py
Tool for testing Inform and Z-code stories.

Version: 0.1

Status: Under development

    inform-test.py 0.1 --- Testing of Inform and Z-code stories
    Usage:
      inform-test.py [-s <storyfile>] [-r <replayfile>] [-t <transcriptfile>]
                 [-T <testfile>] [-R] [-p] [-c] [-l <numlines>] [-u] [-n] [-H]
                 [-f | -F <width>] [-v ...]
      inform-test.py (-h | --help)
      inform-test.py --version

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

