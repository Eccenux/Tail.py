#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import time
from utils.system import systemExec, printUnicode

if len(sys.argv)<2:
	print "Usage:"
	print "tail.py your.file.log"
	exit(1)
fname = sys.argv[1]

if sys.platform == 'win32':
	systemExec('set PYTHONIOENCODING=utf-8', totalSilence=True)	# bez tego Python szaleje po chcp
	systemExec('chcp 65001', totalSilence=True)

prev = ""
while True:
	time.sleep(1)
	with open(fname, 'rb') as fh:
		fh.seek(-1024, 2)
		last = fh.readlines()[-1]
		if last != prev:
			printUnicode(last.rstrip())
			prev = last
