"""config.py

Central configuration class L{Config}.

See
U{https://projects.hepforge.org/professor/trac/wiki/CentralConfiguration}
for more information and usage example.
"""

import logging
import sys
import traceback
import re
import types
import optparse

def convList(s):
    """Tokenize a config string and return tokens stored in a list.
    E.g., 'file.1,file.2' will be returned as [file.1, file.2].
    None will be returned if argument is None.
    """
    if s is None:
        return None
    try:
        tokens = s.split(',')
        return tokens
    except:
        raise StandardError("Must specify string")

def convParamList(s):
    """Convert a config string to a parameter dictionary.

    Converts a string of the form 'PARNAME1:PARVAL1,PARNAME2:PARVAL2...'
    to a dictionay
    {PARNAME1 : float(PARVAL1), PARNAME2 : float(PARVAL2)} .

    None will be returned if argument is None.
    """
    if s is None:
        return None
    s = s.strip()
    s = s.split(',')
    s = [pair.split('=') for pair in s]
    d = dict()
    for pname, pval in s:
        d[pname] = float(pval)
    return d


class Config(object):
    """singleton config and logging facility class

    The central configuration and logging facility. It's done as a singleton
    class. The idea is to call the constructor in submodules without a
    filename argument and register the module with a default configuration.
    Then in a script/program the constructor is called with a filename
    argument. Any option set in the config file overwrites a default value.

    Command line parsing is also possible. See L{initModule} how to do this.
    A '--config' option is automatically added. It takes the path to a
    configuration file to load before the commandline is parsed. So the
    config process is as follows:
        1. Init modules and set default values.
        2. Overwrite default values with those from a given config file, e.g.
           via the --config option.
        3. Overwrite with values from command line.

    Subpackage example (e.g. in .../__init__.py)

        >>> # import part
        >>> from professor.tools.config import Config as _C
        >>> # more imports
        ...
        >>> # now init our module and store the module's logger
        >>> _logger = _C().initModule('foo',
        >>>                  {
        >>>                   # this option is of int-type, recognized on the
        >>>                   # commandline and defaults to 1
        >>>                  'bar option':(1, int, True, "help for bar"),
        >>>                   # this option is of bool-type, not recognized
        >>>                   # on the commandline and defaults to False
        >>>                   'spam option':(False, _C().convBool)
        >>>                  })

    Script example:

        >>> # import part
        >>> from professor.tools.config import Config as _C
        >>> # more imports
        ...
        >>> conf = _C()
        >>> # init any options via initModule or initOption
        >>> conf.initOption('my script', 'foo option', 'unset',
        >>>                 cmdline=True, help="an option for 'my script'")
        ...
        >>> # update the values from commandline
        >>> # if --config FILE is given, parse FILE before command line
        >>> # parsing
        >>> opts, args = conf.parseCommandline()
        >>> # if we handle arguments do it here:
        ...

    Logging options recognized for each module:
        - 'loglevel': (debug|info|warning|error|critical)
        - 'logfiles': comma separated list with filenames to log to. '-' and
          'stderr' are treated in a special way:
              - '-' : turn on propagation, i.e. log messages are sent to the
                parent logger, too.
              - 'stderr' : log to the script's stderr

    Configuration values can be retrieved  via the
    L{getOption}('submodule name', 'option name') method.

    See U{http://www.python.org/download/releases/2.2.3/descrintro} for the
    singleton stuff.
    """
    __loglevels = {'debug' : logging.DEBUG, 'info' : logging.INFO,
                   'warning' : logging.WARNING, 'error' : logging.ERROR,
                   'critical' : logging.CRITICAL
                  }
    __sectionre = re.compile(r".*\[(?P<MODULE>.*)\]\s*(?:#.*)?")
    __optionre = re.compile(r"\s*(?P<NAME>[^=]*\S)\s*=\s*(?P<VALUE>.*[^\\])\\?")
    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get("__it__")
        if it is None:
            it = cls.__it__ = object.__new__(cls)
            it.__singleton_init()
        return it

    def __singleton_init(self):
        """init method called only once during the whole program from __new__"""
        # modules layout: nested dicts:
        # { module name :
        #       { option name : (value, conv*, cmdline*, help* } }
        #  *: may be None
        self.__modules = {}
        self.__filename = None

        self.__op = optparse.OptionParser()
        self.__op.add_option('--config', help="configuration file")
        # self.__stderr = logging.StreamHandler()
        #self.__stderr.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
        # self.__stderr.setFormatter(logging.Formatter('%(name)s: %(message)s'))

        # init global stuff e.g. logging fall back values
        self.initModule('global', {'logfiles' : 'stderr', 'loglevel' : 'info'})
        self.addExceptionHook(self.loggingExceptionHook)

    def __init__(self, filename=None):
        if filename is None:
            return
        if self.__filename is not None:
            raise RuntimeError(("Config already read from file '%s':"
                                " bad file '%s'")%(self.__filename,
                                                   filename))
        try:
            self.__filename = filename
            self.__parseFile()
            self.__op.remove_option('--config')
        except IOError, e:
            self.getLogger().error("failed to load config from file '%s'"
                                   " %s"%(filename, e))
            self.__filename = None

    def __str__(self):
        return "central config for modules: %s; loaded from file '%s'"%(
                self.__modules.keys(), self.__filename)

    def addExceptionHook(self, newhook):
        old = sys.excepthook
        def new(ex_cl, ex_i, tr):
            newhook(ex_cl, ex_i, tr)
            old(ex_cl, ex_i, tr)
        sys.excepthook = new

    def loggingExceptionHook(self, ex_cl, ex_i, tb):
        l = self.getLogger()
        l.error('Uncaught exception:')
        l.error(''.join(traceback.format_exception(ex_cl, ex_i, tb)))

    def __parseFile(self):
        self.getLogger().debug("parsing file '%s'"%(self.__filename))
        currentmodule = None
        f = open(self.__filename)
        for line in f:
            line = line.strip()
            if line.startswith('#') or len(line) == 0:
                continue
            m = self.__sectionre.match(line)
            if m is not None:
                currentmodule = m.groupdict()['MODULE']
            else:
                if currentmodule is None:
                    raise ValueError("Setting option before [module] line.")
                m = self.__optionre.match(line)
                m = m.groupdict()
                optname = m['NAME']
                value = m['VALUE']
                if line.endswith("\\"):
                    for line2 in f:
                        line2 = line2.strip()
                        if line2.endswith("\\"):
                            value += line2[:-1]
                        else:
                            value += line2
                            break
                self.setOption(currentmodule, optname, value, True)

    def write(self, f, close=True):
        if type(f) in types.StringTypes:
            f = open(f, 'w')
        f.write(u"# professor config file\n"
                u"# format is the same as accepted from Python standard\n"
                u"# library module ConfigParser\n")
        for modname, moddict in self.__modules.iteritems():
            f.write(u"[%s]\n"%(modname))
            for optname, opt in moddict.iteritems():
                # write help
                if opt[3] is not None:
                    f.write(u"# %s\n"%(opt[3]))
                val = opt[0]
                if type(val) == float:
                    f.write(u"%s = %g\n"%(optname, val))
                else:
                    f.write(u"%s = %s\n"%(optname, val))
            f.write("\n")
        if close:
            f.close()

    def initModule(self, module, moddict):
        """Init configuration section for module and return a handle to the
        modules logger.

        Option Values:
            1. A single string
            2. A list with length between 1 and 4. List items are used as
               following:
                1. option value
                2. conversion function: used to convert a string to the real
                   value, e.g. C{int},C{float},L{convBool}
                3. cmdline: use a string or C{True} to create a command line
                   switch for this option. If it's a string, this is used as
                   option string. It must not begin with '--' and the user
                   has to take care that it's valid for use with
                   optparse.OptionParser. If C{True} the option string is
                   created from the option name.
                4. help: a string used for command line help.

               Values for 2. to 4. may be None or even not there.


        @param module: name of the module
        @param moddict: dictionary with option name - option value pairs
        """
        if self.__modules.has_key(module):
            raise RuntimeError("Module '%s' inited twice!" % (module))

        def secureindex(l, i):
            try:
                return l[i]
            except IndexError:
                return None

        # t = {}
        for name, opts in moddict.iteritems():
            if type(opts) in (list, tuple):
                # val = opts[0]
                # conv = secureindex(opts, 1)
                # cmdline = secureindex(opts, 2)
                # help = secureindex(opts, 3)
                # t[name] = [val, conv, cmdline, help]
                self.initOption(module, name, opts[0],
                        secureindex(opts, 1),
                        secureindex(opts, 2),
                        secureindex(opts, 3))
            # this is for backwards compatibility
            else:
                self.initOption(module, name, opts)
        # self.__modules[module] = t
        return self.configLogger(module)


    def initOption(self, module, name, val,
            conv=None, cmdline=None, help=None):
        """Initialize a new option 'name' in 'module'.

        If module does not exist, it's silently created.

        @param module: the module name
        @param name: the option name
        @param val: the default option value
        @param conv: If not None, a conversion function used to convert a
            string to the real value, e.g. C{int},C{float},L{convBool}
            during config file and commmand line parsing.
        @param cmdline: If not None, a string used as option string. Must
            not begin with '--'. The user must take care that it's valid for
            use with optparse.OptionParser . If not a string type but
            evaluates to C{True}, then a option string is created from the
            option name (see L{str4optparse}).
        @param help: If not None, a string used for command line help. A
            default hint is added.
        """
        if not self.__modules.has_key(module):
            self.__modules[module] = {}
        mdict = self.__modules[module]

        if mdict.has_key(name):
            raise RuntimeError("Option '%s.%s' inited twice!"%(module, name))

        if cmdline:
            if type(cmdline) not in types.StringTypes:
                cmdline = self.str4optparse(name)
            if help:
                self.__op.add_option('--' + cmdline,
                                     help="%s (default: %s)"%(help, val))
            else:
                self.__op.add_option('--' + cmdline,
                                     help="(default: %s)"%(val))
            cmdline = cmdline.replace('-', '_')
        mdict[name] = [val, conv, cmdline, help]

    @staticmethod
    def str4optparse(s):
        """Little helper to get optparse long option strings."""
        for c in ('-', ' '):
            s = s.replace(c, '_')
        return s

    def setOption(self, module, name, value, overwrite=True):
        """Set option 'name' in 'module'.

        If 'module' does not exist, it's silently created. If option does
        not exist, it's silently created as non-commandline string-type
        option (conv, cmdline, help are None in initOption call).

        @param module: the module name
        @param name: the option name
        @param value: The new option value. If it's a string and a
            conversion function was set for this option, this function is
            applied on value and the result is inserted.
        @param overwrite: switch to turn overwriting options on/off.
        """
        # print "setting option %s.%s = %s"%(module, name, value)
        if not self.__modules.has_key(module):
            self.__modules[module] = {}

        configured = False
        # initing option
        if not self.__modules[module].has_key(name):
            self.initOption(module, name, value)
            # self.__modules[module][name] = [value, None, None, None]
            configured = True
        # overwriting already inited option
        elif overwrite:
            opt = self.__modules[module][name]
            # convert value if we have a conversion function and the value
            # is a string
            if opt[1] is not None and type(value) in types.StringTypes:
                value = opt[1](value)
            self.__modules[module][name][0] = value
            configured = True

        if configured and 'log' in name:
            [self.configLogger(mod) for mod in self.__modules.iterkeys()]

    def getOption(self, module, name):
        return self.__modules[module][name][0]

    @staticmethod
    def convBool(s):
        """Convert a config string to a bool value.

        Strings which lower() is in ('1', 'on', 'true', 'yes') evaluate to
        True. Bools are passed through.

        Use this as conv field for switch options.
        """
        if type(s) == bool:
            return s
        elif type(s) in types.StringTypes:
            if s.lower() in ('1', 'yes', 'on', 'true'):
                return True
            else:
                return False
        else:
            raise ValueError("argument s(%s) must be bool,"
                             " str or unicode!"%(s))

    @staticmethod
    def convList(s):
        """Tokenize a config string and return tokens stored in a list.
        E.g., 'file.1,file.2' will be returned as [file.1, file.2].
        None will be returned if argument is None.
        """
        if s is None:
            return None
        try:
            tokens = s.split(',')
            return tokens
        except:
            raise StandardError("Must specify string")

    @staticmethod
    def convParamList(s):
        """Convert a config string to a parameter dictionary.

        Converts a string of the form 'PARNAME1:PARVAL1,PARNAME2:PARVAL2...'
        to a dictionay
        {PARNAME1 : float(PARVAL1), PARNAME2 : float(PARVAL2)} .

        None will be returned if argument is None.
        """
        if s is None:
            return None
        s = s.strip()
        s = s.split(',')
        s = [pair.split('=') for pair in s]
        d = dict()
        for pname, pval in s:
            d[pname] = float(pval)
        return d

    def getLogger(self, module=None):
        return logging.getLogger()
        # if module in (None, 'global'):
            # return logging.getLogger('')
        # else:
            # return logging.getLogger(module)

    def configLogger(self, module):
        return
        curlog = self.getLogger(module)
        try:
            lvl = self.getOption(module, 'loglevel')
        except KeyError:
            lvl = self.getOption('global', 'loglevel')
        curlog.setLevel(self.__loglevels[lvl.lower()])

        curlog.handlers = []
        try:
            names = self.getOption(module, 'logfiles').split(',')
            names = map(lambda i: i.strip(), names)
        except KeyError:
            names = ['-']

        # handle old config files where root logger logs to - (= should log
        # to stderr)
        if curlog == self.getLogger() and names == ['-']:
            names = ['stderr']
        # print "logging for '%s' to '%s' with level %s"%(module, names, lvl)

        curlog.propagate = 0
        for n in names:
            if n == '-':
                curlog.propagate = 1
                # [curlog.addHandler(h) for h in self.getLogger().handlers]
            elif n == 'stderr':
                curlog.addHandler(self.__stderr)
            else:
                handler = logging.FileHandler(n)
                formatter = logging.Formatter(
                    '%(asctime)s %(name)-10s %(levelname)-8s %(message)s',
                    '%m-%d %H:%M:%S')
                handler.setFormatter(formatter)
                curlog.addHandler(handler)
        return curlog

    def setUsage(self, usage):
        self.__op.set_usage(usage)

    def getHelp(self):
        return self.__op.format_help()

    def parseCommandline(self):
        """Parses command line and updates values.

        @returns: (options, arguments) as returned by
            optparse.OptionParser.parse_args()
        """
        opts, args = self.__op.parse_args()
        if self.__filename is None and opts.config is not None:
            self.__init__(opts.config)
        for modname, moddict in self.__modules.iteritems():
            for optname, (value, conv, cmdline, help_) in moddict.iteritems():
                if not cmdline:
                    continue
                # the value on the commandline
                cmdval = getattr(opts, cmdline)
                if cmdval is None:
                    continue
                if conv is None:
                    self.setOption(modname, optname, cmdval)
                else:
                    self.setOption(modname, optname, conv(cmdval))
        return opts, args
