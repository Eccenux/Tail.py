#!/usr/bin/env python
import os,sys
import shlex

# Copy stdout to file given by name
# Note! You should call .close() when you want to stop copying to file
# TODO: printUnicode not working when Tee is created
# TODO: print is not copied to stderr from systemExec output.
class Tee(object):
	def __init__(self, name, mode):
		self.file = open(name, mode)
		self.stdout = sys.stdout
		sys.stdout = self
	def __exit__(self, type, value, traceback):
		self.close()
	def close(self):
		sys.stdout = self.stdout
		self.file.close()
	def write(self, data):
		self.file.write(data)
		self.stdout.write(data)

##
# Functions
##
def printUnicode(utfString):
	"""
	http://stackoverflow.com/questions/13452916/why-do-i-get-ioerrors-when-writing-unicode-to-the-cmd-with-codepage-65001
	"""
	os.write(sys.stdout.fileno(), utfString+"\n")
	#sys.stdout.write(utfString+"\n")

def pauseWithInput(customInfo):
	if len(customInfo):
		printUnicode(customInfo)
	else:
		printUnicode("Press ENTER to continue.")
	raw_input()

def pauseWait(delay):
	printUnicode("Waiting " + str(delay) + " seconds.")
	from time import sleep
	sleep(delay)

def systemExec(command, returnOutput=False, showCommand=True, verbose=True, totalSilence=False):
	"""
		Run system command and display results
		
		@param totalSilence ignores showCommand and verbose parameters.
		
		@throws exception when command returned non-zero result
		@note PN2 will show ouput of all commands before print statements
	"""
	## os.system is passe...
	# os.system(command)
	
	if showCommand and not totalSilence:
		print "$> " + command
	
	import subprocess
	retcode = -1
	output = ""
	try:
		if not returnOutput:
			if totalSilence:
				with open(os.devnull, "w") as fnull:
					retcode = subprocess.call(command, stdout = fnull, shell=True)
			else:
				retcode = subprocess.call(command, shell=True)
		else:
			if sys.platform == 'win32':
				proc = subprocess.Popen(command, stdout=subprocess.PIPE)
			else:
				# Popen needs array input on Linux
				args = shlex.split(command)
				proc = subprocess.Popen(args, stdout=subprocess.PIPE)
			output = proc.communicate()[0]
			if not totalSilence:
				print output
			retcode = proc.returncode
	
		if not totalSilence:
			if retcode < 0:
				print >>sys.stderr, "Command was terminated by signal", -retcode
			elif retcode > 0:
				print >>sys.stderr, "Command returned non-zero code ", -retcode
			elif verbose:
				print >>sys.stderr, "Command seem to have returned successfully"
	except OSError, e:
		print >>sys.stderr, "Execution failed: ", e
		
	if retcode <> 0:
		raise Exception("[ERROR] Failed to run a command")
		
	return output

# test when run directly
if __name__ == '__main__':
	if sys.platform == 'win32':
		# windows
		systemExec ('echo "123"')
		
		# utf8
		systemExec('set PYTHONIOENCODING=utf-8', totalSilence=True)
		
		# this doesn't really work - echo is not a file
		#print systemExec ('echo "123"', True)
		#print "ret: " + ret
		
		ret = systemExec(r"svn status ..\workspace\1\molik_svn_compiled", True)
		print "ret :" + ret
		ret = systemExec(r"svn status ..\workspace\1\molik_svn_compiled")
		print "ret :" + ret
	else:
		# linux
		systemExec ("echo '123'")
		print systemExec ("echo '123'", True)
	