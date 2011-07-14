#!/usr/bin/env python2

"""
The batch job submitter. Submits the job to the hosts specified in the .hosts file 
and launches the job with the specified number of threads.
Alternatively another input file can be given from command line
"""
def LaunchJobs(hosts):
	for host in hosts:
		with open(host, 'r') as file:
			for line in file:
				line = line.strip()
				index = line.find(" ")
				LaunchSsh(line[:index], line[index:].strip())

def LaunchSsh(host, threads):
	from os import system
	output = system("ssh " + host + " \' mkdir batchJob \'")
	print output
	
	output = system("scp make.py " + host + ":~/batchJob")
	print output
	
	output = system("ssh " + host + " \' cd batchJob ; ./make.py --threads " + threads + "\'")
	print output

def StatusPoll(hosts, statusFile):
	for host in hosts:
		from os import system
		output = system("scp " + host + ":batchJob/" + statusFile + " .status")
		print output

		status = open(".status", "r")
		return "Status of " + host + " is " + str(status.readline())
		

import sys
if sys.version_info[:3] < (2, 4, 0):
	print 'At least python 2.4 is required to launch this script.'
	system.exit(1)

# A bit of parsing:
from optparse import OptionParser
parser = OptionParser(usage=__doc__, version='1')

parser.add_option('-f', '--hosts', dest='HOSTS', default=None, help="Specifies a custom hosts file")
(opts, args) = parser.parse_args()

import time
# Check if the custom hosts file was set by the user, if not, use autodetect
hosts = []
if not opts.HOSTS:
	from glob import glob
	hosts = glob("*.hosts")
	LaunchJobs(hosts)
	time.sleep(15)
	print StatusPoll(hosts, ".status")
else:
	hosts = [] * 1
	hosts[0] = opts.HOSTS
	LauchJobs(hosts)
	time.sleep(15)
	print StatusPoll(hosts, ".status")
