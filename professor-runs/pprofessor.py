#!/usr/bin/env python2

"""
The batch job submitter for professor and lxplus
"""

devnull = open('/dev/null', 'w')

def LaunchJobs(hosts):
    from multiprocessing import Process
    from subprocess import call
    from progressbar import Bar, ETA, Percentage, ProgressBar
    from time import sleep
    from os import listdir
    from glob import glob

    #Now, take the directories in which we have the script:
    dirs = glob("mc/*")
    for directory in dirs:
        print directory
    subprocess = []

    servers = open(hosts[0], 'r').readlines()
    for n, directory in enumerate(dirs):
        line = servers[n%len(servers)]
        line.strip()
        index = line.find(" ")
        subprocess.append(Process(target=LaunchSsh, args=(line[:index], directory)))

    for process in subprocess:
        process.start()
    
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

def LaunchSsh(host, directory):
    from subprocess import call

    #Setting up and running the program:
    call("ssh " + host + " \' mkdir -p ~/pprofessor/" + directory + " \'", stdout = devnull, stderr = devnull, shell=True)
    call(['scp ' + directory + "/* " + host + ':~/pprofessor/' + directory], shell=True, stdout = devnull, stderr = devnull)
    call(["ssh " + host + " \' cd ~/pprofessor" + directory + " && batch.sh \'"], shell=True,stdout = devnull, stderr = devnull)

    #And copying it all up:
    call(["scp " + host + ":~/pprofessor" + directory + "/* " + directory], shell=True, stdout=devnull, stderr=devnull)



import sys
if sys.version_info[:3] < (2, 4, 0):
    print 'We need at least python 2.4.'
    system.exit(1)

#Now, take the hosts from the file:
hosts = []
from glob import glob
hosts = glob("*.hosts")
LaunchJobs(hosts)
