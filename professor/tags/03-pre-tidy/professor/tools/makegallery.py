#!/usr/bin/env python2.5
"""makegallery.py

Create png files and a html gallery from all *.EXTENSION files.
"""

from optparse import OptionParser
import os
import subprocess

optp = OptionParser(usage="%prog [options] extension TARGET.html")
optp.add_option('-c', "--columns", action="store", type="int",
                help="# of columns of the gallery", default=1)
optp.add_option('-f', "--filetype", action="store", type="str",
                help="filetype of output images", default='png')
optp.add_option('-s', "--subdir", action="store", type="string",
                help="directory, where the images are to be found", default='.')
optp.add_option("--convert", action="store", type="string",
                help="ImageMagick convert command line with options",
                default="convert")

opts, (ext, outpath) = optp.parse_args()

out = open(outpath, "w")

files = filter(lambda s: s.endswith(ext), os.listdir(opts.subdir))
files.sort()

out.write('<html>\n'
          '<table>\n'
          '<tr>\n')

#newwidth = str(200./opts.columns) + '\%'

for i, f in enumerate(files):
    if i%opts.columns == 0:
        out.write('</tr>\n<tr>\n')
    #if not ext == 'png':
    if not ext == opts.filetype:
        newf = opts.subdir + '/' + "tn_" + f.replace(ext, opts.filetype)
        cmdline = opts.convert + ' '+opts.subdir+'/' + f + ' ' + newf
        cmdline = (cmdline.replace('(', '\\(').replace(')', '\\)')).replace('>', '\\>')
        print cmdline
        # os.system(cmdline)
        subprocess.call(cmdline, shell=True)
    else:
        newf = opts.subdir +'/' + f
    #out.write('<td><a href="%s">%s:<br><img src="%s" width="%s"></a></td>\n'%(
              #newf, newf, newf, newwidth))
    out.write('<td><a href="%s">%s:<br><img src="%s" ></a></td>\n'%(
              opts.subdir+ '/' + f, newf, newf))

out.write('</tr>\n'
          '</table>\n'
          '</html>')
