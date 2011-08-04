"""progressbar.py\n

"""


from sys import stdout
from math import ceil

class ForLoopProgressBar:
    """
    A class that represents a progress bar object suitable for visualizing
    progress in a for loop.
    """
    def __init__(self, start, stop, windowsize=50, name='loading '):
        self._start = start
        self._stop = stop
        self._progress = 0
        self._bar = ""
        self._name = name
        self._windowsize = windowsize
        self._interval = self.getInterval(start, stop, windowsize)

    def getInterval(self, start, stop, windowsize):
        """ calculate the number of iterations in the loop before progress bar
        grows by one unit
        """
        if stop == start:
            return 1./windowsize
        else:
            return float(stop - start)/float(windowsize)


    def display(self, string):
        """ write directly to stdout """
        stdout.write('\r' + string)
        stdout.flush()


    def update(self, current):
        """ this does all the work. has to be called before/after each
        iteration
        """
        if self._progress + 1 == self._stop:
            self.cleanup()
        else:
            if current + 1 >= len(self._bar)*self._interval:
                if (self._stop - self._start) < self._windowsize:
                    self._bar += int(ceil(1./self._interval))*"="
                else:
                    self._bar += "="
                self.display(self._name +'[%s]'%(self._bar + (self._windowsize-len(self._bar))*' '))
            else:
                pass
        self._progress += 1

    def cleanup(self):
        """ self explaining """
        self.display((' ' * (self._windowsize + len(self._name) + 2)) + '\r')
