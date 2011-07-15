#!/usr/bin/env python2

"""
The batch job submitter. Submits the job to the hosts specified in the .hosts file 
and launches the job with the specified number of threads.
Alternatively another input file can be given from command line
"""
devnull = open('/dev/null', 'w')

def LaunchJobs(hosts):
    from multiprocessing import Process
    from subprocess import call 
    from progressbar import Bar, ETA, Percentage, ProgressBar
    from time import sleep 

    call(['mkdir output2/'], shell=True, stdout=devnull, stderr=devnull)

    subprocess = []
    for host in hosts:
        with open(host, 'r') as file:
            for n, line in enumerate(file):
                line = line.strip()
                index = line.find(" ")
                subprocess.append(Process(target=LaunchSsh, args=(line[:index], line[index:].strip(),n)))
    for process in subprocess:
        process.start()
    
    # A 'progress' bar
    counter = 0
    widgets = ['Computing on the grid:', Percentage(), ' ', Bar(marker='#', left='[', right=']'), ' ', ETA(), ' ']
    pbar = ProgressBar(widgets = widgets, maxval=len(subprocess))
    while counter < len(subprocess):
        counter = 0
        sleep(0.5)
        for process in subprocess:
            if not process.is_alive():
                counter += 1
        pbar.update(counter)
    pbar.finish()

def LaunchSsh(host, threads, n):
    from subprocess import call

    call("ssh "+ host + " \' mkdir ~/batchJob/" + str(n) + " \'", stdout = devnull, stderr = devnull, shell=True)
    
    call(['scp make.py *.cc *.params ' + host + ':~/batchJob/' + str(n)], shell=True , stdout = devnull, stderr = devnull)
    
    call(["ssh " + host + " \'  cd ~/batchJob/" + str(n) + "  && ./make.py MC_TTBAR2.cc -P params.params -n 5000 --prefix " + str(n) + " --threads " + threads + "\'"], shell=True, stdout = devnull, stderr = devnull)

    #Copying all the files to the main host:
    call(["scp " +  host + ":~/batchJob/" + str(n) + "/*.aida output2/"], shell=True, stdout = devnull, stderr = devnull)

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
else:
    hosts = [] * 1
    hosts[0] = opts.HOSTS
    LauchJobs(hosts)

